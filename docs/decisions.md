# decisions.md — why things are the way they are

The specs say *what* the project does. This file keeps *why*, and what was considered and rejected,
so a later session does not re-open a settled question or "optimise away" something kept on
purpose. Newest last. When a decision is reversed, add an entry; don't edit the old one.

## 2026-10-21/22 — adapting the previous project

**D1. `CLAUDE.md` is the constitution; no per-feature specs.** Full spec-driven development (a
separate constitution, then spec → plan → tasks per component) was considered and rejected: the
constitution would duplicate `CLAUDE.md` and drift, and a skill's spec *is* its `SKILL.md`, a
script's spec *is* its tests plus the guarded properties in `techstack.md`. Docs stay lean:
`project.md`, `techstack.md`, `roadmap.md`, this file.

**D2. Pilot before hardening.** The largest risk is whether the output is useful, not the code. The
previous project's concept notes were built carefully and still failed, and that only showed in
use. Specs for debates and positions are hypotheses until the pilot (`roadmap.md`, phase 1) is
reviewed.

**D3. Concept notes replaced by key claims → debates → positions.** The previous project's atomic
concepts were one or two lines long, multiplied without limit, were extracted one paper at a time,
and rarely linked papers. What was useful was a large summary of the literature's positions.
Rejected alternatives:
- *Constrained concepts* (minimum sources, minimum length) — treats the symptom; the unit was wrong.
- *Glossary file* — not wanted.
- *Era notes* — eras are a lens requested in `/positions` ("by era"), not a note type.
- *Standalone, hand-maintained matrix* — would drift from the debates; the matrix is generated from
  the debates' `## Stances`.

**D4. `## Connections` stays in source notes, on purpose.** It looks redundant next to debates. It
is not: debates are the structured links, Connections is the free-form place for a link seen from
one paper. A contributor asked for it to be kept. Do not remove it as a simplification.

**D5. One `/positions <direction>` skill.** It replaced both a per-question `synthesise` skill and a
`map-eras` skill. What is wanted is a summary of positions built from debates and source summaries,
with a contributor directing the topics and the lens. The brief is stored verbatim in the document
so it can be regenerated against the same brief.

**D6. Key claims are written at intake, by the summariser.** It has the full text in context; a
separate pass would either re-read the PDF (expensive) or work from the summary (second-hand
anchors). `extract-claims` exists only to backfill.

**D7. Model tiers.** Sonnet writes summaries **and** key claims, backfill included — Haiku was
judged likely to flatten a hedged claim into a strong one, a failure the quote checker cannot
catch (hence also `CLAUDE.md` §4.10). Opus maps debates and drafts positions — the most
judgement-heavy work. Haiku fact-checks and handles short, low-argument sources. To be revisited
with real token costs after the pilot.

**D8. Lean frontmatter.** Dropped from the previous schema: `qualis` (no Brazilian venue ranking
needed), `eixo` and `origem` (CSV pipeline, gone), `tipo_publicacao` (covered by `source_type`),
`veiculo` (merged into `venue`), `acesso_em` (belongs in the snapshot), `modo_leitura`, and the
`revisado` boolean (redundant with `reviewed_by`). Added `summarised_by` with the **model id**, so
notes written by a lighter model can be prioritised for human review. Claude may move `status` to
`summarised`, never to `read`.

**D9. Agents draft; the main session applies.** A subagent cannot pause for approval, so anything
behind approval (debates, positions) returns from the agent as a proposal or draft. A summary a
contributor asked for is written directly — the request is the confirmation.

**D10. Contributors are unnamed.** The previous project had two named researchers and fixed
branches. Here: any number of contributors, `### <handle>` subheadings, own branch each, merge into
`main`.

**D11. English** for everything, unless a contributor states otherwise for a piece of work.

**D12. Hard rule numbering.** `CLAUDE.md` §4.10 was appended rather than inserted, so existing
references to §4.8 and §4.9 stay valid. Keep appending.

## 2026-10-22 — implementation plan for phases 0 and 1

**D13. Pilot set.** Five sprint-1 PDFs, picked to disagree: `metr_productivity_2025` (independent
trial), `2026_Work_Trend_Index_Annual_Report…` (Microsoft, vendor), `skill_formation_ai`,
`Research Brief_The impact of GenAi on jobs…` (review of empirical evidence) and `sdd`
(spec-driven development). The validated scales stay out of the pilot; their note shape is still
open (below).

