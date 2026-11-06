"""Check that the quotes in source notes appear verbatim on the page they cite.

    uv run scripts/check_quotes.py [NOTE ...]

NOTE defaults to every note in notes/20-sources/. For each note with a `pdf:` field, every bullet
in `## Quotes` of the form `- "..." (p. N)` (or `(pp. N-M)`) is looked up in the extracted text
(data/extracted/, written by extract_pdf.py), and every `(p. N)` anchor elsewhere in the note must
point to a page that exists. A note with a `snapshot:` field instead is checked the same way, with
`(¶ N)` against the numbered paragraphs of its snapshot (references/web/, written by
capture_web.py). `(§ name)` anchors are not checked.

Comparison is verbatim after normalising, on both sides: Unicode compatibility forms (ligatures),
quote and dash characters, soft hyphens, whitespace, and hyphens between letters -- so line-break
hyphenation ("ran-" / "domly") and compounds broken at a line end ("self-" / "reported") both
match. `...`, `…` and `[...]` mark gaps: the fragments must appear in order.

Two tolerances are reported, never silent: a quote found only after removing footnote markers
glued to words ("condition1." -> "condition."), and a quote that runs onto the next page.

It cannot check paraphrase; whether a key claim reports its page faithfully is the checker
agent's job. Exits 1 if any quote or anchor fails.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from capture_web import parse_paragraphs
from extract_pdf import OUT_ROOT, ROOT, parse_pages
from vault import NoteFormatError, read_note, sections

NOTES_DIR = ROOT / "notes" / "20-sources"
PDF_PREFIX = "references/pdfs/"
WEB_PREFIX = "references/web/"

QUOTE_LINE = re.compile(r'^- ["“](?P<quote>.+)["”] \((?P<anchor>[^()]*)\)$')
PAGE_REF = r"pp?\. \d+(?:\s*[-–]\s*\d+)?"
PARAGRAPH_REF = r"¶ \d+(?:\s*[-–]\s*\d+)?"
GAP = re.compile(r"\s*(?:\[[^\]]*\]|\.\.\.|…)\s*")
FOOTNOTE_MARKER = re.compile(r"(?:(?<=[^\W\d_])|(?<=\)))\d{1,3}\b")

CHARS = str.maketrans(
    {
        **dict.fromkeys("‘’‚‛′", "'"),
        **dict.fromkeys("“”„‟″", '"'),
        **dict.fromkeys("‐‑‒–—―−\u00ad", "-"),
    }
)

FAILING = {"wrong-page", "not-found", "malformed", "bad-anchor"}


@dataclass(frozen=True)
class Units:
    """What a document is divided into, and how an anchor cites one."""

    label: str  # how a detail message cites one
    name: str
    ref: str

    @property
    def exact(self) -> re.Pattern[str]:
        return re.compile(rf"^{self.ref}$")

    @property
    def any_anchor(self) -> re.Pattern[str]:
        # One or more references in one pair of parentheses: (p. 4), (pp. 4–6), (p. 3, p. 8),
        # (p. 3; pp. 10–12). A claim drawn from several pages lists them all (D24).
        return re.compile(rf"\(({self.ref}(?:\s*[,;]\s*{self.ref})*)\)")


PAGES = Units("p.", "page", PAGE_REF)
PARAGRAPHS = Units("¶", "paragraph", PARAGRAPH_REF)


@dataclass(frozen=True)
class Finding:
    line: int
    status: str  # verified | tolerated | wrong-page | not-found | malformed | bad-anchor
    detail: str = ""
    quote: str = ""

    @property
    def failed(self) -> bool:
        return self.status in FAILING


@dataclass
class NoteReport:
    path: Path
    quotes: int = 0
    findings: list[Finding] = field(default_factory=list)
    skipped: str = ""  # reason the note was not checked
    error: str = ""  # reason the note could not be checked; counts as a failure

    @property
    def failed(self) -> bool:
        return bool(self.error) or any(f.failed for f in self.findings)


# --- pure transformation -------------------------------------------------------------------


def normalise(text: str, drop_footnotes: bool = False) -> str:
    text = unicodedata.normalize("NFKC", text).translate(CHARS)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r" ?- ?", "-", text)
    text = re.sub(r"(?<=\w)-(?=\w)", "", text)
    if drop_footnotes:
        text = FOOTNOTE_MARKER.sub("", text)
    return text.strip()


def fragments(quote: str) -> list[str]:
    """The quote split at its gaps (ellipses, bracketed insertions)."""
    return [f for f in GAP.split(quote) if f.strip()]


def contains_in_order(parts: list[str], text: str) -> bool:
    pos = 0
    for part in parts:
        i = text.find(part, pos)
        if i < 0:
            return False
        pos = i + len(part)
    return True


def _span(pages: dict[int, str], first: int, last: int) -> str:
    return "\n".join(pages[n] for n in range(first, last + 1) if n in pages)


def check_quote(
    quote: str, first: int, last: int, pages: dict[int, str], units: Units = PAGES
) -> tuple[str, str]:
    """Locate a quote cited at pages (or paragraphs) first..last. Returns (status, detail)."""
    raw = fragments(quote)
    if not raw:
        return "malformed", "empty quote"
    if first < 1 or last < first or last > max(pages, default=0):
        cited = f"{units.label} {first}-{last}"
        return "bad-anchor", f"cites {cited}, document has {len(pages)} {units.name}s"

    for drop in (False, True):
        parts = [normalise(f, drop) for f in raw]
        tolerance = "footnote markers ignored" if drop else ""
        if contains_in_order(parts, normalise(_span(pages, first, last), drop)):
            return ("tolerated", tolerance) if drop else ("verified", "")
        # Runs onto the next page: found across the break, but not on the next page alone --
        # a quote wholly on p. N+1 cited as p. N is a wrong page, not a page break.
        if (
            last + 1 in pages
            and contains_in_order(parts, normalise(_span(pages, first, last + 1), drop))
            and not contains_in_order(parts, normalise(pages[last + 1], drop))
        ):
            runs_onto = f"runs onto {units.label} {last + 1}"
            detail = "; ".join(filter(None, [runs_onto, tolerance]))
            return "tolerated", detail

    for drop in (False, True):
        parts = [normalise(f, drop) for f in raw]
        elsewhere = [
            n
            for n in sorted(pages)
            if not first <= n <= last and contains_in_order(parts, normalise(pages[n], drop))
        ]
        if elsewhere:
            where = ", ".join(f"{units.label} {n}" for n in elsewhere)
            return "wrong-page", f"not on the cited {units.name}; found on {where}"

    return "not-found", "not found anywhere in the document"


def parse_anchor(anchor: str, units: Units = PAGES) -> tuple[int, int] | None:
    anchor = anchor.strip()
    if not units.exact.match(anchor):
        return None
    numbers = [int(n) for n in re.findall(r"\d+", anchor)]
    return numbers[0], numbers[-1]


def check_quote_line(
    line: str, number: int, pages: dict[int, str], units: Units = PAGES
) -> Finding:
    m = QUOTE_LINE.match(line.rstrip())
    if not m:
        expected = f'expected - "quote" ({units.label} N)'
        return Finding(number, "malformed", expected, line.strip())
    quote = m.group("quote")
    anchor = parse_anchor(m.group("anchor"), units)
    if anchor is None:
        detail = f"not a {units.name} anchor: ({m.group('anchor')})"
        return Finding(number, "malformed", detail, quote)
    status, detail = check_quote(quote, *anchor, pages, units)
    return Finding(number, status, detail, quote)


def check_anchors(
    lines: list[str], skip: set[int], page_count: int, units: Units = PAGES
) -> list[Finding]:
    """Every anchor outside the quotes, multi-page ones included, must point to something real."""
    findings = []
    for number, line in enumerate(lines, start=1):
        if number in skip:
            continue
        for m in units.any_anchor.finditer(line):
            pages = [int(n) for n in re.findall(r"\d+", m.group(1))]
            if any(not 1 <= p <= page_count for p in pages):
                detail = f"anchor {m.group(0)} outside the document's {page_count} {units.name}s"
                findings.append(Finding(number, "bad-anchor", detail))
    return findings


def link_path(value: object) -> str:
    """The vault path in a `pdf:` or `snapshot:` field: '[[references/x.pdf]]', with or without an
    alias.

    An unquoted [[...]] in YAML parses as a nested list; that form is accepted too.
    """
    while isinstance(value, list) and value:
        value = value[0]
    if not isinstance(value, str):
        return ""
    target = value.strip().removeprefix("[[").removesuffix("]]")
    return target.split("|")[0].split("#")[0].strip()


# --- I/O -----------------------------------------------------------------------------------


def check_note(path: Path, out_root: Path = OUT_ROOT, root: Path = ROOT) -> NoteReport:
    report = NoteReport(path)
    try:
        note = read_note(path)
        quotes_text = sections(note.body).get("Quotes", "")
    except NoteFormatError as e:
        report.error = str(e)
        return report

    target = link_path(note.meta.get("pdf"))
    snapshot = link_path(note.meta.get("snapshot"))
    if target:
        units = PAGES
        if not target.startswith(PDF_PREFIX):
            report.error = f"pdf: {target} is not under {PDF_PREFIX}"
            return report
        extracted = out_root / Path(target.removeprefix(PDF_PREFIX)).with_suffix(".md")
        if not extracted.exists():
            report.error = f"{extracted} missing; run extract_pdf.py"
            return report
        pages = parse_pages(extracted.read_text(encoding="utf-8"))
    elif snapshot:
        units = PARAGRAPHS
        if not snapshot.startswith(WEB_PREFIX):
            report.error = f"snapshot: {snapshot} is not under {WEB_PREFIX}"
            return report
        if not (root / snapshot).exists():
            report.error = f"{snapshot} missing; run capture_web.py"
            return report
        pages = parse_paragraphs((root / snapshot).read_text(encoding="utf-8"))
    else:
        report.skipped = "no pdf or snapshot"
        return report

    lines = path.read_text(encoding="utf-8").splitlines()
    heading = next((i for i, line in enumerate(lines) if line.rstrip() == "## Quotes"), None)
    quote_lines: set[int] = set()
    if heading is not None:
        for line in quotes_text.splitlines():
            if not line.startswith("- "):
                continue  # translations and other non-bullet lines
            number = next(
                i + 1
                for i in range(heading, len(lines))
                if lines[i] == line and i + 1 not in quote_lines
            )
            quote_lines.add(number)
            report.findings.append(check_quote_line(line, number, pages, units))
    report.quotes = len(quote_lines)
    report.findings += check_anchors(lines, quote_lines, len(pages), units)
    report.findings.sort(key=lambda f: f.line)
    return report


def shorten(text: str, width: int = 70) -> str:
    return text if len(text) <= width else text[: width - 1] + "…"


def format_report(report: NoteReport, root: Path = ROOT) -> list[str]:
    name = report.path.relative_to(root) if report.path.is_relative_to(root) else report.path
    if report.skipped:
        return [f"{name}: skipped ({report.skipped})"]
    if report.error:
        return [f"{name}: ERROR {report.error}"]
    count = {s: sum(f.status == s for f in report.findings) for s in ("verified", "tolerated")}
    failing = sum(f.failed for f in report.findings)
    out = [
        f"{name}: {report.quotes} quotes, {count['verified']} verified, "
        f"{count['tolerated']} tolerated, {failing} failing"
    ]
    for f in report.findings:
        if f.status == "verified":
            continue
        label = "FAIL" if f.failed else "warn"
        quote = f'  "{shorten(f.quote)}"' if f.quote else ""
        out.append(f"  line {f.line:<4} {label}  {f.status}: {f.detail}{quote}")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("notes", nargs="*", type=Path, help="source notes (default: all)")
    args = parser.parse_args(argv)

    paths = [p.resolve() for p in args.notes] or sorted(NOTES_DIR.rglob("*.md"))
    reports = [check_note(p) for p in paths]
    for report in reports:
        print("\n".join(format_report(report)))

    checked = [r for r in reports if not r.skipped]
    failed = sum(r.failed for r in checked)
    print(
        f"{len(checked)} notes checked: {len(checked) - failed} clean, {failed} with failures; "
        f"{len(reports) - len(checked)} skipped"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
