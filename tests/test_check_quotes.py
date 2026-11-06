import pytest

from check_quotes import (
    check_anchors,
    check_note,
    check_quote,
    check_quote_line,
    fragments,
    link_path,
    normalise,
)
from extract_pdf import Extraction, Page, render

PAGES = {
    1: "Measuring the Impact of Early-2025 AI\non Experienced Open-Source Developers",
    2: (
        "Each task is ran-\ndomly assigned to allow or disallow AI usage, and we measure how\n"
        "long it takes developers to complete tasks in each condition1. Developers, who\n"
        "typically have self-\nreported experience, use the ﬁrst tools available.\n"
        "We ﬁnd that allowing AI actually increases completion time by 19%— devel-\n"
        "opers are slower when using AI tooling. This effect is"
    ),
    3: "robust across outcome measures.\nDevelopers’ forecasts were wrong.",
}


def status(quote, first, last=None):
    return check_quote(quote, first, last or first, PAGES)


# --- normalisation -------------------------------------------------------------------------


def test_normalise_unifies_quotes_dashes_and_whitespace():
    assert normalise("Developers’  “slow”\n— yes") == 'Developers\' "slow"-yes'


def test_normalise_expands_ligatures():
    assert normalise("ﬁrst eﬀect") == "first effect"


def test_fragments_split_at_ellipses_and_brackets():
    assert fragments("one ... two … three [...] four [sic] five") == [
        "one",
        "two",
        "three",
        "four",
        "five",
    ]


# --- check_quote ---------------------------------------------------------------------------


def test_exact_quote_is_verified():
    assert status("we measure how long it takes developers", 2) == ("verified", "")


def test_altered_quote_is_not_found():
    assert status("we measure how quickly developers", 2)[0] == "not-found"


def test_case_change_is_not_verbatim():
    assert status("We measure how long it takes developers", 2)[0] == "not-found"


def test_quote_on_another_page_is_reported_with_where():
    assert status("robust across outcome measures", 2) == (
        "wrong-page",
        "not on the cited page; found on p. 3",
    )


def test_ligatures_do_not_cause_false_alarms():
    assert status("use the first tools available", 2)[0] == "verified"


def test_line_break_hyphenation_both_kinds_in_one_quote():
    quote = "Each task is randomly assigned"
    assert status(quote, 2)[0] == "verified"
    assert status("typically have self-reported experience", 2)[0] == "verified"


def test_soft_hyphen_at_line_break_joins_the_word():
    page = "humans actively interrogate AI recom\u00ad\nmendations rather than"
    assert check_quote("interrogate AI recommendations rather", 1, 1, {1: page})[0] == "verified"


def test_em_dash_spacing_is_tolerated():
    assert status("increases completion time by 19%—developers are slower", 2)[0] == "verified"


def test_gaps_must_appear_in_order():
    assert status("Each task is randomly assigned ... in each condition1.", 2)[0] == "verified"
    assert status("in each condition1. ... Each task is randomly assigned", 2)[0] == "not-found"


def test_quote_copying_the_footnote_marker_is_verified_strictly():
    assert status("in each condition1. Developers", 2) == ("verified", "")


def test_quote_without_the_footnote_marker_is_tolerated_and_says_so():
    assert status("in each condition. Developers", 2) == ("tolerated", "footnote markers ignored")


def test_quote_running_onto_the_next_page_is_tolerated_and_says_so():
    assert status("This effect is robust across outcome measures", 2) == (
        "tolerated",
        "runs onto p. 3",
    )


def test_page_range_anchor():
    assert status("This effect is robust across outcome measures", 2, 3)[0] == "verified"


def test_anchor_beyond_the_document():
    assert status("anything", 9)[0] == "bad-anchor"


# --- quote lines and anchors ---------------------------------------------------------------


def test_quote_line_with_curly_quotes_and_range():
    line = "- “This effect is robust across outcome measures” (pp. 2–3)"
    assert check_quote_line(line, 10, PAGES).status == "verified"


def test_quote_line_without_anchor_is_malformed():
    assert check_quote_line('- "Each task is randomly assigned"', 7, PAGES).status == "malformed"


def test_quote_line_with_a_web_anchor_is_malformed_for_a_pdf():
    assert check_quote_line('- "Each task" (¶ 4)', 7, PAGES).status == "malformed"


def test_anchors_outside_quotes_are_range_checked():
    lines = ["- Developers were slower (p. 2)", "- A claim (p. 99)", "- quoted (p. 50)"]
    findings = check_anchors(lines, skip={3}, page_count=3)
    assert [(f.line, f.status) for f in findings] == [(2, "bad-anchor")]


