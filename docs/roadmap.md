# roadmap.md — build phases

Each phase can be delivered and checked on its own. The order matters: the pilot comes before
hardening because the largest risk in this project is not the code but whether the output is
useful — the previous project's concept notes were well-built and still failed that test.

**Inherited tooling.** This vault was adapted from an earlier one on AI-assisted coding (D36).
Phases 0, 1, 2 and the built part of 6 were done there; the scripts, agents, skills and rules they
produced carry over unchanged, and their checkboxes stay marked. The pilot that validated them ran
on the previous corpus; its logs stayed with that project.

Mark `[x]` when done.

## Phase 0 — Foundation

Structure and configuration, no logic.

- [x] Folder tree: `notes/00-questions`, `10-debates`, `20-sources`, `30-positions`,
      `90-meta/templates`, `references/annotations`, `references/pdfs`, `data/`, `scripts/`,
      `tests/`, `.claude/skills/`, `.claude/agents/`
- [x] `pyproject.toml`: runtime and dev dependencies (`techstack.md`); remove `main.py`
- [x] `.gitignore`: all of `data/` (D17), `references/pdfs/**/*.pdf` (D14),
      `.obsidian/workspace.json`
- [x] `.obsidian/app.json` with `userIgnoreFilters` for `data/`, `scripts/`, `docs/`, `tests/`
- [x] Templates in `notes/90-meta/templates/`: source, debate, positions, question, annotation —
      matching `CLAUDE.md` §3
- [x] `notes/90-meta/taxonomy.md` skeleton: the five facets, **no tags** — tags are declared by
      contributors (`CLAUDE.md` §4.9)
- [x] `README.md`: what the vault is, where to put each material, the skills, the merge ritual

**Check:** open the vault in Obsidian; `data/`, `scripts/`, `docs/` and `tests/` do not appear in
search or the quick switcher; `references/` does.

## Phase 1 — Pilot

The thinnest end-to-end chain, run on **4–6 real PDFs** chosen by a contributor — ideally sources
that disagree (a vendor benchmark and an independent study, for instance), so debates have
something to map. Rough is fine: a step may be run by hand in the main session instead of through a
finished skill.

- [x] `scripts/extract_pdf.py`, with tests for page markers and idempotence
- [x] `scripts/check_quotes.py`, with tests for altered quote, wrong page, ligatures, hyphenation
- [x] Draft `summariser` agent and `summarise-pdf` skill
- [x] One source note per pilot PDF
- [x] `check_quotes.py` run over all pilot notes; every failure fixed or explained
- [x] Minimal `scripts/claims_index.py`
- [x] Draft `mapper` agent proposes debates from the pool; a contributor approves 1–3
- [x] `scripts/matrix.py`
- [x] One `/positions` run, on a brief written by a contributor
- [x] **Review gate** — a contributor answers, in writing:
  - Are the key claims accurate, and do they keep the source's hedges and scope?
  - Is each source note usable without reopening the PDF?
  - Are the debates the right size — not trivial, not so broad that every source qualifies?
  - Is the positions document material you would write the paper from?
  - What did the run cost in tokens, per step?

**Check:** the review gate is answered (done on the previous corpus; lessons below).

### Pilot lessons carried over

From the previous corpus, still relevant here: the contributor judged the summaries usable without
the PDF and the key claims faithful to the source's hedges and scope; notes tend to land at the top
of the length target; summaries are about two thirds of a batch's token cost, and the cost that
scales with the corpus (D31–D34).

## Phase 2 — Spec revision

- [x] Fold the pilot findings into `CLAUDE.md`, the templates, `project.md` and `techstack.md`
      (D31, D32)
- [x] Decide on the agent tiers again (D34): Sonnet stays for summaries; Haiku stays undecided,
      since it has never run on the corpus, and is tested when the checker is built (phase 4)
- [x] Decide whether agents get a shorter contract than `CLAUDE.md` (D34): no; they keep the whole
      file
- [x] Decide whether the `summariser` prompt asks for fewer turns (adopted, D32): the extracted
      text read in one call instead of 150–600-line chunks, and every quote failure fixed in one
      pass. Each turn
      re-sends the whole context; in the pilot, METR took 16 turns (16 separate edits) and ~959k
      cache-read tokens, the other summaries 7–9 turns and ~150–300k

**Check:** every pilot finding is either reflected in a spec change or recorded as a deliberate
non-change.

## Phase 6 — Web intake

Brought forward, ahead of phase 3, at the contributor's request (D35). The number stays because
other documents cite it.

- [x] Decide how to handle web sources (D35): snapshots in `references/web/`, every non-heading
      block numbered `[¶ N]`
- [x] `scripts/capture_web.py`, with offline tests
- [x] `check_quotes.py` verifies `(¶ N)` against the snapshot
- [x] `summariser` takes a snapshot; `summarise-web` skill
- [x] Smoke test on real pages, written outside the vault: two posts captured (93 and 42 numbered
      blocks), one PDF URL flagged. `--paste` and the `robots.txt` block have only run against mock
      responses
