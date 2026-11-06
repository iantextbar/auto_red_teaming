---
name: summarise-web
description: Summarise web pages into source notes in notes/20-sources/, key claims included. Takes one or more URLs a contributor chose. Freezes each page as a numbered snapshot in references/web/, flags pages that already have a note, and runs one summariser agent per remaining page.
argument-hint: <url> [<url> ...]
---

Summarise: $ARGUMENTS

If no URL was given, ask for one.

## 1. Flag URLs that already have a note

For each URL, search `notes/20-sources/` for it as a fixed string (Grep, not a regex anchored to a line start: Obsidian re-indents and re-quotes frontmatter). A match means a note already exists: that URL is **not** summarised, and **not** captured. Updating an existing note needs the non-destructive merge, which does not exist yet (docs/roadmap.md, phase 3). Keep it for the report with the note's path.

## 2. Capture

For each remaining URL, run `uv run scripts/capture_web.py <url>`. It prints one line: `extracted` (with the snapshot's name, paragraphs and words), `skipped` (a snapshot with this text exists: use it, the line names it), `flagged` or `error`. Exit code 1 only means something was flagged or failed: carry on with the rest. Flagged and failed pages are **not** summarised; keep them for the report with the reason the script gave.

Never work around a flag. A page blocked by `robots.txt` or by the server, or one built by JavaScript, is for the contributor to paste: they save the page's text to a file and run `uv run scripts/capture_web.py <url> --paste <file>`. A snapshot flagged as changed stays as it is; replacing it is the contributor's decision, because `(¶ N)` anchors depend on it.

## 3. Confirm a batch

With a single page left, the request is the confirmation: go on. With more than one, show the contributor the list to summarise (with paragraphs and words from the capture output) and the pages excluded in steps 1–2, and wait for a yes before launching anything.

## 4. Summarise

Start one `summariser` agent per page, **at most three at a time** (three Agent calls in one message, then the next three when they return). The task message is the snapshot path and nothing else:

```
Snapshot: references/web/<name>.md
```

The agent writes the note and checks its own quotes; do not re-run `check_quotes.py` here. Record each agent's token usage and duration from its completion notice.

## 5. Report

To the contributor, in this order:

1. A table: URL · snapshot · note · stated words (target) · quotes line · tokens · duration.
2. Proposed tags from all agents, deduplicated, as lines ready to paste into `notes/90-meta/taxonomy.md`. Do not write them: declaring tags is the contributors' (CLAUDE.md §4.9).
3. Uncertain points per note, as the agents reported them.
4. Excluded pages: flagged by the capture (with the reason and the `--paste` route when it applies) and those that already had a note (with its path).

The new snapshots are committed along with the notes: they are the evidence behind the anchors. Do not edit the notes the agents wrote, and do not fill `## Reading`, `## Connections` or `## Disagreements`.
