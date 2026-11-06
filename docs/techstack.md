# techstack.md — libraries, scripts, agents and skills

## Runtime

- **Python ≥ 3.12**, managed by [`uv`](https://docs.astral.sh/uv/).
- No service, database or daemon. Scripts are one-off invocations that read and write files.

## Libraries

| Library | For | Why this one |
|---|---|---|
| `pymupdf` | extracting text and metadata from PDFs, page by page | fast, no external binary, and returns the page number with the text — exactly the anchor quotes need |
| `httpx` | fetching web pages | explicit timeout and size limit, content type visible before extracting, and `MockTransport` so tests never touch the network |
| `trafilatura` | extracting a page's main text from HTML | drops menus, ads and footers; returns author, date and outlet in the same pass; emits markdown |
| `python-frontmatter` | reading and writing note YAML | leaves the markdown body intact; hand-written YAML handling breaks on some edge case sooner or later |
| `pytest` | tests | — |
| `ruff` | lint and format | one fast binary |

Runtime dependencies (`pymupdf`, `python-frontmatter`, `httpx`, `trafilatura`) go in
`[project.dependencies]`; `pytest` and `ruff` in a dev group. `pymupdf` is pinned below 2.0 (D18).

**Network.** `capture_web.py` is the only script that touches the internet (D35). Tests make no
real request. The user-agent names the project honestly and does not imitate a browser,
`robots.txt` is respected, and a request has a 30 s timeout and a 10 MB limit. A site that blocks
the capture is pasted by hand (`--paste`), never worked around.

## Design

### Pure transformation, thin I/O

Each script has a **pure transformation function** and a thin I/O layer around it:

```
input (text, dict)  ──►  transform()  ──►  result (dataclass)  ──►  write()
                         pure, testable                              touches disk
```

Tests exercise the transformation with literal inputs — no fixture files where a string will do, no
temporary vault where a dict will do, and never the network.

### Scripts

| Script | Reads | Writes | Purpose |
|---|---|---|---|
| `scripts/vault.py` | — | — | shared module; every other script goes through it to touch a note |
| `scripts/extract_pdf.py` | `references/pdfs/**` | `data/extracted/<mirrored path>.md` | per-page text with page markers |
| `scripts/capture_web.py` | a URL, or a pasted file | `references/web/<slug>.md` | a page's text frozen as a numbered snapshot (D35) |
| `scripts/check_quotes.py` | source notes, `data/extracted/`, `references/web/` | report (stdout) | verbatim check of quotes and anchors |
| `scripts/claims_index.py` | source notes, debate notes | `data/claims.md`, `data/pool.md`, `data/debates.md` | the compact index corpus-level work reads |
| `scripts/matrix.py` | debate notes | `notes/90-meta/matrix.md` | each source's stances across the debates, listed per source (D28) |
| `scripts/audit.py` | the whole vault | `notes/90-meta/audit.md` | review debt (later phase) |

#### `vault.py`

- `read_note(path) -> Note` / `write_note(note)` — via `python-frontmatter`.
- `slug(title)` — deterministic, so the same source always resolves to the same file.
- `sections(body) -> dict[str, str]` — splits markdown by `##`, preserving order and content.
- `source_key(note)` — source identity, by order of confidence: **DOI** (canonical `10.xxxx/...`,
  extracted from a bare DOI or a `doi.org` link) → **normalised URL** (no scheme, `www.`, trailing
  slash, fragment or tracking parameters) → **normalised title + year**. The same normalisation
  serves deduplication and filenames, so the two cannot diverge.
- **`merge_non_destructive(existing, new) -> Note`** — the central rule, defined in one place:
  - an empty mechanical frontmatter field is filled; a filled one is left alone (a human may have
    corrected it);
  - `reviewed_by` is never touched; `status` is never moved, except `to-read` → `summarised`;
  - mechanical sections (`## Stated by the source`, `## Extracted facts`, `## Quotes`) are updated;
  - interpretive sections (`## Reading`, `## Connections`, `## Disagreements`) are never touched.

#### `extract_pdf.py`

- Writes one markdown file per PDF, mirroring the folder structure of `references/pdfs/` — a flat
  destination lets two same-named PDFs from different folders overwrite each other, and one note
  would then cite `(p. N)` from the other.
- Each page is preceded by a marker carrying the **physical** page index (1 = first page of the
  file), which is what `(p. N)` anchors cite and what Obsidian's `[[file.pdf#page=N]]` opens. When
  the PDF carries a page label that differs, the marker records it too:
  `<!-- page 5 | printed 1127 -->` (D15).
- The text is written as `pymupdf` returns it; all normalisation (ligatures, hyphenation, quote
  characters) happens in `check_quotes.py`, so the extracted file stays a faithful copy.
- A YAML header records the source path, a content hash, page and word counts and the extractor
  version; an output whose hash and version both match is skipped unless `--force`.
- Flags instead of extracting: PDFs with no text layer — under 50 words in the whole document;
  would need OCR, not planned — and PDFs above **200 pages or 80k words** (a whole proceedings
  volume is not a paper). `--no-limit` overrides (D16). A PDF with text but some blank pages (a
  cover image, a partial scan) is extracted, and the blank pages are listed in the header's
  `empty_pages`.
- Output mirrors `references/pdfs/`: `references/pdfs/sprint2/x.pdf` →
  `data/extracted/sprint2/x.md`. `parse_pages()` reads an extracted file back into `{page: text}`,
  so the marker format is defined in one module.

#### `capture_web.py`

- Writes one markdown file per page to `references/web/<slug>.md`, committed to git (D35). The slug
  comes from `--name`, the page title or the URL, in that order.
- The YAML header carries `url`, `title`, `author`, `date`, `sitename`, `captured`, `method`
  (`fetch` | `paste`), `sha256` (of the numbered text), `paragraphs`, `words` and
  `extractor_version`.
- `number_blocks()` puts every non-heading block on one line and prefixes `[¶ N]`, in document
  order: paragraphs, list items and table rows. Inline markup is dropped so that quotes match.
  `parse_paragraphs()` reads a snapshot back into `{paragraph: text}`, so the format is defined in
  one module.
- Flagged, with nothing written: disallowed by `robots.txt`, an HTTP error, a PDF response, a
  response over 10 MB, or under 50 words of text. `--paste FILE` is the manual route, except for a
  PDF, which belongs in `references/pdfs/`.
- A snapshot is never replaced: the same `sha256` is skipped, a different one is flagged and the
  file left alone. Replacing one is a deliberate manual act, because `(¶ N)` anchors depend on it.

#### `check_quotes.py`

- For every bullet in `## Quotes`, checks that the quoted text appears **verbatim** on the cited
  page of the extracted text, or in the cited paragraph of the snapshot for a note with `snapshot:`
  and no `pdf:`, after normalising whitespace, line-break hyphenation, ligatures and quote
  characters.
- Checks that every `(p. N)` or `(¶ N)` anchor in the note points to a page or paragraph that
  exists. `(§ name)` anchors are not checked.
- `...`, `…` and `[...]` mark gaps: the fragments must appear in order. `(pp. N–M)` is accepted.
- Reports per note: verified; *tolerated* — matched only with footnote markers ignored, or running
  onto the next page (D20); not found on the cited page (and where it was found); not found at
  all; malformed line; anchor out of range. Exits 1 on any failure.
- It **cannot** check paraphrase. Whether a key claim faithfully reports its page is a semantic
  question, and belongs to the `checker` agent.

#### `claims_index.py`

- Collects every `### Key claims` bullet into `data/claims.md`: claim · source · anchor.
- Groups claims by source, with the source's `source_type` and `interest` in the group header.
- A source is *in a debate* when any debate's `## Stances` links to it; the decision is per source,
  not per claim (D25).
- Writes `data/pool.md`, the claims of sources not yet in any debate (`--all`: every claim), and
  `data/debates.md`, a one-line index of existing debates (question + positions). These two files
  are all `map-debates` needs to start from.
- A key claim without an anchor is reported and left out; exits 1 on any such problem.

#### `matrix.py`

- Parses `## Stances` lines of the form
  `- [[source note]] · <position> · supports | contests | qualifies · (p. N)`.
- A line that does not match the form is an **error**, reported with file and line — never silently
  dropped.
- A position that is not a `###` heading under the debate's `## Positions` is also an error.
- Writes `notes/90-meta/matrix.md`: one list per source, headed by its `interest`, with a line per
  debate it takes a stance in — debate, position, stance, anchor. A list, not a table, so the file
  stays readable as debates grow (D28).

### Obsidian's YAML normalisation

Obsidian rewrites frontmatter on save: single quotes become double, and list items are re-indented
(`- x` becomes `  - x`). Every piece of code that reads frontmatter must tolerate both forms. In the
previous project a regex anchored at column 0 made notes **silently disappear** from a generated
index after someone opened them in Obsidian. Rule: read frontmatter with `python-frontmatter`, never
by regex.

### Note form in generated output

Text the scripts write into `notes/` follows `CLAUDE.md` §6: one paragraph per line, one list item
per line, no hard wrap. A string split across two lines of code must not become two lines of
markdown. `CLAUDE.md`, `docs/` and `README.md` keep the 100-column wrap.

## Agents

Defined in `.claude/agents/`, one file each, with the model pinned in the file:

| Agent | Model | Job | Returns |
|---|---|---|---|
| `summariser` | sonnet | one source → one full source note, key claims included; key-claims backfill | short report |
| `summariser-light` | haiku | one short, low-argument source → one note | short report |
| `checker` | haiku | semantic check: does each key claim (or debate position) match its cited page? | list of mismatches |
| `mapper` | opus | *propose* mode: `map-debates` proposals, read-only by prompt; *write* mode: the approved debates (D26). Drafting positions documents: decided in phase 4 (D29) | proposal or written debates |

**Agents draft; the main session decides.** A subagent cannot stop mid-run to ask a contributor for
approval. So anything `CLAUDE.md` puts behind approval — a new debate, a debate update, a positions
document — comes back from the agent as a proposal or draft. The main session shows it to the
contributor, gets the answer, and applies the writes. A summary the contributor asked for is written
by the summariser directly: the request is the confirmation.

Agent files pin the **full model id** (`model: claude-sonnet-5-5`), allow-list their tools
(leaving out `Agent`, so they cannot spawn agents of their own) and cap `maxTurns`. Subagents load
`CLAUDE.md`, the whole file (D21, D34). The `haiku` tier above is a hypothesis until phase 4 (D34).

## Skills

Defined in `.claude/skills/`, one folder each. `CLAUDE.md` §9 is the list; here, what each one
drives:

| Skill | Drives |
|---|---|
| `new-source` | router: PDF → `summarise-pdf`; URL → `summarise-web` |
| `summarise-pdf` | a PDF or a folder: `extract_pdf.py`, flag PDFs that already have a note, then one `summariser` agent per PDF (which runs `check_quotes.py` itself) |
| `summarise-web` | one or more URLs: flag URLs that already have a note, `capture_web.py`, then one `summariser` agent per snapshot |
| `extract-claims` | the `summariser` agent in backfill mode, reading the note and the extracted text |
| `map-debates` | `claims_index.py`, then the `mapper` agent; approval in the main session; then `matrix.py` |
| `refresh` | counts sources missing claims, asks, runs `extract-claims` in parallel, then `map-debates` |
| `positions` | restates the brief for confirmation, then an Opus agent drafts from `data/` and the debates — `mapper` or its own agent, decided in phase 4 (D29) |
| `review-links` | broken wikilinks, orphan notes, tags absent from the taxonomy, duplicate debates |
| `audit` | `audit.py` |
| `stress-test` | main session; no agent, because it is a conversation |

`CLAUDE.md` §3 is the single source for the note format. Skills do not repeat it; each keeps only
what is specific to its job.

## Guarded properties

These are the tests that matter; the rest is detail:

1. **Idempotence** — running `extract_pdf.py`, `capture_web.py`, `claims_index.py` or `matrix.py`
   twice produces no diff.
2. **Deduplication** — same DOI → one note; without a DOI, same URL up to tracking parameters and
   trailing slash → one note; without either, same title and year → one note.
3. **Non-destructiveness** — a note with `## Reading` written, `status: read` and `reviewed_by` set
   survives any script intact.
4. **Frontmatter round-trip** — reading and rewriting a note without changing it does not change a
   byte of the body.
5. **Quote checking** — an altered quote and a quote on the wrong page or paragraph are both
   caught; ligatures and line-break hyphenation do not cause false alarms.
6. **Stance format** — a malformed stance line fails loudly with file and line.
7. **Obsidian tolerance** — re-indented YAML lists parse the same as unindented ones.
8. **No network** — `uv run pytest` passes offline.
9. **Snapshot stability** — the same text gets the same `[¶ N]` numbering, and a changed page never
   overwrites an existing snapshot.

## Tools

- `uv run pytest` — tests, with temporary vaults in `tmp_path` where a vault is needed.
- `uv run ruff check` / `uv run ruff format` — lint and format.
- Scripts run directly: `uv run scripts/extract_pdf.py`.
