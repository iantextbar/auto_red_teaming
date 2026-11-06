import pytest

from vault import NoteFormatError, read_note, sections, subsections

BODY = """## Stated by the source

### What it is about

A trial.

### Key claims

- Developers were slower (p. 4)

## Quotes

- "A # inside a quote is text" (p. 2)

## Reading
"""


def test_read_note_tolerates_obsidian_reindented_lists(tmp_path):
    flat = tmp_path / "flat.md"
    flat.write_text("---\ntitle: 'A'\nauthors:\n- Becker\n- Rush\n---\n\nBody\n")
    indented = tmp_path / "indented.md"
    indented.write_text('---\ntitle: "A"\nauthors:\n  - Becker\n  - Rush\n---\n\nBody\n')

    assert read_note(flat).meta == read_note(indented).meta
    assert read_note(flat).meta["authors"] == ["Becker", "Rush"]


def test_read_note_empty_field_is_none(tmp_path):
    p = tmp_path / "n.md"
    p.write_text("---\npdf:\nyear: 2025\n---\n")
    note = read_note(p)
    assert note.meta["pdf"] is None
    assert note.meta["year"] == 2025


def test_sections_in_document_order():
    assert list(sections(BODY)) == ["Stated by the source", "Quotes", "Reading"]


def test_level_three_heading_does_not_end_a_section():
    stated = sections(BODY)["Stated by the source"]
    assert "### Key claims" in stated
    assert subsections(stated)["Key claims"] == "- Developers were slower (p. 4)"


def test_hash_inside_text_is_not_a_heading():
    assert sections(BODY)["Quotes"] == '- "A # inside a quote is text" (p. 2)'


def test_empty_section_maps_to_empty_string():
    assert sections(BODY)["Reading"] == ""


def test_missing_section_is_absent():
    assert "Connections" not in sections(BODY)


def test_preamble_goes_under_empty_key():
    assert sections("Intro line\n\n## A\n\nx\n") == {"": "Intro line", "A": "x"}
    assert "" not in sections("\n\n## A\n")


def test_trailing_spaces_on_heading_are_ignored():
    assert list(sections("## Quotes  \n\n- q\n")) == ["Quotes"]


def test_duplicate_heading_raises():
    with pytest.raises(NoteFormatError, match="## Quotes"):
        sections("## Quotes\n\n## Quotes\n")
    with pytest.raises(NoteFormatError, match="### Key claims"):
        subsections("### Key claims\n\n### Key claims\n")
