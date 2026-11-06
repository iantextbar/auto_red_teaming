# roadmap.md — build phases

Each phase can be delivered and checked on its own. The order matters: the pilot comes before
hardening because the largest risk in this project is not the code but whether the output is
useful — the previous project's concept notes were well-built and still failed that test.

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
that disagree (a vendor productivity study and an independent trial, for instance), so debates have
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

**Check:** the review gate is answered, and its findings are listed at the end of this phase.

### Pilot log (in progress)

Material for the review gate, recorded as the pilot runs.

**Summaries (2026-10-22).** Five notes, one `summariser` agent each (`claude-sonnet-5-5`,
`CLAUDE.md` loaded). Tokens as reported by the harness per agent:

| Source | Note | Stated words (target) | Quotes | Tokens | Time |
|---|---|---|---|---|---|
| `metr_productivity_2025` (51 pp, 23k words) | `early-2025-ai-developer-productivity-2025-becker` | 1478 (800–1500) | 9/9 | 93.9k | 2m34s |
| Work Trend Index (33 pp, 10k) | `2026-work-trend-index-annual-report-2026-microsoft` | 1492 (800–1500) | 9 + 1 tolerated | 61.6k | 1m29s |
| `skill_formation_ai` (31 pp, 13k) | `how-ai-impacts-skill-formation-2026-shen` | 1491 (800–1500) | 10/10 | 61.8k | 1m47s |
| Research Brief (8 pp, 4.5k) | `impact-genai-jobs-productivity-work-2026-merola` | 1340 (600–1200) | 9/9 | 40.3k | 1m13s |
| `sdd` (17 pp, 10k) | `specification-driven-development-foundation-2026-alenezi` | 1514 (800–1500) | 10/10 | 54.9k | 1m17s |

About 312k tokens in all, ~62k per source. `CLAUDE.md` is roughly 6k of each run (an estimate:
the harness reports one total per agent).

Observations so far:

- The contributor judged the summaries good.
- Every quote verified (47/48 strict, 1 tolerated for a footnote marker) — the agents' own
  `check_quotes.py` loop works.
- Notes land at the **top** of the length target or above it; the Research Brief note (2142
  words) is close to the "half the source" ceiling. Suspected cause: the agent prompt warns that a
  short note means the text was not read. Candidate for phase 2.
- Agents recorded internal inconsistencies of the sources (METR recording counts; Work Trend Index
  survey date and market count; Shen annotated-participant counts; Merola citation missing from
  its reference list) in `## Extracted facts`, attributed, without resolving them.
- Agents proposed tags in inconsistent vocabulary (`rct` vs `randomized-experiment`); the
  contributor declared five `#topic/` tags, which were applied. `sdd` has none that fit.
- Multi-page anchors appeared in key claims and were accepted (D24).

**Claims index.** 39 key claims from 5 sources; the pool is ~1,100 words (~1.5k tokens).

