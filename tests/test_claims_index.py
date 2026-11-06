from claims_index import Debate, Index, Source, build, parse_claims, parse_debate, run

CLAIMS = """- Allowing AI increased completion time by 19% (p. 1).
- Perceived and actual impact diverged (p. 3, p. 8).
- The slowdown holds across estimators (pp. 26–27)
- A web claim (¶ 14)
- A section claim (§ Methods).
- A claim the summariser forgot to anchor.
Not a bullet (p. 2)"""


def test_parse_claims_keeps_text_and_anchor_and_drops_trailing_period():
    claims, unanchored = parse_claims(CLAIMS)
    assert claims == [
        "Allowing AI increased completion time by 19% (p. 1)",
        "Perceived and actual impact diverged (p. 3, p. 8)",
        "The slowdown holds across estimators (pp. 26–27)",
        "A web claim (¶ 14)",
        "A section claim (§ Methods)",
    ]
    assert unanchored == ["- A claim the summariser forgot to anchor."]


def test_parenthesis_inside_the_claim_is_not_the_anchor():
    claims, _ = parse_claims("- Economists (39%) overestimated the speedup (p. 9).")
    assert claims == ["Economists (39%) overestimated the speedup (p. 9)"]


DEBATE_BODY = """## Question

Does AI speed up experienced developers?

## Positions

### Speeds up

Prose.

### Slows down

Prose.

## Why they differ

## Stances

- [[becker-2025]] · Slows down · supports · (p. 1)
- [[notes/20-sources/peng-2023.md|Peng]] · Speeds up · supports · (p. 2)

## Reading
"""


def test_parse_debate_reads_question_positions_and_linked_sources():
    debate = parse_debate("speed", {"question": "Does AI speed up developers?"}, DEBATE_BODY)
    assert debate.question == "Does AI speed up developers?"
    assert debate.positions == ["Speeds up", "Slows down"]
    assert debate.sources == {"becker-2025", "peng-2023"}


def test_links_outside_stances_do_not_count():
    body = "## Positions\n\n### A\n\nSee [[other-2024]].\n\n## Stances\n"
    assert parse_debate("d", {}, body).sources == set()


def index():
    return Index(
        sources=[
            Source("becker-2025", "preprint", "independent", ["Slower (p. 1)"]),
            Source("microsoft-2026", "report", "vendor", ["Readiness matters (p. 4)"]),
            Source("empty-2024", "", "", []),
        ],
        debates=[Debate("speed", "Faster?", ["Yes", "No"], {"becker-2025"})],
    )


def test_pool_holds_only_sources_not_in_any_debate():
    files = build(index())
    assert "[[becker-2025]]" in files["claims.md"]
    assert "[[becker-2025]]" not in files["pool.md"]
    assert "## [[microsoft-2026]] · report · vendor" in files["pool.md"]
    assert "empty-2024" not in files["claims.md"]


def test_all_puts_every_claim_in_the_pool():
    assert "[[becker-2025]]" in build(index(), all_claims=True)["pool.md"]


def test_debates_index_is_one_line_per_debate():
    assert "- [[speed]] · Faster? · positions: Yes | No" in build(index())["debates.md"]
    assert "No debates yet." in build(Index())["debates.md"]


SOURCE_NOTE = """---
type: source
source_type: preprint
interest: independent
tags:
  - topic/developer-productivity
---

## Stated by the source

### Key claims

- Allowing AI increased completion time by 19% (p. 1).
- An unanchored claim.

## Quotes
"""


def make_vault(tmp_path):
    notes = tmp_path / "notes"
    (notes / "20-sources").mkdir(parents=True)
    (notes / "10-debates").mkdir()
    (notes / "20-sources" / "becker-2025.md").write_text(SOURCE_NOTE)
    (notes / "20-sources" / "dup.md").write_text(
        "---\ntype: source\n---\n\n## Quotes\n\n## Quotes\n"
    )
    return notes


def test_run_reports_problems_and_still_indexes_the_rest(tmp_path):
    notes = make_vault(tmp_path)
    result = run(notes, tmp_path / "data")

    assert any("without anchor" in p for p in result.problems)
    assert any(p.startswith("dup.md") and "## Quotes" in p for p in result.problems)
    claims = (tmp_path / "data" / "claims.md").read_text()
    assert "- Allowing AI increased completion time by 19% (p. 1)" in claims
    assert "unanchored" not in claims


def test_second_run_changes_nothing(tmp_path):
    notes = make_vault(tmp_path)
    data = tmp_path / "data"
    run(notes, data)
    first = {p.name: p.read_bytes() for p in data.iterdir()}
    run(notes, data)
    assert {p.name: p.read_bytes() for p in data.iterdir()} == first
