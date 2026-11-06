"""Extract per-page text from the PDFs in references/pdfs/ into data/extracted/.

    uv run scripts/extract_pdf.py [PATH ...] [--force] [--no-limit]

PATH is a PDF or a folder under references/pdfs/ (default: all of it, recursively). Each PDF
becomes data/extracted/<same relative path>.md, so references/pdfs/sprint2/x.pdf lands in
data/extracted/sprint2/x.md.

The output is a YAML header followed by every page, each preceded by a marker carrying the
physical page index -- the N that `(p. N)` anchors cite (docs/decisions.md, D15):

    <!-- page 5 -->                 or, when the PDF carries a differing printed label,
    <!-- page 5 | printed 1127 -->

The text is written as pymupdf returns it; normalisation belongs to check_quotes.py. An output
whose source hash and extractor version match is skipped unless --force. PDFs with no text layer,
or above 200 pages / 80k words (D16), are flagged and not written; --no-limit lifts the size
limit. Exits 1 if any PDF was flagged or failed.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import frontmatter
import pymupdf
import yaml

EXTRACTOR_VERSION = 1
MAX_PAGES = 200
MAX_WORDS = 80_000
MIN_WORDS = 50  # below this, the whole document counts as having no text layer

ROOT = Path(__file__).resolve().parent.parent
PDF_ROOT = ROOT / "references" / "pdfs"
OUT_ROOT = ROOT / "data" / "extracted"


@dataclass(frozen=True)
class Page:
    number: int  # physical index, 1-based
    label: str  # printed page label from the PDF, "" when absent
    text: str


@dataclass(frozen=True)
class Extraction:
    source: str  # path relative to references/pdfs/, with forward slashes
    sha256: str
    pages: list[Page]

    @property
    def words(self) -> int:
        return sum(len(p.text.split()) for p in self.pages)

    @property
    def empty_pages(self) -> list[int]:
        return [p.number for p in self.pages if not p.text.strip()]


@dataclass(frozen=True)
class Outcome:
    source: str
    status: str  # extracted | skipped | flagged | error
    detail: str = ""


# --- pure transformation -------------------------------------------------------------------


def size_flag(
    pages: int, words: int, max_pages: int = MAX_PAGES, max_words: int = MAX_WORDS
) -> str:
    """Why a document is too large to extract, or "" if it is not."""
    if pages > max_pages:
        return f"oversized ({pages} pages > {max_pages})"
    if words > max_words:
        return f"oversized ({words} words > {max_words})"
    return ""


def text_flag(words: int, min_words: int = MIN_WORDS) -> str:
    """Why a document counts as having no text layer, or "" if it has one."""
    if words < min_words:
        return f"no text layer ({words} words; needs OCR)"
    return ""


def marker(page: Page) -> str:
    if page.label and page.label != str(page.number):
        return f"<!-- page {page.number} | printed {page.label} -->"
    return f"<!-- page {page.number} -->"


MARKER = re.compile(r"^<!-- page (\d+)(?: \| printed .*?)? -->$", re.MULTILINE)


def parse_pages(text: str) -> dict[int, str]:
    """Read an extracted file back into {physical page: text}; the inverse of render()."""
    body = frontmatter.loads(text).content
    matches = list(MARKER.finditer(body))
    return {
        int(m.group(1)): body[
            m.end() : matches[i + 1].start() if i + 1 < len(matches) else None
        ].strip("\n")
        for i, m in enumerate(matches)
    }


def render(ex: Extraction) -> str:
    header = {
        "source": ex.source,
        "sha256": ex.sha256,
        "pages": len(ex.pages),
        "words": ex.words,
        "anchor": "physical",
        "empty_pages": ex.empty_pages,
        "extractor_version": EXTRACTOR_VERSION,
    }
    parts = ["---", yaml.safe_dump(header, sort_keys=False, allow_unicode=True).rstrip(), "---"]
    for page in ex.pages:
        parts += ["", marker(page), "", page.text.rstrip()]
    return "\n".join(parts) + "\n"


# --- I/O -----------------------------------------------------------------------------------


def output_path(rel: Path, out_root: Path) -> Path:
    return out_root / rel.with_suffix(".md")


def is_current(out: Path, sha256: str) -> bool:
    if not out.exists():
        return False
    meta = frontmatter.load(str(out)).metadata
    return meta.get("sha256") == sha256 and meta.get("extractor_version") == EXTRACTOR_VERSION


def extract_file(
    pdf: Path,
    pdf_root: Path,
    out_root: Path,
    force: bool = False,
    limit: bool = True,
    max_pages: int = MAX_PAGES,
    max_words: int = MAX_WORDS,
) -> Outcome:
    rel = pdf.relative_to(pdf_root)
    source = rel.as_posix()
    out = output_path(rel, out_root)
    sha256 = hashlib.sha256(pdf.read_bytes()).hexdigest()

    if not force and is_current(out, sha256):
        return Outcome(source, "skipped", "unchanged")

    try:
        with pymupdf.open(pdf) as doc:
            if limit and (flag := size_flag(doc.page_count, 0, max_pages, max_words)):
                return Outcome(source, "flagged", flag)
            pages = [Page(i + 1, p.get_label(), p.get_text()) for i, p in enumerate(doc)]
    except Exception as e:  # a corrupt or encrypted PDF must not stop the batch
        return Outcome(source, "error", f"{type(e).__name__}: {e}")

    ex = Extraction(source, sha256, pages)
    flag = text_flag(ex.words)
    if not flag and limit:
        flag = size_flag(len(pages), ex.words, max_pages, max_words)
    if flag:
        return Outcome(source, "flagged", flag)

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(ex), encoding="utf-8")
    detail = f"{len(pages)} pages, {ex.words} words"
    if ex.empty_pages:
        detail += f", empty pages {ex.empty_pages}"
    return Outcome(source, "extracted", detail)


def find_pdfs(paths: list[Path], pdf_root: Path) -> list[Path]:
    found: set[Path] = set()
    for path in paths:
        path = path.resolve()
        if not path.is_relative_to(pdf_root):
            raise SystemExit(f"error: {path} is not under {pdf_root}")
        if path.is_dir():
            found.update(p for p in path.rglob("*") if p.suffix.lower() == ".pdf")
        elif path.suffix.lower() == ".pdf":
            found.add(path)
        else:
            raise SystemExit(f"error: {path} is not a PDF or a folder")
    return sorted(found)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "paths", nargs="*", type=Path, help="PDFs or folders under references/pdfs/"
    )
    parser.add_argument("--force", action="store_true", help="re-extract even if unchanged")
    parser.add_argument("--no-limit", action="store_true", help="lift the size limit")
    args = parser.parse_args(argv)

    pdfs = find_pdfs(args.paths or [PDF_ROOT], PDF_ROOT.resolve())
    outcomes = [
        extract_file(pdf, PDF_ROOT.resolve(), OUT_ROOT, args.force, not args.no_limit)
        for pdf in pdfs
    ]
    for o in outcomes:
        print(f"{o.status:<10} {o.source}" + (f"  ({o.detail})" if o.detail else ""))

    counts = {
        s: sum(o.status == s for o in outcomes)
        for s in ("extracted", "skipped", "flagged", "error")
    }
    print(", ".join(f"{n} {s}" for s, n in counts.items()))
    return 1 if counts["flagged"] or counts["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