- [ ] First real run: a contributor picks a post, `/summarise-web` writes the note, the contributor
      reads it

**Check:** the note's quotes pass `check_quotes.py`, `claims_index.py` picks up its claims, and the
contributor finds the note as usable as a PDF one.

## Phase 3 — Harden the scripts

- [ ] Full `scripts/vault.py`: notes, slugs, sections, source identity, non-destructive merge
- [ ] Existing scripts moved onto `vault.py`
- [ ] `vault.py` owns the note format, not just reading: one anchor parser (today three regexes —
      `check_quotes.py` strict, `claims_index.py` and `matrix.py` loose, `(p. foo)` passes); one
      reader of `## Stances` (today `claims_index.py` counts any link, `matrix.py` the strict form);
      `link_target` moved out of `claims_index.py`, merged with `check_quotes.link_path`; `slug`
      moved out of `capture_web.py`; `sections()` with line numbers, replacing the line lookup in
      `check_quotes.check_note`
- [ ] Tests for all guarded properties in `techstack.md`

**Check:** `uv run pytest` passes offline; `uv run ruff check` is clean.

## Phase 4 — Final skills and agents

- [ ] `new-source`, `summarise-pdf`, `summarise-web`, `extract-claims`, `map-debates`, `positions`,
      `stress-test`, `review-links`, `audit` (with `scripts/audit.py`)
- [ ] Agents `summariser-light` and `checker`; `summariser` and `mapper` finalised
- [ ] Decide the checker's model (D34): plant known errors (a dropped hedge, a widened scope, a
      wrong page) in copies of a few notes and see whether Haiku catches them
- [ ] The sprint 1 sources become the reference set: rerunning a skill on them is how a change to
      the skill is judged

**Check:** each skill rerun on the reference set produces output at least as good as the reviewed
output; no skill writes behind an approval step without approval.

## Phase 5 — `refresh`

- [ ] The orchestrator: count sources missing claims, ask, run `extract-claims` in parallel agents,
      run `map-debates`, stop at the approval step

**Check:** after adding a batch of PDFs, one `/refresh` leaves the vault with claims for every
summarised source and a debate proposal waiting for approval — and nothing written that needed
approval.

## Phase 7 — Product track

- [ ] A separate specification for the product (automatic vulnerability detection and compliance
      checking for AI-generated code): requirements drawn from positions documents written with a
      product lens, the benchmarks and datasets in the corpus that will evaluate it, and where it
      lives (repository, stack)

## Later

Ideas outside the current scope, recorded so they are not lost:

- BibTeX export from source-note frontmatter.
- `scripts/papers_dashboard.py` belongs to the previous project (its evidence map and external
  survey); adapt it to this project's paper and product, or remove it.
- `scripts/capture_web.py`'s user-agent still names the previous vault.

## State on 2026-11-11

Tooling inherited from the previous vault (D36); `notes/` is empty and `taxonomy.md` declares no
tags yet. Sprint 1 holds 6 PDFs in `references/pdfs/sprint1/`, all extracted (13–47 pages,
7–22k words, none flagged) and summarised (log below). Next: contributors declare tags and
review the notes; then map debates.

**Sprint 1 log (2026-11-11).** `summarise-pdf` followed as a procedure; one `summariser` agent per
PDF (`claude-sonnet-5-5`), three at a time. Tokens are each agent's final context as reported by
the harness.

| PDF | Note | Stated words (target) | Quotes | Tokens | Time |
|---|---|---|---|---|---|
| `asleep_on_keyboard` (15 pp, 15k) | `asleep-at-the-keyboard-copilot-security-2021-pearce` | 1536 (800–1500) | 10/10 | 71.8k | 63s |
| `ai_assistants_insecure_code` (16 pp, 13k) | `do-users-write-more-insecure-code-2023-perry` | ~1500 (800–1500) | 8/8 | 60.9k | 60s |
| `baxbench` (47 pp, 17k) | `baxbench-correct-secure-backends-2025-vero` | ~1470 (800–1500) | 9/9 | 93.8k | 80s |
| CyberGym (46 pp, 22k) | `cybergym-evaluating-ai-agents-cybersecurity-2026-wang` | 1522 (800–1500) | 8/8 | 109.6k | 86s |
| `is_vibe_coding_safe` (24 pp, 15k) | `is-vibe-coding-safe-2026-zhao` | ~1390 (800–1500) | 8/8 | 72.3k | 66s |
| `threat_remains` (13 pp, 7k) | `range-shrinks-threat-remains-2026-churilov` | ~1250 (600–1200) | 8/8 | 47.8k | 56s |

About 456k tokens in all. 51/51 quotes verified, none tolerated; `claims_index.py` reads 51 key
claims from 6 sources, all in the pool. Notes again land at the top of the length target or just
above it. Every agent recorded internal inconsistencies of its source, unresolved. No tags applied:
`taxonomy.md` declares none yet.

**How we work** (per the contributor): each script, agent and skill gets a short design
walk-through and the contributor's OK before it is written; lead with the simplest design and note
what it gives up. Decisions and their reasons go in `decisions.md`.
