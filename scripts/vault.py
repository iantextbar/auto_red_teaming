"""Shared access to vault notes.

Phase 1 scope: reading only. Every script that needs a note's frontmatter or one of its sections
goes through here, so there is one parser and one set of edge cases. Writing notes, slugs, source
identity and the non-destructive merge arrive in phase 3 (docs/roadmap.md).

Frontmatter is read with python-frontmatter, never by regex: Obsidian re-indents YAML lists and
rewrites quotes on save, and a regex anchored at column 0 silently stops matching
(docs/techstack.md, "Obsidian's YAML normalisation").
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import frontmatter


class NoteFormatError(ValueError):
    """A note does not have the structure the scripts rely on.

    Raised without the file name, which the parsing functions do not know; each script's per-note
    loop catches it and reports it with the note's path.
    """


@dataclass(frozen=True)
class Note:
    path: Path
    meta: dict
    body: str


def read_note(path: str | Path) -> Note:
    post = frontmatter.load(str(path))
    return Note(path=Path(path), meta=dict(post.metadata), body=post.content)


def _split(text: str, level: int) -> dict[str, str]:
    # `## ` (hashes followed by a space) at the start of a line: a `###` heading never matches
    # the `##` pattern, because its third character is `#`, not a space.
    heading = re.compile(rf"^{'#' * level} (.+?)[ \t]*$", re.MULTILINE)
    result: dict[str, str] = {}
    matches = list(heading.finditer(text))

    preamble = text[: matches[0].start()] if matches else text
    if preamble.strip():
        result[""] = preamble.strip("\n")

    for i, m in enumerate(matches):
        name = m.group(1).strip()
        if name in result:
            raise NoteFormatError(f"duplicate heading '{'#' * level} {name}'")
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        result[name] = text[m.end() : end].strip("\n")
    return result


def sections(body: str) -> dict[str, str]:
    """Split a note body by `##` headings, in document order.

    Each value is the section's content without its heading and without surrounding blank lines;
    an empty section maps to "". Text before the first heading, if any, goes under "". A heading
    that appears twice raises NoteFormatError.
    """
    return _split(body, 2)


def subsections(text: str) -> dict[str, str]:
    """Split a section's content by `###` headings; same rules as sections()."""
    return _split(text, 3)
