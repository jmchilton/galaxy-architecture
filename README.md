# Galaxy Architecture Documentation

**Source of truth for Galaxy architecture documentation - generates multiple output formats**

## Overview

This repository maintains Galaxy architecture knowledge as structured content (markdown + metadata) and generates multiple output formats:

- **Training Slides** - GTN-compatible Remark.js slides for architecture tutorials
- **Sphinx Docs** - Published at https://jmchilton.github.io/galaxy-architecture/
- **Training Material Sync** - Back-sync to training-material repository
- **Hub Articles** - Planned for galaxyproject.org

## Published Documentation

**Live site**: https://jmchilton.github.io/galaxy-architecture/

The documentation is automatically built and published to GitHub Pages on every push to `main`. Includes:
- Sphinx HTML documentation for all 16 architecture topics
- Embedded Remark.js slide presentations
- PlantUML diagrams and mindmaps
- Full-text search and navigation

See [docs/GITHUB_PAGES_QUICKSTART.md](docs/GITHUB_PAGES_QUICKSTART.md) for setup details.

## Why This Belongs in Galaxy

### Code is cheap; understanding is the bottleneck

With coding agents, 4,000-line Galaxy PRs are now routine - all four below landed or opened in 2026. Reviewers still have to understand them. The design knowledge those reviews need lives in maintainers' heads and in PR descriptions that vanish into history at merge. Recent PRs show it:

