"""Freeze a web page as a numbered markdown snapshot in references/web/.

    uv run scripts/capture_web.py URL [--name SLUG] [--paste FILE]

The snapshot is a YAML header followed by the page's main text, with every non-heading block --
each paragraph, list item and table row -- on one line and numbered in document order. That number
is the N that `(¶ N)` anchors cite (docs/decisions.md, D35):

    ## A heading
    [¶ 12] A paragraph.

Snapshots are committed: a page can change or vanish, so the snapshot is the evidence behind the
anchors. For that reason a snapshot is never replaced. Capturing the same text again is skipped;
different text is flagged and the snapshot left alone.

A page is flagged and nothing is written when robots.txt disallows it, the server answers with an
HTTP error, the response is a PDF, or fewer than 50 words come out (usually a page built by
JavaScript). --paste FILE is the manual route for those: save the page's text to a file and it is
numbered the same way. Exits 1 if the page was flagged or failed.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser

import frontmatter
import httpx
import trafilatura
import yaml

from extract_pdf import MIN_WORDS, ROOT, Outcome

EXTRACTOR_VERSION = 1
USER_AGENT = "ai-assisted-coding-vault/0.1 (academic research; captures pages chosen by hand)"
TIMEOUT = 30
MAX_BYTES = 10_000_000
SLUG_WORDS = 8

OUT_ROOT = ROOT / "references" / "web"

NUMBERED = re.compile(r"^\[¶ (\d+)\] (.*)$", re.MULTILINE)
HEADING = re.compile(r"^#{1,6} ")
ITEM = re.compile(r"^(?:[-*+] |\d+[.)] )")
TABLE_RULE = re.compile(r"^\|[-:| ]+\|$")


@dataclass(frozen=True)
class Page:
    title: str = ""
    author: str = ""
    date: str = ""
    sitename: str = ""


class Flag(Exception):
    """The page cannot be captured, for a reason the contributor can act on."""


# --- pure transformation -------------------------------------------------------------------


def plain(text: str) -> str:
    """Drop inline markdown, so a quote copied from the page matches the snapshot verbatim."""
    text = text.replace("**", "").replace("`", "")
    return re.sub(r"(?<!\w)\*(\S(?:.*?\S)?)\*(?!\w)", r"\1", text)


def number_blocks(markdown: str) -> str:
    """Put each block on one line, numbered in order. Headings keep their line, unnumbered.

    Consecutive plain lines are one paragraph. A list item or a table row is a block of its own,
    so it can be cited alone. Code fences only separate blocks; their lines become one paragraph.
    """
    out: list[str] = []
    paragraph: list[str] = []
    count = 0

    def add(text: str) -> None:
        nonlocal count
        count += 1
        out.append(f"[¶ {count}] {plain(text)}")

    def flush() -> None:
        if paragraph:
            add(" ".join(paragraph))
            paragraph.clear()

    for raw in markdown.splitlines():
        line = raw.strip()
        if not line or line.startswith("```"):
            flush()
        elif HEADING.match(line):
            flush()
            out.append(plain(line))
        elif ITEM.match(line):
            flush()
            add(ITEM.sub("", line))
        elif line.startswith("|"):
            flush()
            if not TABLE_RULE.match(line):
                add(line)
        else:
            paragraph.append(line)
    flush()
    return "\n\n".join(out)


def parse_paragraphs(text: str) -> dict[int, str]:
    """Read a snapshot back into {paragraph number: text}; the inverse of number_blocks()."""
    body = frontmatter.loads(text).content
    return {int(m.group(1)): m.group(2) for m in NUMBERED.finditer(body)}


def slug(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return "-".join(re.findall(r"[a-z0-9]+", ascii_text.lower())[:SLUG_WORDS])


def url_slug(url: str) -> str:
    parts = urlsplit(url)
    return slug(f"{parts.netloc} {parts.path}")


def robots_allows(robots_txt: str, url: str, agent: str = USER_AGENT) -> bool:
    parser = RobotFileParser()
    parser.parse(robots_txt.splitlines())
    # The parser denies everything until it has seen a rule, so an empty robots.txt, or one with
    # only a Sitemap line, would read as a ban; RFC 9309 says the opposite.
    parser.modified()
    return parser.can_fetch(agent, url)


def render(url: str, page: Page, method: str, captured: str, body: str) -> str:
    header = {
        "url": url,
        "title": page.title,
        "author": page.author,
        "date": page.date,
        "sitename": page.sitename,
        "captured": captured,
        "method": method,
        "sha256": body_hash(body),
        "paragraphs": len(NUMBERED.findall(body)),
        "words": len(NUMBERED.sub(r"\2", body).split()),
        "extractor_version": EXTRACTOR_VERSION,
    }
    head = yaml.safe_dump(header, sort_keys=False, allow_unicode=True).rstrip()
    return f"---\n{head}\n---\n\n{body}\n"


def body_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def extract(html: str) -> tuple[str, Page]:
    """The page's main text as markdown, and its metadata; ("", ...) when nothing comes out."""
    markdown = trafilatura.extract(
        html, output_format="markdown", include_tables=True, include_links=False
    )
    meta = trafilatura.extract_metadata(html)
    page = Page(
        title=(meta.title if meta else "") or "",
        author=(meta.author if meta else "") or "",
        date=(meta.date if meta else "") or "",
        sitename=(meta.sitename if meta else "") or "",
    )
    return markdown or "", page


