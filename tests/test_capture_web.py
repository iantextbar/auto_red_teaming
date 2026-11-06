import httpx
import pytest

from capture_web import (
    Flag,
    Page,
    capture,
    fetch,
    number_blocks,
    parse_paragraphs,
    plain,
    render,
    robots_allows,
    slug,
)

WORDS = " ".join(f"word{i}" for i in range(60))
HTML = f"""<html><head><title>A Post About Code</title>
<meta name="author" content="Ana Lima"></head><body><article><h1>A Post About Code</h1>
<p>{WORDS}</p><p>A second paragraph, long enough for the extractor to keep it in the output.</p>
</article></body></html>"""
URL = "https://example.org/blog/post"


def client(pages=None, robots="", status=200, content_type="text/html"):
    pages = {URL: HTML} if pages is None else pages

    def handler(request):
        url = str(request.url)
        if url.endswith("/robots.txt"):
            return httpx.Response(200, text=robots)
        if url in pages:
            return httpx.Response(status, text=pages[url], headers={"content-type": content_type})
        return httpx.Response(404)

    return httpx.Client(transport=httpx.MockTransport(handler))


# --- numbering -----------------------------------------------------------------------------


def test_each_block_is_numbered_in_order_and_headings_are_not():
    body = number_blocks("# Title\n\nOne.\n\n## Part\n\nTwo.\n\n- three\n- four")
    assert body.splitlines()[::2] == [
        "# Title",
        "[¶ 1] One.",
        "## Part",
        "[¶ 2] Two.",
        "[¶ 3] three",
        "[¶ 4] four",
    ]


def test_numbering_is_deterministic():
    text = "One.\n\n- two\n\nThree."
    assert number_blocks(text) == number_blocks(text)


def test_wrapped_lines_are_one_paragraph():
    assert number_blocks("one\ntwo\n\nthree") == "[¶ 1] one two\n\n[¶ 2] three"


def test_table_rows_are_blocks_and_the_rule_is_dropped():
    assert number_blocks("| a | b |\n|---|---|\n| 1 | 2 | ") == "[¶ 1] | a | b |\n\n[¶ 2] | 1 | 2 |"


def test_code_fence_separates_blocks():
    assert number_blocks("```\nx = 1\ny = 2\n```\nAfter.") == "[¶ 1] x = 1 y = 2\n\n[¶ 2] After."


def test_inline_markup_is_dropped_so_quotes_match():
    assert plain("has **bold** and *italic* and `code` but 2*3*4 stays") == (
        "has bold and italic and code but 2*3*4 stays"
    )


def test_parse_paragraphs_reads_back_what_was_numbered():
    body = number_blocks("# T\n\nOne.\n\n- two")
    text = render(URL, Page(title="T"), "fetch", "2026-10-30", body)
    assert parse_paragraphs(text) == {1: "One.", 2: "two"}


# --- helpers -------------------------------------------------------------------------------


def test_slug_is_ascii_and_bounded():
    assert slug("Programação: um Guia!") == "programacao-um-guia"
    assert slug(" ".join("abcdefghij")) == "a-b-c-d-e-f-g-h"


@pytest.mark.parametrize("robots", ["", "Sitemap: https://example.org/s.xml", "<html>oops</html>"])
def test_robots_with_no_rules_allows(robots):
    assert robots_allows(robots, URL)


def test_robots_disallow():
    assert not robots_allows("User-agent: *\nDisallow: /blog/", URL)


# --- capture -------------------------------------------------------------------------------


def test_capture_writes_snapshot_with_header(tmp_path):
    outcome = capture(URL, client(), tmp_path, captured="2026-10-30")
    assert outcome.status == "extracted"
    out = tmp_path / "a-post-about-code.md"
    text = out.read_text(encoding="utf-8")
    assert "url: https://example.org/blog/post" in text
    assert "author: Ana Lima" in text
    assert "method: fetch" in text
    assert "captured: '2026-10-30'" in text
    assert parse_paragraphs(text)[1] == WORDS


def test_same_text_is_skipped(tmp_path):
    capture(URL, client(), tmp_path)
    assert capture(URL, client(), tmp_path).status == "skipped"


def test_changed_text_is_flagged_and_the_snapshot_left_alone(tmp_path):
    capture(URL, client(), tmp_path)
    out = tmp_path / "a-post-about-code.md"
    before = out.read_text(encoding="utf-8")
    changed = HTML.replace("word3 ", "CHANGED ")
    outcome = capture(URL, client({URL: changed}), tmp_path)
    assert outcome.status == "flagged"
    assert "different text" in outcome.detail
    assert out.read_text(encoding="utf-8") == before


def test_pdf_response_is_flagged(tmp_path):
    outcome = capture(URL, client(content_type="application/pdf"), tmp_path)
    assert outcome.status == "flagged"
    assert "references/pdfs" in outcome.detail
    assert not list(tmp_path.iterdir())


def test_thin_page_is_flagged(tmp_path):
    thin = "<html><body><div id='app'>Loading</div></body></html>"
    outcome = capture(URL, client({URL: thin}), tmp_path)
    assert outcome.status == "flagged"
    assert "--paste" in outcome.detail
    assert not list(tmp_path.iterdir())


def test_robots_block_is_flagged_without_fetching_the_page(tmp_path):
    outcome = capture(URL, client({}, robots="User-agent: *\nDisallow: /"), tmp_path)
    assert outcome.status == "flagged"
    assert "robots" in outcome.detail


def test_http_error_is_flagged(tmp_path):
    outcome = capture(URL, client(status=403), tmp_path)
    assert outcome.status == "flagged"
    assert "403" in outcome.detail


def test_network_failure_is_an_error(tmp_path):
    def handler(request):
        raise httpx.ConnectError("no route")

    outcome = capture(URL, httpx.Client(transport=httpx.MockTransport(handler)), tmp_path)
    assert outcome.status == "error"


def test_oversized_response_is_flagged():
    with pytest.raises(Flag, match="larger than"):
        fetch(URL, client(), max_bytes=10)


def test_paste_needs_no_network_and_records_the_method(tmp_path):
    def handler(request):
        raise AssertionError("no request should be made")

    offline = httpx.Client(transport=httpx.MockTransport(handler))
    outcome = capture(URL, offline, tmp_path, paste=f"# Pasted Page\n\n{WORDS}")
    assert outcome.status == "extracted"
    text = (tmp_path / "pasted-page.md").read_text(encoding="utf-8")
    assert "method: paste" in text
    assert "title: Pasted Page" in text


def test_name_overrides_the_title(tmp_path):
    capture(URL, client(), tmp_path, name="chosen")
    assert (tmp_path / "chosen.md").exists()
