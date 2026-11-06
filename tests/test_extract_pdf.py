import frontmatter
import pymupdf
import pytest

from extract_pdf import (
    Extraction,
    Page,
    extract_file,
    find_pdfs,
    marker,
    parse_pages,
    render,
    size_flag,
)

WORDS = " ".join(["word"] * 30)  # 30 words: two such pages clear MIN_WORDS (50), one does not


def make_pdf(path, pages, labels_from=None):
    """Write a PDF with one string per page; blank strings make image-like empty pages."""
    doc = pymupdf.open()
    for text in pages:
        page = doc.new_page()
        if text:
            page.insert_textbox(pymupdf.Rect(72, 72, 520, 760), text)
    if labels_from is not None:
        doc.set_page_labels(
            [{"startpage": 0, "prefix": "", "style": "D", "firstpagenum": labels_from}]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)
    return path


@pytest.fixture
def vault(tmp_path):
    return tmp_path / "pdfs", tmp_path / "extracted"


# --- pure ----------------------------------------------------------------------------------


def test_marker_uses_physical_index():
    assert marker(Page(5, "", "x")) == "<!-- page 5 -->"


def test_marker_records_a_differing_printed_label():
    assert marker(Page(5, "1127", "x")) == "<!-- page 5 | printed 1127 -->"
    assert marker(Page(5, "5", "x")) == "<!-- page 5 -->"


def test_render_is_deterministic_and_marks_every_page():
    ex = Extraction(
        "s1/a.pdf", "abc", [Page(1, "", "one\n"), Page(2, "", ""), Page(3, "", "three")]
    )
    out = render(ex)
    assert out == render(ex)
    assert [line for line in out.splitlines() if line.startswith("<!--")] == [
        "<!-- page 1 -->",
        "<!-- page 2 -->",
        "<!-- page 3 -->",
    ]
    meta = frontmatter.loads(out).metadata
    assert meta["pages"] == 3
    assert meta["words"] == 2
    assert meta["empty_pages"] == [2]
    assert meta["anchor"] == "physical"


def test_size_flag():
    assert size_flag(200, 80_000) == ""
    assert "201 pages" in size_flag(201, 10)
    assert "80001 words" in size_flag(10, 80_001)


# --- I/O -----------------------------------------------------------------------------------


def test_extracts_with_page_markers_and_labels(vault):
    pdf_root, out_root = vault
    pdf = make_pdf(pdf_root / "sprint1" / "a.pdf", [WORDS, WORDS], labels_from=1127)

    outcome = extract_file(pdf, pdf_root, out_root)

    assert outcome.status == "extracted"
    text = (out_root / "sprint1" / "a.md").read_text()
    assert "<!-- page 1 | printed 1127 -->" in text
    assert "<!-- page 2 | printed 1128 -->" in text
    assert frontmatter.loads(text).metadata["source"] == "sprint1/a.pdf"


def test_output_mirrors_sprint_folders(vault):
    pdf_root, out_root = vault
    for sprint in ("sprint1", "sprint2"):
        make_pdf(pdf_root / sprint / "same.pdf", [WORDS, f"{sprint} {WORDS}"])
        extract_file(pdf_root / sprint / "same.pdf", pdf_root, out_root)

    assert "sprint1 word" in (out_root / "sprint1" / "same.md").read_text()
    assert "sprint2 word" in (out_root / "sprint2" / "same.md").read_text()


def test_second_run_skips_and_changes_nothing(vault):
    pdf_root, out_root = vault
    pdf = make_pdf(pdf_root / "a.pdf", [WORDS, WORDS])
    extract_file(pdf, pdf_root, out_root)
    first = (out_root / "a.md").read_bytes()

    assert extract_file(pdf, pdf_root, out_root).status == "skipped"
    assert extract_file(pdf, pdf_root, out_root, force=True).status == "extracted"
    assert (out_root / "a.md").read_bytes() == first


def test_changed_pdf_is_re_extracted(vault):
    pdf_root, out_root = vault
    pdf = make_pdf(pdf_root / "a.pdf", [WORDS, WORDS])
    extract_file(pdf, pdf_root, out_root)
    make_pdf(pdf, [WORDS, WORDS, "new page " + WORDS])

    assert extract_file(pdf, pdf_root, out_root).status == "extracted"
    assert "<!-- page 3 -->" in (out_root / "a.md").read_text()


def test_pdf_without_text_is_flagged_and_not_written(vault):
    pdf_root, out_root = vault
    pdf = make_pdf(pdf_root / "scan.pdf", ["", "", ""])

    outcome = extract_file(pdf, pdf_root, out_root)

    assert outcome.status == "flagged"
    assert "no text" in outcome.detail
    assert not (out_root / "scan.md").exists()


def test_partly_empty_pdf_is_extracted_with_empty_pages_listed(vault):
    pdf_root, out_root = vault
    pdf = make_pdf(pdf_root / "mixed.pdf", [WORDS, "", WORDS])

    assert extract_file(pdf, pdf_root, out_root).status == "extracted"
    assert frontmatter.load(out_root / "mixed.md").metadata["empty_pages"] == [2]


def test_oversized_pdf_is_flagged_unless_limit_lifted(vault):
    pdf_root, out_root = vault
    pdf = make_pdf(pdf_root / "big.pdf", [WORDS] * 4)

    flagged = extract_file(pdf, pdf_root, out_root, max_pages=3)
    assert flagged.status == "flagged" and "4 pages" in flagged.detail
    assert not (out_root / "big.md").exists()

    assert extract_file(pdf, pdf_root, out_root, limit=False, max_pages=3).status == "extracted"


def test_too_many_words_is_flagged(vault):
    pdf_root, out_root = vault
    pdf = make_pdf(pdf_root / "wordy.pdf", [WORDS, WORDS])

    outcome = extract_file(pdf, pdf_root, out_root, max_words=59)
    assert outcome.status == "flagged" and "60 words" in outcome.detail


def test_corrupt_pdf_is_an_error_not_a_crash(vault):
    pdf_root, out_root = vault
    bad = pdf_root / "bad.pdf"
    bad.parent.mkdir(parents=True)
    bad.write_bytes(b"not a pdf")

    assert extract_file(bad, pdf_root, out_root).status == "error"


def test_find_pdfs_walks_folders_recursively(vault):
    pdf_root, _ = vault
    a = make_pdf(pdf_root / "sprint1" / "a.pdf", [WORDS])
    b = make_pdf(pdf_root / "sprint2" / "deep" / "b.PDF", [WORDS])
    (pdf_root / "sprint1" / "notes.txt").write_text("x")

    assert find_pdfs([pdf_root], pdf_root.resolve()) == sorted([a.resolve(), b.resolve()])


def test_find_pdfs_rejects_paths_outside_the_pdf_root(vault, tmp_path):
    pdf_root, _ = vault
    pdf_root.mkdir()
    with pytest.raises(SystemExit):
        find_pdfs([tmp_path], pdf_root.resolve())


def test_parse_pages_inverts_render():
    pages = [Page(1, "", "one\ntwo\n"), Page(2, "ii", ""), Page(3, "", "three")]
    text = render(Extraction("a.pdf", "x", pages))
    assert parse_pages(text) == {1: "one\ntwo", 2: "", 3: "three"}