# --- I/O -----------------------------------------------------------------------------------


def check_robots(url: str, client: httpx.Client) -> None:
    response = client.get(urljoin(url, "/robots.txt"))
    # RFC 9309: a 4xx means no rules apply; a server error means assume everything is disallowed.
    if response.status_code >= 500:
        raise Flag(f"robots.txt answered HTTP {response.status_code}; use --paste")
    if response.is_success and not robots_allows(response.text, url):
        raise Flag("disallowed by robots.txt; use --paste")


def fetch(url: str, client: httpx.Client, max_bytes: int = MAX_BYTES) -> str:
    with client.stream("GET", url) as response:
        if not response.is_success:
            raise Flag(f"HTTP {response.status_code}; use --paste")
        if "pdf" in response.headers.get("content-type", "").lower():
            raise Flag("the URL is a PDF; save it under references/pdfs/ and use /summarise-pdf")
        data = b""
        for chunk in response.iter_bytes():
            data += chunk
            if len(data) > max_bytes:
                raise Flag(f"response larger than {max_bytes} bytes")
        return data.decode(response.encoding or "utf-8", errors="replace")


def capture(
    url: str,
    client: httpx.Client,
    out_root: Path = OUT_ROOT,
    name: str = "",
    paste: str | None = None,
    captured: str = "",
) -> Outcome:
    try:
        if paste is None:
            check_robots(url, client)
            markdown, page = extract(fetch(url, client))
            method = "fetch"
        else:
            markdown, method = paste, "paste"
            first_heading = next(
                (ln.lstrip("# ").strip() for ln in paste.splitlines() if HEADING.match(ln)), ""
            )
            page = Page(title=first_heading)
    except Flag as e:
        return Outcome(url, "flagged", str(e))
    except httpx.HTTPError as e:  # a network failure must not read as a page with no text
        return Outcome(url, "error", f"{type(e).__name__}: {e}")

    body = number_blocks(markdown)
    words = len(NUMBERED.sub(r"\2", body).split())
    if words < MIN_WORDS:
        return Outcome(url, "flagged", f"only {words} words came out; use --paste")

    out = out_root / f"{name or slug(page.title) or url_slug(url)}.md"
    if out.exists():
        if frontmatter.load(str(out)).metadata.get("sha256") == body_hash(body):
            return Outcome(url, "skipped", f"unchanged: {out.name}")
        return Outcome(url, "flagged", f"{out.name} exists with different text; left alone")

    out.parent.mkdir(parents=True, exist_ok=True)
    text = render(url, page, method, captured or date.today().isoformat(), body)
    out.write_text(text, encoding="utf-8")
    return Outcome(url, "extracted", f"{out.name}, {len(NUMBERED.findall(body))} ¶, {words} words")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("url", help="the page's URL; recorded in the snapshot even with --paste")
    parser.add_argument("--name", default="", help="snapshot filename, without .md")
    parser.add_argument("--paste", type=Path, help="take the text from this file; no fetching")
    args = parser.parse_args(argv)

    paste = args.paste.read_text(encoding="utf-8") if args.paste else None
    headers = {"User-Agent": USER_AGENT}
    with httpx.Client(headers=headers, timeout=TIMEOUT, follow_redirects=True) as client:
        o = capture(args.url, client, name=args.name, paste=paste)
    print(f"{o.status:<10} {o.source}" + (f"  ({o.detail})" if o.detail else ""))
    return 1 if o.status in ("flagged", "error") else 0


if __name__ == "__main__":
    sys.exit(main())
