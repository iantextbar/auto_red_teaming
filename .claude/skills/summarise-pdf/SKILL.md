---
name: summarise-pdf
description: Summarise PDFs into source notes in notes/20-sources/, key claims included. Takes one PDF or a folder of PDFs under references/pdfs/ (e.g. a sprint folder such as references/pdfs/sprint1). Extracts the text, flags PDFs that already have a note, and runs one summariser agent per remaining PDF.
argument-hint: <pdf or folder under references/pdfs/>
---

Summarise: $ARGUMENTS

If no path was given, ask for one. Paths must be under `references/pdfs/`.

## 1. Extract

Run `uv run scripts/extract_pdf.py <paths>`. It prints one line per PDF: `extracted`, `skipped` (unchanged since the last run — fine), `flagged` or `error`. Exit code 1 only means something was flagged or failed: carry on with the rest. Flagged and failed PDFs are **not** summarised; keep them for the report with the reason the script gave.

## 2. Flag PDFs that already have a note

For each remaining PDF, search `notes/20-sources/` for its vault path, `references/pdfs/<batch>/<name>.pdf`, as a fixed string (Grep, not a regex anchored to a line start: Obsidian re-indents and re-quotes frontmatter). A match means a note already exists: that PDF is **not** summarised. Updating an existing note needs the non-destructive merge, which does not exist yet (docs/roadmap.md, phase 3). Keep it for the report with the note's path.

## 3. Confirm a batch

With a single PDF left, the request is the confirmation: go on. With more than one, show the contributor the list of PDFs to summarise (with pages and words from the extractor's output) and the PDFs excluded in steps 1–2, and wait for a yes before launching anything.

## 4. Summarise

Start one `summariser` agent per PDF, **at most three at a time** (three Agent calls in one message, then the next three when they return). The task message is the two paths and nothing else:

```
Extracted text: data/extracted/<batch>/<name>.md
PDF: references/pdfs/<batch>/<name>.pdf
```

The agent writes the note and checks its own quotes; do not re-run `check_quotes.py` here. Record each agent's token usage and duration from its completion notice.

## 5. Report

To the contributor, in this order:

1. A table: PDF · note · stated words (target) · quotes line · tokens · duration.
2. Proposed tags from all agents, deduplicated, as lines ready to paste into `notes/90-meta/taxonomy.md`. Do not write them: declaring tags is the contributors' (CLAUDE.md §4.9).
3. Uncertain points per note, as the agents reported them.
4. Excluded PDFs: flagged by the extractor (with the reason) and those that already had a note (with its path).

Do not edit the notes the agents wrote, and do not fill `## Reading`, `## Connections` or `## Disagreements`.