def test_multi_page_anchors_are_range_checked():
    lines = [
        "- Perceived and actual impact diverged (p. 2, p. 3)",
        "- A claim on two pages, one missing (p. 2, p. 9)",
        "- A range and a page (pp. 1–2; p. 3)",
        "- A range running past the end (pp. 2–4)",
    ]
    findings = check_anchors(lines, skip=set(), page_count=3)
    assert [(f.line, f.status) for f in findings] == [(2, "bad-anchor"), (4, "bad-anchor")]


@pytest.mark.parametrize(
    "value",
    [
        "[[references/pdfs/sprint1/a.pdf]]",
        "[[references/pdfs/sprint1/a.pdf|METR]]",
        "references/pdfs/sprint1/a.pdf",
        [["references/pdfs/sprint1/a.pdf"]],
    ],
)
def test_link_path_forms(value):
    assert link_path(value) == "references/pdfs/sprint1/a.pdf"


def test_link_path_empty():
    assert link_path(None) == ""


# --- whole note ----------------------------------------------------------------------------

NOTE = """---
type: source
pdf: "[[references/pdfs/sprint1/a.pdf]]"
---

## Stated by the source

### Key claims

- Developers were slower with AI (p. 2)
- A claim with a broken anchor (p. 12)

## Quotes

- "Each task is randomly assigned" (p. 2)
- "in each condition. Developers" (p. 2)
- "robust across outcome measures" (p. 2)

Translation (p. 2): not a quote line.

## Reading
"""


@pytest.fixture
def extracted(tmp_path):
    out_root = tmp_path / "extracted"
    target = out_root / "sprint1" / "a.md"
    target.parent.mkdir(parents=True)
    pages = [Page(n, "", text) for n, text in PAGES.items()]
    target.write_text(render(Extraction("sprint1/a.pdf", "x", pages)))
    return out_root


def test_check_note_reports_each_quote_with_its_line(tmp_path, extracted):
    note = tmp_path / "note.md"
    note.write_text(NOTE)

    report = check_note(note, extracted)

    assert report.quotes == 3
    assert [(f.line, f.status) for f in report.findings] == [
        (11, "bad-anchor"),
        (15, "verified"),
        (16, "tolerated"),
        (17, "wrong-page"),
    ]
    assert report.failed


def test_note_without_pdf_is_skipped(tmp_path, extracted):
    note = tmp_path / "web.md"
    note.write_text("---\ntype: source\npdf:\n---\n\n## Quotes\n")
    assert check_note(note, extracted).skipped == "no pdf or snapshot"


def test_missing_extraction_is_an_error(tmp_path):
    note = tmp_path / "note.md"
    note.write_text(NOTE)
    report = check_note(note, tmp_path / "nowhere")
    assert "run extract_pdf.py" in report.error
    assert report.failed


def test_duplicate_section_is_an_error_naming_nothing_lost(tmp_path, extracted):
    note = tmp_path / "dup.md"
    note.write_text(NOTE + "\n## Quotes\n")
    report = check_note(note, extracted)
    assert "## Quotes" in report.error


# --- web snapshots -------------------------------------------------------------------------


SNAPSHOT = (
    "---\nurl: https://example.org\n---\n\n# T\n\n[¶ 1] First paragraph.\n\n[¶ 2] Second one.\n"
)


@pytest.fixture
def web_root(tmp_path):
    (tmp_path / "references" / "web").mkdir(parents=True)
    (tmp_path / "references" / "web" / "post.md").write_text(SNAPSHOT, encoding="utf-8")
    return tmp_path


def web_note(root, body):
    note = root / "note.md"
    meta = 'snapshot: "[[references/web/post.md]]"'
    note.write_text(f"---\n{meta}\n---\n\n{body}\n", encoding="utf-8")
    return check_note(note, root / "nowhere", root)


@pytest.mark.parametrize(
    "quote, anchor, expected",
    [
        ("First paragraph.", "¶ 1", "verified"),
        ("Second one.", "¶ 1", "wrong-page"),
        ("An altered quote.", "¶ 1", "not-found"),
        ("First paragraph.", "¶ 9", "bad-anchor"),
        ("First paragraph.", "p. 1", "malformed"),
    ],
)
def test_snapshot_quotes(web_root, quote, anchor, expected):
    report = web_note(web_root, f'## Quotes\n\n- "{quote}" ({anchor})')
    assert [f.status for f in report.findings] == [expected]


def test_wrong_paragraph_says_paragraph(web_root):
    report = web_note(web_root, '## Quotes\n\n- "Second one." (¶ 1)')
    assert report.findings[0].detail == "not on the cited paragraph; found on ¶ 2"


def test_snapshot_anchors_outside_quotes_are_range_checked(web_root):
    report = web_note(web_root, "## Argument\n\nFine (¶ 2), and not (¶ 2, ¶ 9).")
    assert [f.status for f in report.findings] == ["bad-anchor"]


def test_missing_snapshot_is_an_error(tmp_path):
    report = web_note(tmp_path, "## Quotes")
    assert "missing" in report.error