- **[#22513](https://github.com/galaxyproject/galaxy/pull/22513), Server-Sent Events (+5.2k lines, 77 files).** The first review: "nothing is too scary other than just the vastness of how much of it I don't understand but wish I did", asking for the admin and architecture story. The author had it already, in private markdown files: "I am still iterating on how it'll look like in the end and where to put these." The author also noted "it's so cheap these days to explore alternative architectures." After merge: "We really do need a place to capture this architecture stuff close to the code."
- **[#22860](https://github.com/galaxyproject/galaxy/pull/22860), notebook workflow extraction (+4.2k lines, 40 files).** The design is an 841-line PR description. Once merged, nothing links it to the code it explains.
- **[#23676](https://github.com/galaxyproject/galaxy/pull/23676), subworkflow mapping (+4.3k lines).** Its own author writes: "***I just don't understand this PR***. I don't know how to make it understandable."
- **[#22752](https://github.com/galaxyproject/galaxy/pull/22752), History Graph UI (+4.6k lines, 84 files).** Review leaned on an AI assistant ("My Claude caught...", "Claude thinks this watch is redundant"). Assistants review as well as the context they get, and today Galaxy gives them no architecture docs to read.

Architecture docs in the repository answer all four: reviewers get a map, authors get a place to put the design story, and coding agents get context that is versioned with the code they change.

This is not a Galaxy quirk. In 2026:

- "We made writing cheap, and understanding stayed exactly as expensive as it has always been." Review now means "reconstructing intent that never got written down, which is harder and slower." — Addy Osmani, [Agentic Code Review](https://addyosmani.com/blog/agentic-code-review/) (June 2026)
- "Comprehension debt is the growing gap between how much code exists in your system and how much of it any human being genuinely understands." — Addy Osmani, [Comprehension Debt](https://addyosmani.com/blog/comprehension-debt/) (March 2026)
- "Delivering new code has dropped in price to almost free... but delivering good code remains significantly more expensive than that." Good code is "documented at an appropriate level, and that documentation reflects the current state of the system." — Simon Willison, [Writing code is cheap now](https://simonwillison.net/guides/agentic-engineering-patterns/code-is-cheap/) (February 2026)
- Teams found "the theory of the system, their shared understanding, had fragmented or disappeared entirely"; "velocity without understanding is not sustainable." — Margaret-Anne Storey, [Cognitive Debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/) (February 2026)
- "Many of the things we advocate for developers also enable LLMs to work more effectively too." — Martin Fowler, [Fragments: February 13](https://martinfowler.com/fragments/2026-02-13.html) (February 2026)
- Of Ghostty's agent context file: "Each line in that file is based on a bad agent behavior, and it almost completely resolved them all." — Mitchell Hashimoto, [My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey) (February 2026)

### The gap

Galaxy's developer docs have no architecture reference. `doc/source/dev/index.rst`, `CONTRIBUTING.md` and `doc/source/dev/writing_tests.md` link to a GTN slides URL that now redirects to the first of 16 decks. Core subsystems - dependency injection, Celery tasks, app startup, repository layout, client build, Galaxy Markdown - have no dedicated dev-doc page.

The goal of this repository is to move that content into `galaxyproject/galaxy`:

- **Versioned with the code.** docs.galaxyproject.org already builds per release, so architecture pages would describe the release you run, and a PR that changes the architecture can update its docs in the same diff.
- **Checked against the code.** Topics name the files they describe (`related_code_paths`, file-structure mindmaps). Inside Galaxy, a test can fail when those paths move; out here, ~40 went stale unnoticed.
- **No new tooling.** Galaxy's Sphinx build already uses `myst_parser` and `sphinx_rtd_theme`, already generates pages from YAML at build time (`doc/gen_authoring_doc.py`), and already commits rendered PlantUML SVGs. These pages render unchanged under Galaxy's pins, with no Java or Node in docs CI.
- **One source, GTN still served.** Reference prose lives in Sphinx; GTN slides are exported from the same source, so the two stop drifting apart.
- **More than one maintainer.** Today this is a single-author repository outside the org; in Galaxy, subsystem owners review the topics for their code.

**Didn't Galaxy try this before?** Yes: Remark architecture slides lived in `doc/source/slideshow/` from 2016 (galaxyproject/galaxy#2244) until 2019, when they were removed because GTN hosted them. That was a second copy of a slideshow with its own HTML/JS toolchain. This is reference prose Galaxy lacks, built by Galaxy's existing Sphinx setup, with GTN remaining the home for slides.

**Why not generate diagrams with a tool like [Archify](https://github.com/tt-a1i/archify)?** Archify is impressive: an agent writes a typed JSON spec, and a deterministic renderer turns it into a polished, interactive diagram with source links pinned to a commit. But it does not fit how Galaxy distributes docs. Galaxy docs are text in the repository, built by Sphinx per release branch into static HTML on docs.galaxyproject.org, read as plain Markdown on GitHub, and reused as static images in GTN Remark slides. Archify's output is an ~800 KB self-contained HTML app per diagram, with no command-line export to SVG. That renders in none of those places (at best an iframe in Sphinx), would add a Node toolchain to docs CI, and bloats the repository across dozens of diagrams. Its node positions are hand-placed coordinates, so reviewers would diff numbers rather than meaning. Its "verified source" badges only check that a file and line range exist, not that the diagram is right. PlantUML text next to a committed SVG, the pattern `doc/source/dev/` already uses, diffs cleanly and renders everywhere. Archify's authoring rules (at most ~12 nodes, one main path, detail in cards) are worth borrowing. The tool is not.

## Quick Links

- **[Published Documentation](https://jmchilton.github.io/galaxy-architecture/)** - Live Sphinx docs with embedded slides
- **[docs/SCHEMA.md](docs/SCHEMA.md)** - Complete metadata schema documentation
- **[docs/GITHUB_PAGES_QUICKSTART.md](docs/GITHUB_PAGES_QUICKSTART.md)** - GitHub Pages publishing setup
- **[docs/GITHUB_PAGES_SETUP.md](docs/GITHUB_PAGES_SETUP.md)** - Technical deployment details

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) - Modern Python package manager

### Setup

```bash
# Clone repository
git clone https://github.com/jmchilton/galaxy-architecture.git
cd galaxy-architecture

# Install dependencies
uv sync

# Install dev dependencies (for tests)
uv sync --extra dev
```

### External Checkouts

Some targets need other repositories. Point these environment variables at local clones:

| Variable | Repository | Used by |
|---|---|---|
| `GALAXY_ROOT` | galaxyproject/galaxy | `make validate-files`, `/research-find-code-paths` |
| `GTN_ROOT` | galaxyproject/training-material | `make compare-slides`, `make sync-to-training`, `make validate-sync` |

Scripts also accept `--galaxy-root` / `--training-material-root`.

### Build Targets

```bash
# Validate all topics and metadata
make validate

# Verify file references in mindmaps exist in $GALAXY_ROOT
make validate-files

# Build PlantUML diagrams from source
make images

# Generate training slides
make build-slides

# Generate Sphinx documentation
make build-sphinx

# Build everything (validates + generates all outputs)
make build

# View local Sphinx site
make view-sphinx

# Compare with training-material
make compare-slides

# Sync to training-material (dry-run)
make sync-to-training

# Watch and rebuild on changes
make watch

# Clean generated files
make clean
```

### Example: Adding a New Topic

```bash
# 1. Create topic directory
mkdir -p topics/my-topic

# 2. Create metadata.yaml (see docs/SCHEMA.md for schema)
# 3. Create content.yaml with content blocks
# 4. Optionally create fragments/ for granular content organization

# 5. Validate
make validate

# 6. Generate outputs
make build

# 7. View locally
make view-sphinx
```

See [docs/SCHEMA.md](docs/SCHEMA.md) for the metadata and content.yaml schema.

## Repository Structure

```
galaxy-architecture/
├── topics/                     # 16 architectural topics
│   └── ecosystem/
│       ├── metadata.yaml       # Topic metadata (training, sphinx)
│       ├── content.yaml        # Ordered content blocks
│       └── fragments/          # Optional: granular content files
├── outputs/
│   ├── training-slides/
│   │   ├── build.py           # Generates Remark.js slides
│   │   ├── template.html      # Jekyll markdown template (for GTN)
│   │   └── generated/         # Generated slides (.md and .html)
│   └── sphinx-docs/
│       ├── build.py           # Generates Sphinx markdown
│       └── generated/         # Generated Sphinx content
├── doc/                        # Sphinx project
│   ├── source/                # Source files (incl. generated)
│   └── build/html/            # Built site (published to GitHub Pages)
├── scripts/
│   ├── validate.py            # Content validation
│   ├── models.py              # Pydantic schemas
│   ├── sync_to_training_material.py  # Sync slides to GTN
│   ├── sync_images.py         # Sync image assets
│   └── compare_slides.py      # Diff with training-material
├── images/                     # PlantUML diagrams and mindmaps
│   ├── *.plantuml.txt         # PlantUML source files
│   ├── *.mindmap.yml          # YAML mindmap definitions
│   └── Makefile              # Diagram build rules
├── docs/                      # Documentation
│   ├── SCHEMA.md             # Auto-generated from Pydantic models
│   ├── GITHUB_PAGES_QUICKSTART.md
│   └── GITHUB_PAGES_SETUP.md
└── .github/workflows/
    ├── validate.yml          # CI validation
    └── deploy-docs.yml       # GitHub Pages deployment
```

## Features

### ✅ Implemented

- **16 Architecture Topics**: Ecosystem, project management, principles, files, frameworks, DI, tasks, components, plugins, client, dependencies, startup, production, file sources, markdown, tests
- **Structured Content**: `metadata.yaml` + `content.yaml` with content blocks
- **Slide Generation**: GTN-compatible Remark.js slides (Jekyll markdown + standalone HTML)
- **Sphinx Documentation**: Published to GitHub Pages with embedded slides
- **GitHub Pages**: Automated deployment on push to main
- **PlantUML Diagrams**: Build infrastructure for architecture diagrams and mindmaps
- **Training-Material Sync**: Scripts to sync slides back to training-material repo
- **Validation Framework**: Pydantic v2 models with file reference checking
- **CI Integration**: Automated validation and deployment
- **Layout Classes**: Support for `reduce90`, `enlarge150`, `code[]` wrappers
- **Navigation**: Previous/next footnotes generated during sync

### ⏳ Planned

- **Hub Articles**: Generate galaxyproject.org articles
- **Galaxy Repo Migration**: Move content into main Galaxy repository

## Agentic Code Review

Architecture documentation enables **agentic code review** - generating AI-powered review commands from architectural knowledge.

### The Plugin Marketplace

The `review/` directory builds the `claude-galaxy-plugins` marketplace containing slash commands for reviewing Galaxy contributions. Commands come from two sources:

- **Static commands**: Hand-written review prompts (`review/static_commands/`)
- **Generated commands**: Created from architecture topics via `/generate-agentic-op`

Build and use:
```bash
cd review && make
claude --plugin-dir review/galaxy-plugins
/gx-arch-review:gx-review <pr-or-commit>
```

Or install from GitHub:
```bash
/plugin marketplace add galaxyproject/claude-galaxy-plugins
/plugin install gx-arch-review@claude-galaxy-plugins
```

See [review/galaxy-plugins/README.md](review/galaxy-plugins/README.md) for full marketplace documentation.

### The Feedback Loop

Architecture documentation, agentic commands, and code reviews form a **positive feedback loop**:

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   ┌──────────────────┐         ┌──────────────────┐                │
│   │   Architecture   │────────▶│ Agentic Commands │                │
│   │  Documentation   │         │   (gx-review)    │                │
│   └────────▲─────────┘         └────────┬─────────┘                │
│            │                            │                          │
│            │                            ▼                          │
│   ┌────────┴─────────┐         ┌──────────────────┐                │
│   │   Suggestions    │◀────────│   Code Reviews   │                │
│   │ (topic/suggests/)│         │                  │                │
│   └──────────────────┘         └──────────────────┘                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Documentation → Commands**: Generating agentic commands from architecture docs produces `suggestions/` files identifying documentation gaps. If a topic lacks detail to produce a useful review command, that's signal to improve the docs.

**Commands → Reviews**: Better architecture documentation yields more comprehensive review commands that catch more issues.

**Reviews → Documentation**: When agentic reviews miss something a human reviewer catches, this reveals gaps in architecture documentation. The missed pattern should be documented, improving future command generation.

This virtuous cycle means:
- Every documentation improvement makes reviews better
- Every review gap improves documentation
- The system self-improves through use

### Slash Commands

| Command | Source | Description |
|---------|--------|-------------|
| `/generate-agentic-op` | Built-in | Generate review command from topic |
| `/gx-arch-review:gx-review` | Plugin | Orchestrator - runs applicable sub-reviews |
| `/gx-arch-review:gx-review-di` | Generated | Dependency injection patterns |
| `/gx-arch-review:gx-review-business-logic-organization` | Generated | Controller/Service/Manager layers |
| `/gx-arch-review:py-challenge-patches` | Static | Mock/patch quality in tests |
| `/gx-arch-review:gx-vitest-review` | Static | Vue/TypeScript test review |

See `review/galaxy-plugins/plugins/gx-arch-review/README.md` for the complete command list.

## Ongoing Maintenance

Regular tasks to keep the repository healthy:

### File Reference Validation

The `make validate-files` target verifies that all file paths referenced in file-structure mindmaps (`images/*files*.mindmap.yml`) exist in `$GALAXY_ROOT`. This ensures documentation stays in sync with the actual codebase.

**When to run:**
- Before committing changes to mindmap files
- When Galaxy repository is updated with new/moved files

**What it checks:**
- All entries in `images/*files*.mindmap.yml` (except `...` placeholders) exist in the Galaxy checkout
- Reports missing files with their mindmap source
- Returns non-zero exit code if any files are missing

**Common workflow:**
```bash
# Update a mindmap file
# Run validation
make validate-files

# If there are missing files, either:
# 1. Update the mindmap to reference correct files
# 2. Remove/document obsolete file references

# Commit with validated mindmaps
git add images/
git commit -m "Update architecture mindmaps"
```

## Contributing

To add or update topics:
1. Review [docs/SCHEMA.md](docs/SCHEMA.md) for metadata and content structure
2. Create/edit `metadata.yaml` and `content.yaml` in topic directory
3. Run `make validate` to check for errors
4. Run `make build` to generate all outputs
5. Submit pull request

## Migration Plan

1. Stabilize and simplify this repository (in progress).
2. Refresh stale topics; restructure pages to read as reference docs rather than slides.
3. Propose to Galaxy: a first batch of topics under `doc/source/dev/architecture/` plus a code-path existence test.
4. Export GTN slides from Galaxy; redirect this site to docs.galaxyproject.org and archive the repository.

## License

MIT

## Contact

John Chilton (@jmchilton)
