# project.md — what this project is

## What it is

A research knowledge base on **AI-assisted coding**, kept as an Obsidian vault versioned in git. It
supports a paper with three strands:

1. **History** — how AI assistance in programming developed, from early program synthesis to
   today's coding agents.
2. **Trends and future patterns** — the directions the literature takes and the positions it holds
   on where this is going.
3. **Survey** — a questionnaire validating the view of workers at a large Brazilian bank on the use
   of AI in their workflows.

The vault is fed by:

- **PDFs** of papers and reports, added by contributors to `references/pdfs/`;
- **web sources** (blog posts, vendor reports, documentation), frozen as snapshots in
  `references/web/` by `scripts/capture_web.py`;
- **the contributors' own annotations** — readings, ideas and conclusions in their own voice.

There is no external literature-review pipeline. Every source enters because a contributor chose
it.

The operating contract for Claude is `CLAUDE.md`. It is the project's constitution: the rules live
there and only there. This file says what the project is for; `techstack.md` says how the tooling
is built; `roadmap.md` says in what order; `decisions.md` says why, and what was rejected.

## Goals

- **Substantive intake.** A new source becomes a note that informs on its own: the argument in
  prose, the works it argues with, facts and quotes with verifiable anchors, and a handful of key
  claims. Not a skeleton to fill later.
- **Links between papers that survive volume.** Papers are linked through **debates** — contested
  questions with the positions taken, who holds each, and why they differ — so that the hundredth
  source is as easy to place as the tenth.
- **Writing material for the paper.** Directed **positions documents** summarise the literature's
  positions under a brief a contributor gives: topics in and out, lens (by era, by debate, by
  stakeholder), research question served.
- **Visible authorship and review.** Who wrote what, and which model, is recorded inside each file;
  what no human has reviewed yet is always listable.
- **Token-efficient operation.** Deterministic work runs in scripts; model tiers are pinned in the
  repository, so cheaper models do the work they are fit for without anyone switching models by
  hand.

## Non-goals

- **Outsourcing judgement.** Summaries must inform by themselves — a summary too short to use
  protects no one. What stays with the contributors is judgement: what the evidence is worth, what
  it implies, which side of a debate is right.
- **A reference manager.** Metadata sufficient to cite, not a replacement for Zotero.
- **Atomic concept notes.** The previous project generated one-idea-per-note concepts. They came out
  one or two lines long, multiplied without limit, were extracted one paper at a time and so rarely
  linked papers. What proved useful was the large summary of positions across the literature. Key
  claims, debates and positions documents replace concepts.

## Users and division of work

**Contributors** — several researchers. They author all interpretation and approve every debate.
Each works on their own branch and merges into `main`.

**Claude** — extraction, mapping, drafting on request, and stress-testing, under `CLAUDE.md`.

The central design constraint is cognitive, not organisational: a pipeline that hands over finished
judgement produces a vault nobody understands. The line separates **reporting** from **judging**,
not short from long.

| Layer | Author | Content |
|---|---|---|
| Extraction | Claude | metadata, N, method, population, measured effects, anchored quotes |
| Stated by the source | Claude | what it is about, the argument in prose, interlocutors, methodology, findings, what it offers, limitations, key claims |
| Debates | Claude proposes, contributor approves | contested questions, positions, who holds each, why they differ, stances |
| Positions documents | Claude, on request, under a contributor's brief | the literature's positions, organised by the requested lens |
| Interpretation | contributors | what the evidence is worth, what it implies, what it conflicts with |
| Stress-testing | Claude | tension between notes, counterexamples, claims without strong evidence |

Interpretation on explicit request is legitimate work for Claude — it just never happens in passing.

## Survey strand

The survey is a separate track with its own specification, to be written when the work reaches it
(`roadmap.md`, phase 7). It has to settle at least: the instrument and how it is versioned; how
responses are collected and anonymised under the LGPD; where anonymised data lives and what never
enters the repository; and how the survey's questions connect to the debates mapped from the
literature.

## Directory structure

```
/
├── CLAUDE.md                  operating contract (the constitution)
├── README.md                  entry point
├── docs/                      project, techstack, roadmap, decisions
├── .claude/
│   ├── skills/                project skills
│   └── agents/                subagent definitions, with pinned models
├── notes/
│   ├── 00-questions/          one hub per research question
│   ├── 10-debates/            one note per contested question
│   ├── 20-sources/            one note per source
│   ├── 30-positions/          directed summaries of positions
│   └── 90-meta/               taxonomy, audit, generated matrix, candidate debates, templates
├── references/
│   ├── annotations/           contributors' readings, in their own voice
│   ├── pdfs/                  PDFs
│   └── web/                   web snapshots (evidence, versioned)
├── data/                      extracted text, claims index (derived)
├── scripts/                   tooling
└── tests/                     tests for the scripts
```

The Obsidian vault is the **repository root**, not `notes/` — that is what lets a source note link
straight to its PDF and open it inside Obsidian. `data/`, `scripts/`, `docs/` and `tests/` are
hidden from Obsidian's search through `userIgnoreFilters`.

The numeric prefixes in `notes/` only fix the order in the file explorer: questions on top, then
debates, sources, positions, and metadata last.