**Mapper, propose (2026-10-23).** One run (`claude-opus-5-5`, through a general-purpose agent told
to follow `mapper.md`: the type was not yet registered in the session). 51.8k tokens, 4 tool uses,
1m33s; it read the index files only, no source note. Two proposals (time to complete tasks; what
moderates outcomes) and six near misses, most of them two-source questions.
The contributor approved the first, with an edit (state Alenezi's single-case caveat), held the
second, and asked for the near misses to be kept as candidates (D27).

**Mapper, write (2026-10-23).** `mapper` agent, one debate
(`ai-assistance-developer-task-completion-time`, 4 sources, 3 positions, ~1,100 words). 50.0k
tokens, 11 tool uses, 1m31s. Form clean; `claims_index.py` parses it; prose anchors spot-checked
against the source notes, all supported. After it, the pool holds 7 claims (Work Trend Index only),
as D25 intends.

**Positions (2026-10-23).** General-purpose Opus agent, rules in the task message (D29);
`main-lines-by-debate`, one debate, `## Positions` ~770 words. 64.3k tokens, 15 tool uses, 1m58s.
Form clean; the anchors the agent flagged as its own (Microsoft p. 6, Alenezi p. 1–2, Becker p. 3)
checked against the source notes, all supported. With one debate, the document is mostly a
condensed copy of the debate note; the overview layer can only show its value across several
debates.

**Pilot total so far:** ~478k tokens — summaries 312k, mapper propose 51.8k, mapper write 50.0k,
positions 64.3k (excluding one stray empty agent, ~80k, a session mistake).

### Review gate findings (2026-10-27)

Answered by the contributor:

1. **Key claims** are accurate and keep the source's scope.
2. **Source notes** are usable without the PDF. Reading the paper gives more insight, but with the
   less important parts omitted the note still carries the general idea of the paper.
3. **Debates** are the right size.
4. **The positions document** is what the contributor will write the paper from, going to the
   source notes or the PDF occasionally for more detail.
5. **Token costs.** Rechecked against the subagents' transcripts. The figures in the pilot log are
   each agent's **final context**, not what it consumed: every turn re-sends the context, mostly
   as cache reads billed at a fraction of normal input. Summaries made 7–9 turns and ~150–300k
   cache-read tokens each; METR made 16 (16 separate edits fixing quotes) and ~959k. Agents read
   the extracted text in 150–600-line chunks, a turn each. Registered agents start at ~14k tokens
   of context; the general-purpose agents used for mapper propose and positions started at ~36k
   (every tool definition loaded). Summaries are ~65% of the pilot and are the cost that scales
   with the corpus. The cost levers are phase 2 items, plus D29 for the positions agent (phase 4).

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
- [ ] The pilot sources become the reference set: rerunning a skill on them is how a change to the
      skill is judged

**Check:** each skill rerun on the pilot set produces output at least as good as the reviewed pilot
output; no skill writes behind an approval step without approval.

## Phase 5 — `refresh`

- [ ] The orchestrator: count sources missing claims, ask, run `extract-claims` in parallel agents,
      run `map-debates`, stop at the approval step

**Check:** after adding a batch of PDFs, one `/refresh` leaves the vault with claims for every
summarised source and a debate proposal waiting for approval — and nothing written that needed
approval.

## Phase 7 — Survey track

- [ ] A separate specification: instrument and its versions, collection and anonymisation under the
      LGPD, where anonymised data lives and what never enters the repository, and how the survey's
      questions connect to the mapped debates

## Later

Ideas outside the current scope, recorded so they are not lost:

- BibTeX export from source-note frontmatter.
- Bibliometrics for the paper's method section (the previous project's `bibliometria.md` has the
  design: venue discipline, methodology type, practitioner vs. academic).
- Removing `docs_legacy/` and `CLAUDE_LEGACY.md` once nothing here still refers to them.

## State on 2026-11-06

Phases 0–2 done, and the review gate passed (findings under phase 1). Sprint 1 is summarised: 28
source notes, 6 debates and the positions documents `main-lines-by-debate` and
`sprint-1-by-debate`. Sprint 2 is summarised too: 23 PDFs became 23 source notes (51 in the vault,
all passing `check_quotes.py`), the debates went from 6 to 9, and `paper-ideas-evidence-map` was
updated in place. This is committed and pushed (`7c358d3`, branch `setup/structure`). Web intake is
built (D35), still uncommitted, and waits for its first real run. Next is phase 3.

**Sprint 2 log (2026-11-03 to 2026-11-06).** Run by hand with the phase 4 skills not yet written:
`summarise-pdf` followed as a procedure, `mapper` in propose and write modes.

- **Extraction.** All 23 PDFs were already extracted and unchanged; none was flagged. 12 had notes
  from an earlier session; the other 11 were summarised, one `summariser` agent each, three at a
  time.
- **Summaries.** 11 notes, 1,150–1,750 stated words (four above the 1,500 target for a long
  paper), 5–9 quotes each, all verified. Final context 32–116k tokens per agent, 50–83s each, about
  700k in total. One agent edited a note after its quote check; the check was rerun by hand and
  passed.