**D14. PDFs are not versioned in git.** `references/pdfs/**/*.pdf` is gitignored. Sprint 1 alone
is 54 MB (one file is 19 MB), every sprint would add more, and committing the PDFs redistributes
them. Contributors share PDFs outside git under the same relative path, so `pdf:` links resolve.
Rejected: committing them (as the previous project did) and Git LFS (setup burden on every
contributor, storage quotas).

**D15. `(p. N)` is the physical page index.** Not the printed label. The physical index is what
Obsidian's `[[file.pdf#page=N]]` opens, and it is unambiguous; printed labels are often missing
from the PDF's metadata even when printed on the page, and a mix of schemes across notes would make
anchors unreliable. Where the PDF carries a differing label, the extractor records it in the page
marker (`<!-- page 5 | printed 1127 -->`), so the printed page is at hand when citing in the paper.
This reverses the "printed label when present" proposal in `techstack.md`.

**D16. Extraction size threshold: 200 pages or 80k words.** All 19 sprint-1 PDFs pass (largest:
131 pages, ~36k words). The previous project's ~120 pages / ~40k words would have flagged
`laabor_transformation-under_ai.pdf`, a legitimate report. Proceedings volumes (the previous
project's 587-page case) are still caught. `--no-limit` overrides.

**D17. All of `data/` is gitignored**, not only `data/extracted/`. Every file there (extracted
text, claims index, pool, debates index) is regenerated by a script, and committing it would only
produce merge conflicts between contributor branches. `notes/90-meta/matrix.md` is generated too
but stays committed: it is read in Obsidian.

**D18. `pymupdf` pinned below 2.0.** PyMuPDF 2.0 makes an ONNX layout runtime, `numpy`,
`networkx` and `pymupdf4llm` hard dependencies (~100 MB). The extractor uses plain per-page text,
which the self-contained 1.x line provides. Revisit only if layout-aware extraction is needed.

**D19. Source note filenames: `<short-title>-<year>-<first-author-surname>.md`.** For example
`early-2025-ai-experienced-developers-2025-becker.md`. The short title leads because that is what
a contributor types into Obsidian's quick switcher. The short title is a few distinctive words of
the real title; everything is lowercase ASCII with hyphens, and accents are dropped. The filename
does not follow the PDF's filename, which is whatever the contributor saved it as. Rejected:
`<surname>-<year>-<short-title>` (citation-style, but harder to find by topic).

**D20. Quote checking tolerances.** `check_quotes.py` compares after normalising both sides, and
removes hyphens between letters on both sides rather than trying two hyphenation variants of the
page, so a quote with both a split word and a broken compound still matches. Footnote markers
glued to words (`condition1.`) are handled by a lenient retry that strips them on both sides; a
match found that way is reported as *tolerated*, never silently as verified. Rejected for now:
having the extractor detect superscripts and mark them (`condition^1`) — more precise, but it
makes the extracted text less faithful and also catches exponents and ordinals. Revisit if the
pilot shows real misquotes passing the lenient retry; it would bump `extractor_version`.

**D21. Agents pin the full model id and load `CLAUDE.md`.** Checked against the Claude Code
documentation (sub-agents and skills pages, 2026-10-22): agent files take `model` as an alias or a
full id, `tools` as a tool-level allow-list (Bash cannot be narrowed to one command), and
subagents load `CLAUDE.md` unless `omitClaudeMd: true`. We pin the full id (`claude-sonnet-5-5`),
so `summarised_by` records what actually ran and a model upgrade is a deliberate commit, not a
silent alias move. `CLAUDE.md` stays loaded: §10 binds agents to the whole contract, and a
separate agent contract would duplicate it (D1). Settled after the pilot: see D34.

**D22. The summariser checks its own quotes; the skill does not re-check.** The agent runs
`check_quotes.py` while it still has the source in context, which is where a failure is cheapest
to fix. A second check by the skill was judged redundant.

**D23. `summarise-pdf` takes a PDF or a folder, and never touches an existing note.** A sprint
folder is the normal unit of intake. PDFs that already have a note (found by their vault path in
`notes/20-sources/`) are flagged and skipped until the non-destructive merge exists (phase 3). A
batch of more than one PDF is shown to the contributor before any agent starts; at most three
agents run at a time. Orchestration stays in the main session rather than `context: fork`, so the
contributor sees each step and parallel agents can be launched.

**D24. Multi-page anchors are accepted.** The first pilot note (METR) cited some key claims from two
pages, `(p. 3, p. 8)`. A claim legitimately drawn from several pages lists them in one anchor —
`(p. 3, p. 8)`, `(pp. 10–12)`, `(p. 3; pp. 10–12)` — and `check_quotes.py` range-checks every page
in it. Quotes stay single-page (`(p. N)`, or `(pp. N–M)` across a break). Rejected: one anchor per
claim, which would force the summariser to drop a page the claim rests on.

**D25. The pool is decided per source, not per claim.** `claims_index.py` puts a source's claims
in the pool until any debate's `## Stances` links to that source. Intake comes in batches, and a
batch's claims are what `map-debates` places next. Rejected: matching each claim to stance lines by
page overlap (the original proposal), and stable claim IDs cited by stance lines — both more
precise, both machinery the corpus does not yet need. What is given up: once a source is in a
debate, its other claims leave the pool; `--all` puts every claim back for a full re-map.

**D26. One `mapper` agent, two modes.** The task message sets the mode. *Propose* reads
`data/pool.md` and `data/debates.md` (and `data/claims.md` when a proposal needs a source already
in a debate), writes nothing, and returns at most five proposals with stance lines in the matrix
form. *Write* drafts only the approved proposals, taking every anchor from the source note — never
from extracted text or memory. Pinned `claude-opus-5-5`, no Bash. Rejected: a separate read-only
proposer, which would enforce "writes nothing" by tool access rather than by prompt, at the cost of
a second agent file; and a proposer only, with the main session writing, which loses the clean
context. What is given up: propose mode has Write and is held read-only by its prompt alone.

**D27. Near misses are kept, not dropped.** A question the mapper finds contested but with fewer
than three sources, or with sources that do not yet disagree, goes to
`notes/90-meta/candidate-debates.md`: the question, the sources so far with anchored claims, and
what it would need to become a debate. Asked for by the contributor after the first propose run, so
the questions can be revisited as the corpus grows.

**D28. The matrix is a list per source, not a table.** `notes/90-meta/matrix.md` gives each
source a heading (with its `interest`) and one line per debate it takes a stance in: debate,
position, stance, anchor. A sources × debates table grows a column per debate and becomes
unreadable in Obsidian; the contributor chose the list. Rejected: a coded grid (debate codes as
columns, position number and symbol in cells, a legend below), which keeps the at-a-glance pattern
up to 15–20 debates at the cost of a lookup per cell. What is given up: seeing at a glance which
sources line up together across debates. Candidate debates (D27) do not enter the matrix, and the
mapper does not read them; a candidate becomes a debate only through a normal propose run.

**D29. Positions documents are organised by debate.** The contributor's brief for the pilot run:
summaries centred on debates, giving the main lines in the literature, with eras entering only
where they help explain a debate — the goal is a broad overview of the discussions pertinent to the
research questions. Candidate debates (D27) appear in `## Gaps`, one line each, not as positions.
The pilot run is a general-purpose Opus agent with the rules in its task message; whether
`positions` becomes a third `mapper` mode (as `techstack.md` assumes) or its own agent is decided
in phase 4, after the review gate.

**D30. The note format moves into `vault.py` in phase 3, not now.** Reviewing the code at the end of
the pilot found three places where the format is defined more than once: anchors are parsed by three
regexes (`check_quotes.py` strict; `claims_index.py` and `matrix.py` loose, so `(p. foo)` passes);
`## Stances` is read two ways (`claims_index.py` counts any link, `matrix.py` only the strict line);
and `matrix.py` imports `link_target` from `claims_index.py`. Also, `check_quotes.check_note` finds
quote line numbers by matching line text, because `sections()` does not keep them. The contributor
chose to leave these for phase 3, where `vault.py` becomes the owner of the note format (roadmap,
phase 3). What is accepted meanwhile: the scripts can disagree on a malformed anchor or stance line;
`matrix.py` reports a malformed stance line and exits 1, so the disagreement is not silent.

## 2026-10-27 — review gate and phase 2

**D31. Pilot findings folded into the spec.** The review gate passed (roadmap, phase 1). Changes:
- `CLAUDE.md` §2 lists `candidate-debates.md` under `notes/90-meta/`, and §3 says what goes there
  (D27 had not reached the contract).
- `CLAUDE.md` §2 describes the matrix as a list per source (D28), not a sources × debates table.
- `CLAUDE.md` §3: a source that contradicts itself has both versions recorded in
  `## Extracted facts`, attributed and unresolved. The pilot agents did this unprompted (METR
  recording counts, Work Trend Index survey date, Shen participant counts, Merola's missing
  citation); written down so a lighter model does it too.
- `url` is built as `https://arxiv.org/abs/<id>` when the source prints its own arXiv id, with the
  id as printed. Three pilot notes had empty DOI and URL with the id on page 1. This is built from
  printed text, not completed from memory (§4.1). Rejected: the arXiv DOI (`10.48550/arXiv.<id>`),
  also derivable, but `doi:` is kept to DOIs the source prints.

Deliberate non-changes:
- Inconsistent tag vocabulary in the agents' proposals: the summariser already applies only
  existing tags and proposes new ones in its report; contributors declaring tags is the fix.
- Multi-page anchors (D24) and the footnote tolerance (D20) are already in the contract and
  `check_quotes.py`.
- The mapper ran as a general-purpose agent only because its type was not yet registered in that
  session.
- The positions document's empty `question:` is expected while no question hub exists; hubs are
  the contributors'.

The contributor confirmed `interest` on the five pilot notes.

**D32. The summariser's task is described by content, not length, and in few turns.** Two changes
to `summariser.md`:
- The pilot notes landed at the top of their length target or above it; the prompt warned that a
  short note means the text was not read. The contributor is less concerned with length than
  content, and judged that a length instruction degrades the output. The agent no longer picks a
  target: its task says what the note must let a reader know without the PDF, and that length
  follows from the source. The `CLAUDE.md` §3 table stays, as the contract a reviewer checks
  against. The report keeps the word count, as a measurement.
- Every turn re-sends the agent's whole context. The agent now reads the extracted text whole in
  one call, with the template and taxonomy in the same turn, and fixes all quote failures of a
  `check_quotes.py` run in one turn. Pilot: 7–9 turns per summary, 16 for METR. Expected saving:
  ~10–15% of a summary, more on long or quote-heavy sources; the final context, and so the note,
  is unchanged. Rejected: rewriting the whole note to fix quotes (re-emits the note as output,
  the most expensive token).

**D33. Survey-instrument sources get the normal source note.** The validated scales in sprint 1
(AI anxiety, generative AI literacy, trust in AI, meta AI literacy) are summarised like any other
source. Settles the open question; a variant shape can still come with the survey specification
(roadmap, phase 7).

## 2026-10-30 — phase 2 closed, web intake

**D34. Agent tiers and contract after the pilot.** Closes phase 2.

- **Agents keep the full `CLAUDE.md`.** A shorter contract would save roughly 3k tokens per agent,
  by a word-count estimate: ~20% of what an agent starts with, ~5% of a summary's final context.
  That does not pay for a second copy of the rules, or for splitting the contract across files to
  avoid one. Rejected by the contributor as overengineering. A rule change reaches every agent
  because there is one copy.
- **Sonnet stays for summaries**, on the contributor's reading of its output in the review gate.
- **Haiku is undecided, not approved.** No Haiku agent has ever run on the corpus, so there is no
  evidence either way; the listed `haiku` tier for `checker` and `summariser-light` is a hypothesis
  (D7). Decided in phase 4 when the checker is built: plant known errors (a dropped hedge, a widened
  scope, a wrong page) in copies of a few notes and see whether it catches them.

**D35. Web intake, brought forward.** `scripts/capture_web.py` freezes a page chosen by a
contributor in `references/web/`, and `summarise-web` runs the normal `summariser` on the snapshot.
Moved ahead of phase 3 at the contributor's request; nothing in phases 3–5 was a prerequisite.
Finding sources on the web stays out of scope: every source enters because a contributor chose it.

- **`httpx` + `trafilatura`**, as in the previous project (`docs_legacy/techstack.md`). A
  user-agent naming the project, `robots.txt` respected, no browser impersonation.
- **Every non-heading block is numbered**: paragraphs, list items and table rows, each on one line.
  So `(¶ N)` can anchor anything and `(§ name)`, still allowed by `CLAUDE.md` §4.2, is rarely needed
  and is not checked. Inline markup is dropped, so a quote copied from the page matches. It gives up
  the page's visual fidelity: a snapshot is evidence, not a copy for reading.
- **Snapshots are committed**, unlike PDFs (D14): a PDF can be shared as it is, while a page can
  change or vanish, leaving the snapshot as the only evidence behind an anchor. The repository is
  private; if that changes, this decision has to be revisited, because D14's concern about
  redistribution applies to snapshots too.
- **A snapshot is never replaced.** The same text is skipped; different text is flagged and left
  alone, because anchors depend on the numbering. Replacing one is a deliberate manual act.
- **`--paste` is the one manual route** for a page that is blocked, built by JavaScript or otherwise
  fails: the contributor saves the text and it is numbered the same way, with `method: paste`.
- **Left out of the previous version**, to keep it simple: a link queue, automatic PDF download,
  dated archives of old snapshots, `--ignore-robots`, detecting single-page apps other than by word
  count (under 50 words is flagged). A URL that serves a PDF is flagged, with a pointer to
  `references/pdfs/`.
