# AI-assisted coding vault

A research knowledge base on **AI-assisted coding**, kept as an Obsidian vault versioned in git. It
supports a paper with three strands: the history of AI-assisted coding, the trends that history
points to, and a survey of how workers at a large Brazilian bank see AI in their workflows.

The vault is built by contributors working with Claude Code. The split between the two is the one
rule to keep in mind (`CLAUDE.md` §1):

- **Claude reports what a source says.** It summarises PDFs into source notes, extracts key claims
  with page anchors, maps who holds which position in a debate, and writes directed summaries when
  asked.
- **Contributors decide what it means.** Readings, connections, disagreements, which debates exist,
  which tags exist, and every review are yours. Claude writes interpretation only when you ask for
  it, and then under a `### claude` heading so it stays distinguishable from yours.

## Contents

- [Getting started](#getting-started)
- [Obsidian for this vault](#obsidian-for-this-vault)
- [Where things go](#where-things-go)
- [Literature review workflow](#literature-review-workflow)
- [Skills, agents and scripts](#skills-agents-and-scripts)
- [Working together](#working-together)
- [Further reading](#further-reading)

## Getting started

### 1. Install the tools

You need four programs. Install them once per machine.

| Tool | What it is for | Install |
|---|---|---|
| **Git** | versioning and sharing the vault | <https://git-scm.com/downloads> |
| **uv** | runs the Python scripts and manages their dependencies | see below |
| **Claude Code** | runs the skills and agents that summarise and map the literature | see below |
| **Obsidian** | reading and writing the notes | see [Installing Obsidian](#installing-obsidian) |

uv (it installs the right Python version, 3.12, by itself):

```sh
# macOS, Linux, WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Claude Code (you need a Claude account with Claude Code access; it asks you to log in on first
run):

```sh
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex
```

### 2. Get the repository and the PDFs

```sh
git clone https://github.com/iantextbar/ai_assisted_coding_vault.git
cd ai_assisted_coding_vault
```

**The PDFs are not in git** (they are large, and redistributing them is not ours to decide; D14).
Copy them from the team's shared folder into `references/pdfs/`, keeping the same subfolders — for
example `references/pdfs/sprint1/metr_productivity_2025.pdf`. The `pdf:` links in the source notes
point to these paths, so a file in a different place shows up as a broken link.

**On Windows**, clone into the Windows filesystem (for example under `C:\Users\<you>\`), even if
you run Claude Code from WSL. Obsidian is a Windows program and does not work well on a folder
inside WSL.

### 3. Set up Python

From the repository root:

```sh
uv sync                            # install the dependencies
uv run scripts/extract_pdf.py      # build data/extracted/ from your local PDFs
uv run pytest                      # offline test suite; should pass
```

Everything in `data/` is regenerated from the PDFs and the notes, so it is not in git either. Run
the extraction again whenever new PDFs arrive; PDFs that have not changed are skipped.

### 4. Open the vault in Obsidian

Follow [Installing Obsidian](#installing-obsidian) below, then open the **repository root** — the
folder that holds `CLAUDE.md` — as the vault.

### 5. Start Claude Code

From the repository root, run `claude`. It reads `CLAUDE.md`, the operating contract of the vault,
automatically. Type `/` to see the available skills.

## Obsidian for this vault

Obsidian is an editor for folders of markdown files. Each `.md` file is a note; `[[double
brackets]]` link notes to one another. There is no database and no import step: Obsidian shows the
files in the repository as they are, and every edit you make is saved straight to the file, where
git sees it.

### Installing Obsidian

1. Download Obsidian from <https://obsidian.md/download>.
   - **Windows**: run the `.exe` installer.
   - **macOS**: open the `.dmg` and drag Obsidian to Applications.
   - **Linux**: use the AppImage, or the `.deb`, Snap or Flatpak package.
2. Launch Obsidian. On the start screen, choose **Open folder as vault** and select the repository
   root — the `ai_assisted_coding_vault` folder itself, not `notes/` inside it.
3. If Obsidian asks whether you trust the author of the vault, either answer works: the vault uses
   no community plugins.
4. Check that it worked: press `Ctrl+O` (`Cmd+O` on macOS) and type `taxonomy`. The note
   `notes/90-meta/taxonomy.md` should appear. Folders such as `scripts/` and `data/` are hidden
   from search on purpose (set in `.obsidian/app.json`); that is expected.

### Recommended settings

Open Settings with the gear icon at the bottom left, or `Ctrl+,` (`Cmd+,`).

- **Templates.** Under *Core plugins*, turn on **Templates**. Then, under *Templates*, set
  *Template folder location* to `notes/90-meta/templates`. The command *Templates: Insert template*
  then fills a new note with the right frontmatter — useful for annotations and question hubs.
- **Internal links.** Under *Files and links*, turn on **Automatically update internal links**. If
  a note is ever renamed or moved, Obsidian fixes the links to it. Even so, avoid renaming notes:
  the scripts and the debates refer to them by filename.
- Leave *Excluded files* (also under *Files and links*) as it is: those entries come from the
  repository.

### The basics you will use

| To | Do |
|---|---|
| open a note by name | `Ctrl+O` / `Cmd+O` (quick switcher) |
| search all notes | `Ctrl+Shift+F` / `Cmd+Shift+F` |
| find notes with a tag | search `tag:#topic/skill-formation`, or click a tag in a note |
| switch between editing and reading view | `Ctrl+E` / `Cmd+E` |
| follow a link | click it in reading view, `Ctrl`/`Cmd`+click in editing view |
| link to a note | type `[[` and start typing its name |
| see what links to the current note | the *Backlinks* panel in the right sidebar — e.g. which debates cite a source |
| see the web of notes | `Ctrl+G` / `Cmd+G` (graph view) |
| read the PDF of a source | click the `pdf:` link in the note's properties; it opens inside Obsidian |

The block between `---` lines at the top of each note is its **frontmatter** (Obsidian calls it
*Properties* and shows it as a small table): title, authors, year, status, tags and so on. You can
edit it in place. Obsidian sometimes re-quotes values or re-indents lists when it saves; that is
normal and harmless.

### Writing in a note

The notes follow a fixed form so the scripts can read them (`CLAUDE.md` §6). When you write:

- **One paragraph is one line.** Do not press Enter in the middle of a paragraph — Obsidian wraps
  long lines on screen, and a line break you type shows up as a break when read.
- One blank line between paragraphs, headings and lists.
- Bullets with `-`.
- Write your reading under a heading with your handle (your GitHub username): `### <handle>`
  under `## Reading`.

## Where things go

| Folder | What is in it | Who writes it |
|---|---|---|
| `notes/00-questions/` | one hub per research question | contributors |
| `notes/10-debates/` | one note per contested question in the literature | Claude, after a contributor approves the debate; `## Reading` is yours |
| `notes/20-sources/` | one note per source (paper, report, post) | Claude writes the summary; `## Reading`, `## Connections`, `## Disagreements` are yours |
| `notes/30-positions/` | directed summaries of the literature's positions, written on a contributor's brief | Claude, on request; `## Reading` is yours |
| `notes/90-meta/` | generated files (`matrix.md`, `candidate-debates.md`), templates, and `taxonomy.md` | scripts and Claude — except `taxonomy.md`, which only contributors edit |
| `references/annotations/` | your own readings of a source, in your own voice | contributors; Claude only converts format and adds tags |
| `references/pdfs/<batch>/` | the PDFs (not in git) | whoever brings in the source |
| `references/web/` | numbered snapshots of web pages (committed: they are the evidence) | `scripts/capture_web.py` |
| `data/` | extracted text and claims index (not in git) | scripts |
| `scripts/`, `tests/`, `docs/` | tooling and its specification | maintained with Claude |

Two files are worth knowing early:

- `notes/90-meta/taxonomy.md` — the list of allowed tags. Claude applies tags from it but never adds
  one; when it needs a new tag, it proposes a line for you to paste there.
- `notes/90-meta/matrix.md` — where each source stands in each debate. It is generated by
  `scripts/matrix.py` from the debate notes: never edit it by hand; change the debate note instead.
- `notes/90-meta/papers-dashboard.md` — progress of the three papers in
  `30-positions/paper-ideas-evidence-map.md`: sources cited per question, own data or not,
  contributor review status, debates touched, vault growth, roadmap phases and, when
  `levantamento/dados/paper1/` exists, the external survey's per-technique counts for Paper 1.
  Generated by `uv run scripts/papers_dashboard.py` (counts only, no interpretation); regenerate it
  after changing the evidence map, the sources or the debates.

## Literature review workflow

The cycle for a batch of sources, from PDF to positions document. Steps marked *(by hand)* run in
the Claude Code session today and become skills in later phases (`docs/roadmap.md`).

```
PDFs ─► /summarise-pdf ─► source notes ─► claims index ─► mapper (propose)
                              │                               │ you approve
                              ▼                               ▼
                         you review                 mapper (write) ─► debates ─► matrix
                                                                         │
                                                         your brief ─► positions document
```

### 1. Add the PDFs

Put the batch in a new subfolder, e.g. `references/pdfs/sprint2/`, and copy it to the shared folder
so the others get the same paths. Keep filenames stable once a note links to them.

### 2. Summarise them

In Claude Code:

```
/summarise-pdf references/pdfs/sprint2
```

The skill:

1. extracts the text of each PDF with page markers (`scripts/extract_pdf.py`);
2. sets aside PDFs that already have a source note, PDFs with no text layer (scans), and PDFs above
   200 pages or 80k words;
3. shows you the batch and **waits for your yes**;
4. starts one `summariser` agent per PDF, three at a time. Each writes one note in
   `notes/20-sources/`, with key claims, and checks every quote against the extracted text;
5. reports: a table of notes, the tags the agents propose, their uncertain points, and the PDFs it
   left out and why.

A PDF set aside for size is not summarised until you act. If it is a legitimate long report, run
`uv run scripts/extract_pdf.py <path> --no-limit` and summarise it again. If it is a proceedings
volume or a book, save the chapter you need as its own PDF instead.

**Web sources** take the same route, with a URL instead of a PDF:

```
/summarise-web https://example.org/a-post
```

The skill freezes the page as a numbered snapshot in `references/web/`, then summarises the
snapshot. Anchors are `(¶ N)`, the paragraph number in the snapshot. Commit the snapshot with the
note: a page can change or disappear, and the snapshot is the evidence.

Some pages are set aside: those blocked by `robots.txt` or the server, and those built by
JavaScript, where almost no text comes out. For these, copy the page's text into a file and run
`uv run scripts/capture_web.py <url> --paste <file>`, then `/summarise-web` again. If the URL serves
a PDF, save it under `references/pdfs/` and use `/summarise-pdf`. A page that has changed since its
snapshot is flagged and the snapshot is left alone, because anchors depend on its numbering.

### 3. Review the notes

- **Tags.** Paste the proposed tags you agree with into `notes/90-meta/taxonomy.md`, then ask
  Claude to apply them.
- **Check the summary.** Read the note against the PDF where it matters. Check `source_type` and
  `interest` especially: much of the evidence on AI-assisted coding comes from the companies that
  sell the tools, and `interest: vendor` is how the vault records that. When you have checked the
  note, put your handle in `reviewed_by`.
- **Read and interpret.** Write your reading under `## Reading` → `### <handle>`, and your links
  to other notes under `## Connections` and `## Disagreements`. When you have read the source
  yourself, set `status: read` (Claude only ever sets `summarised`).
- A longer reading of your own can go in `references/annotations/`, from the `annotation`
  template, with `about: "[[source note]]"`.

### 4. Map the debates *(by hand)*

A **debate** is a question on which at least three sources land in different places. Mapping works
from the key claims, not the full notes:

```sh
uv run scripts/claims_index.py     # writes data/claims.md, data/pool.md, data/debates.md
```

Then ask Claude: *"Run the mapper agent in propose mode."* It reads the claims not yet in any
debate and returns up to five proposals — new debates, or new stances for an existing one — plus
near misses (questions with fewer than three sources). It writes nothing.

You decide. Approve, edit or drop each proposal, then ask: *"Run the mapper in write mode on
proposal 1, as approved, with this change: ..."*. Near misses you want to keep go to
`notes/90-meta/candidate-debates.md`, to revisit as the corpus grows. Then regenerate:

```sh
uv run scripts/claims_index.py
uv run scripts/matrix.py           # updates notes/90-meta/matrix.md
```

### 5. Ask for a positions document *(by hand)*

A positions document summarises the literature's positions along the lines you set. Give Claude a
brief — what is in and out, and how to organise it (by debate, by era, by stakeholder). For
example: *"Write a positions document on what the corpus says about productivity, organised by
debate."* Claude restates the brief, the debates and the sources in scope, and writes only after
you confirm. The brief is kept verbatim in the document's `## Direction`, so it can be regenerated
later as the corpus grows.

### 6. Contest your reading

Once you have written a reading, or have an idea to test, ask Claude to stress-test it:
*"Stress-test my reading in `<note>`."* Its job then is to find the strongest objection — tension
with other notes, counterexamples already in the vault, claims resting on weak evidence — not to
agree.

You can ask Claude for a reading, a set of connections or a synthesis at any time. It writes them
under `### claude`, never under your heading.

## Skills, agents and scripts

The tooling is built in phases (`docs/roadmap.md`), and not every skill exists yet.

### Skills

Run a skill by typing its name in Claude Code. Every skill proposes before it writes, and none
creates, merges or deletes a file without your confirmation.

| Skill | When to use | Status |
|---|---|---|
| `/summarise-pdf <pdf or folder>` | summarise PDFs into source notes, key claims included | **available** (draft) |
| `/summarise-web <url> [<url> ...]` | capture web pages and summarise them into source notes | **available** (draft) |
| `/new-source` | a PDF or a URL to summarise; routes it to the right path | planned, phase 4 |
| `/extract-claims` | backfill key claims in notes written without them | planned, phase 4 |
| `/map-debates` | assign new claims to debates, propose new debates; stops for approval | planned, phase 4 — use the mapper by hand meanwhile |
| `/positions` | a directed summary of the literature's positions, from your brief | planned, phase 4 — ask by hand meanwhile |
| `/stress-test` | contest a reading, or an idea brought for testing | planned, phase 4 — ask by hand meanwhile |
| `/review-links` | audit links and tags, especially after a merge | planned, phase 4 |
| `/audit` | the state of the reading debt | planned, phase 4 |
| `/refresh` | after a batch or a merge: backfill claims, then map debates | planned, phase 5 |

### Agents

Agents are the workers the skills start, each with a clean context and a fixed model. They live in
`.claude/agents/` and are bound by `CLAUDE.md` like the main session.

| Agent | Model | What it does | Status |
|---|---|---|---|
| `summariser` | Sonnet | writes one source note from one PDF's extracted text or one web snapshot, and checks its own quotes | **available**, started by `/summarise-pdf` and `/summarise-web` |
| `mapper` | Opus | *propose* mode: reads the claims pool and returns debate proposals, writing nothing; *write* mode: drafts the debates you approved | **available**, run by hand |
| `summariser-light` | Haiku (not yet tested) | short, low-argument sources | planned, phase 4 |
| `checker` | Haiku (not yet tested) | checks that key claims report their pages faithfully | planned, phase 4 |

### Scripts

Deterministic work runs in scripts, which cost no model tokens. Run them with `uv run` from the
repository root.

| Script | What it does |
|---|---|
| `scripts/extract_pdf.py [path] [--force] [--no-limit]` | PDF text, page by page, into `data/extracted/` |
| `scripts/capture_web.py <url> [--name slug] [--paste file]` | a web page's text, numbered, into `references/web/` |
| `scripts/check_quotes.py [note]` | checks that every quote appears verbatim on the page or paragraph it cites |
| `scripts/claims_index.py [--all]` | collects key claims and debates into `data/claims.md`, `pool.md`, `debates.md` |
| `scripts/matrix.py` | regenerates `notes/90-meta/matrix.md` from the debates' stances |

## Working together

Each contributor works on their own branch; `main` is the consolidated state.

```sh
git switch main && git pull
git switch -c <handle>/<topic>     # e.g. maria/sprint2-sources
# ... work ...
git add notes/ references/annotations/ references/web/
git commit -m "Summarise sprint 2"
git push -u origin <handle>/<topic>
```

Then open a pull request into `main` on GitHub.

**After every merge into `main`,** check the debates: git merges text, but it cannot tell that two
debates written on different branches ask the same question in different words. Once
`/review-links` and `/refresh` exist, run them in that order. Until then, regenerate the index and
the matrix (`claims_index.py`, `matrix.py`) and ask Claude to look for duplicate debates. Merging
two debates keeps both sides' prose and authorship (`CLAUDE.md` §4.4).

**Obsidian settings.** Only `.obsidian/app.json` is shared. Turning on a plugin or changing a
setting writes other files to `.obsidian/`; check `git status` and leave them out of your commits
unless the team agrees to share them.

## Further reading

- `CLAUDE.md` — the operating contract: what Claude does here and what it never does
- `docs/project.md` — what the project is for
- `docs/roadmap.md` — build phases, the pilot log and its review
- `docs/techstack.md` — how the tooling is built
- `docs/decisions.md` — why things are the way they are (the `D` numbers cited above)