- **Mapping.** `mapper` propose: 4 proposals and 1 near miss, 76k tokens, 3m. Write: 3 new debates
  and 4 stances added to `ai-assistance-developer-task-completion-time`, 153k tokens, 5m. The
  matrix now reads 48 stances over 33 sources; 133 claims remain in the pool.
- **A near miss stayed a candidate.** The contributor asked for the AI-anxiety learning question
  (Wang, Ugur) as a debate. It has two sources, and `CLAUDE.md` §3 requires three, so it went to
  `candidate-debates.md`. It overlaps an existing Wang-only candidate on AI anxiety and engagement.
- **Extraction limits seen.** Figures and some tables do not extract as text, so several notes give
  no numeric values for results shown only in plots. Several sources contradict themselves (counts,
  percentages, captions against text); the notes record both versions, unresolved.
- **Evidence map.** `paper-ideas-evidence-map` was edited in place (not regenerated) with the sprint
  2 evidence; `written_by` is now `claude-sonnet-5-5`, and the document says Opus wrote the first
  version. It was written by Sonnet in the main session, not by the Opus tier `CLAUDE.md` §10
  assigns to `positions`.

Also uncommitted, and not part of this work: `notes/90-meta/sprint-2-candidates.md` (proposed
reading for sprint 2, now fulfilled), `references/annotations/ai-coding-attention-context.md`, and
the edits to the docs, `CLAUDE.md`, the agent prompt and the scripts.

**Waiting on a contributor:**

- The new tags proposed by the sprint 2 agents and the mapper, for `taxonomy.md`: `#topic/`
  annotation-quality, selective-prediction, uncertainty-calibration, spec-driven-development (also
  proposed earlier), ai-anxiety, code-review, code-quality, code-hallucination-abstention,
  risk-control, selective-labels-evaluation; `#method/` statistical-sampling, repository-mining,
  propensity-matching, survey, simulation-validation, vision-paper, statistical-guarantee,
  theoretical-analysis, calibration-guarantee, controlled-experiment; `#source/` peer-reviewed and
  preprint (both facets are empty). Two pairs overlap (`calibration-guarantee` and
  `statistical-guarantee`; `risk-control` and `selective-prediction`). No note carries them yet.
- Review of the three new debates and the updated time debate. In the latter, `## Question` still
  says "seven settings" and `## Why they differ` omits the four new sources.
- `interest` on the sprint 2 notes, set by agents on inference: `independent` for `He` (the
  acknowledgements mention Google research awards and Cloud credits); `source_type` for `Bucinca`
  (`peer-reviewed` or `preprint`).
- Whether to merge the two AI-anxiety candidates, and a third source to make it a debate.
- The 17 uncommitted paths, and whether they go in one commit or several.
- The first real `/summarise-web` run (phase 6).
- Two wording points flagged in review, still in the notes: "52 developers" for Shen in two debate
  notes and `main-lines-by-debate` (the source note says 52 participants, most of them developers);
  and the phrase in `main-lines-by-debate` that Merola "cites Becker et al. (2025)", which touches
  the overlap the contributor asked not to raise.
- No question hubs exist, so the positions documents' `question:` is empty; hubs are written by
  contributors.
- Earlier points for the review of the notes, not rechecked since: confirm `interest` on the pilot
  notes (Work Trend Index `vendor`; Shen `undetermined` — Anthropic authors, GPT-4o tested; the
  others `independent`); whether to declare a tag for `sdd` (`#topic/spec-driven-development` was
  proposed); the `#topic/` tags have no definitions in `taxonomy.md` yet.

**How we work** (per the contributor): each script, agent and skill gets a short design
walk-through and the contributor's OK before it is written; lead with the simplest design and note
what it gives up. Decisions and their reasons go in `decisions.md`.

`docs_legacy/` and `CLAUDE_LEGACY.md` are kept as reference (Portuguese, previous project).
