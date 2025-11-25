# Galaxy Architecture Documentation - Strategic Plan

## Vision

Establish architecture documentation as a structured, multi-format knowledge base that:
- **Single source of truth** - Content updated in one place, multiple outputs generated
- **Multiple formats** - Training slides, Sphinx docs, Hub articles, AI training data
- **Knowledge base** - Topics organized for focused AI context and reasoning
- **Galaxy integration** - Eventually integrates with Galaxy's official documentation
- **Maintainable** - Clean separation of content from presentation

## Current State

✅ **Migration complete** - All 13 architecture topics extracted from GTN and restructured
✅ **Dual outputs** - Both training slides and Sphinx documentation generating successfully
✅ **GitHub Pages publishing** - Automated deployment to https://jmchilton.github.io/galaxy-architecture/
✅ **Training-material sync** - Scripts and make targets for bi-directional sync
✅ **PlantUML infrastructure** - Diagram generation from source files with mindmap YAML support
✅ **Validation** - Pydantic v2 schema ensures content quality
✅ **Topic sequencing** - Established via `previous_to`/`continues_to` metadata chain

**See MIGRATED.md** for detailed technical documentation of what was moved and how.

## Goals & Anti-Goals

### Goals
✅ Single source of truth for Galaxy architecture information
✅ Generate multiple output formats from same source
✅ Better Claude context management per architectural topic
✅ Validation and consistency checking
✅ Easy to update and maintain
✅ Eventually migrate to Galaxy proper once proven
✅ Fast iteration without organizational buy-in

### Anti-Goals
❌ Not building a CMS or complex system
❌ Not trying to replace all Galaxy documentation
❌ Not adding unnecessary tools (Obsidian, etc.)
❌ Not requiring GTN or Galaxy buy-in during POC phase
❌ Not optimizing for perfection over iteration

## Content Model

### Overview

Each topic consists of two key files:

1. **metadata.yaml** - Topic configuration (training, sphinx, hub metadata)
2. **content.yaml** - Ordered sequence of content blocks (slides and prose)

Content is stored inline in content.yaml blocks or in fragments/ directory for more granular organization.

### Validation with Pydantic

Content structure is enforced using Pydantic v2 models in `scripts/models.py`:

- **TopicMetadata** - Validates metadata.yaml structure
- **TopicContent** - Validates content.yaml structure
- **ContentBlock** - Validates individual content blocks (prose or slide)

See `docs/SCHEMA.md` (auto-generated from models) for complete schema documentation.

### Content Blocks

content.yaml defines a sequence of content blocks:

```yaml
- type: prose
  id: intro
  content: |
    Introduction text for docs only.

- type: slide
  id: problem
  heading: The Problem
  file: fragments/problem.md
```

### Smart Defaults

- **Prose blocks**: Render in docs by default, NOT in slides
- **Slide blocks**: Render in BOTH docs and slides by default

Override with explicit `doc.render: false` or `slides.render: false`.

### Content Organization

**Option 1: Inline content** (simplest)
- All content inline in content.yaml using `content: |` field
- Best for smaller blocks or single-use content
- Example: `content: | This is a slide`

**Option 2: Fragments** (more granular)
- Content split into `fragments/*.md` files
- content.yaml references with `file: fragments/problem.md` or `fragments: [problem.md, solution.md]`
- Better for large topics or reusing content across blocks

Choose based on topic complexity and content organization preferences.

## Repository Structure

```
galaxy-architecture/
│
├── README.md                      # Overview, quick start, vision
├── PLAN.md                        # This file - detailed implementation plan
├── LICENSE                        # MIT license
├── .gitignore                     # Python, build artifacts, etc.
│
├── topics/                        # Core content - one directory per topic
│   ├── dependency-injection/
│   │   ├── metadata.yaml          # Topic metadata (training, sphinx, hub config)
│   │   ├── content.yaml           # Content sequence (slides, prose blocks)
│   │   ├── fragments/             # Optional: reusable content fragments
│   │   │   └── *.md               # Fragment files (if using fragments)
│   │   └── .claude/
│   │       └── CLAUDE.md          # Topic-specific AI context
│   │
│   └── startup/
│       ├── metadata.yaml          # Topic metadata
│       ├── content.yaml           # Content sequence
│       ├── fragments/             # Optional: reusable content fragments
│       └── .claude/
│           └── CLAUDE.md
│
├── outputs/                       # Generated content (gitignored)
│   ├── training-slides/           # GTN slide generation
│   │   ├── build.py               # Builder script
│   │   ├── template.html          # Jekyll markdown template (for GTN)
│   │   └── generated/             # Output directory (.md and .html)
│   │
│   ├── sphinx-docs/               # Sphinx documentation generation
│   │   ├── build.py               # Builder script (generates Markdown)
│   │   └── generated/             # Output directory
│   │
│   └── hub-articles/              # Galaxy Hub generation (planned)
│       ├── build.py               # Builder script
│       ├── templates/             # Markdown templates
│       └── generated/             # Output directory
│
├── scripts/                       # Utility scripts
│   ├── models.py                  # Pydantic models for validation
│   ├── validate.py                # Validate all topics
│   ├── generate_schema_docs.py    # Generate SCHEMA.md from models
│   ├── sync_to_training_material.py  # Sync slides to GTN
│   ├── sync_images.py             # Sync image assets
│   ├── compare_slides.py          # Diff with training-material
│   ├── validate_sync.py           # Validate synced content
│   └── sphinx_image_linter.py     # Check Sphinx image refs
│
├── images/                        # PlantUML diagrams and mindmaps
│   ├── *.plantuml.txt             # PlantUML source files
│   ├── *.mindmap.yml              # YAML mindmap definitions
│   ├── Makefile                   # Diagram build infrastructure
│   └── mindmap_yaml_to_plantuml.py  # Converter script
│
├── doc/                           # Sphinx project
│   ├── source/                    # Source RST/MD (includes generated)
│   └── build/html/                # Built HTML (published to GitHub Pages)
│
├── .claude/                       # Repository-level Claude context
│   ├── CLAUDE.md                  # Overall repo context
│   └── commands/                  # Claude slash commands
│       ├── sync-slides.md         # Generate slides for a topic
│       ├── validate-topic.md      # Validate single topic
│       ├── validate-all.md        # Validate all topics
│       └── new-topic.md           # Scaffold new topic
│
├── docs/                          # Meta-documentation
│   ├── SCHEMA.md                  # Metadata schema specification
│   ├── CONTRIBUTING.md            # How to add/update content
│   ├── OUTPUTS.md                 # How output generation works
│   ├── MIGRATION.md               # Plan for eventually moving to Galaxy
│   ├── GITHUB_PAGES_QUICKSTART.md # GitHub Pages setup guide
│   └── GITHUB_PAGES_SETUP.md      # Technical deployment details
│
└── .github/workflows/             # CI/CD configuration
    ├── validate.yml               # Validation on PRs
    └── deploy-docs.yml            # GitHub Pages deployment
```

## Strategic Initiatives

### 0. GitHub Pages Publishing (Completed ✅)

**Goal**: Automatically build and publish documentation on every commit

**Status**: Fully implemented and operational

**Implementation**:
- GitHub Actions workflow: `.github/workflows/deploy-docs.yml`
- Triggers on push to main branch
- Builds: PlantUML diagrams → training slides → Sphinx docs
- Publishes to: https://jmchilton.github.io/galaxy-architecture/
- Includes: All 13 topics, embedded slide presentations, full-text search

**Documentation**:
- Setup: `docs/GITHUB_PAGES_QUICKSTART.md`
- Technical: `docs/GITHUB_PAGES_SETUP.md`

**Outcome**: Documentation is always up-to-date with latest commits

### 1. Keep Training Material in Sync (Completed ✅)

**Goal**: Automatically sync generated slides back to training-material repository

**Status**: Fully implemented with scripts and make targets

**Implementation**:
- `scripts/sync_to_training_material.py` - Main sync script
- `scripts/sync_images.py` - Sync image assets (SVG/PNG only)
- `scripts/compare_slides.py` - Diff with training-material
- `scripts/validate_sync.py` - Post-sync validation
- Make targets: `make sync-to-training`, `make compare-slides`
- Navigation footnotes added during sync (not in source)

**Workflow**:
1. Update content in this repo
2. Run `make build-slides` to generate
3. Run `make compare-slides` to preview changes
4. Run sync script to copy to ~/workspace/training-material
5. Review diff and commit in training-material

**Benefits Achieved**:
- Single source of truth maintained
- Clean separation: base slides here, GTN-specific nav in sync
- Audit trail of all changes
- Validation prevents broken syncs

### 2. Sphinx Documentation (Completed ✅)

**Goal**: Full integration with documentation publishing

**Status**: Fully implemented and published to GitHub Pages

**Implementation**:
- Generates Markdown from content.yaml
- Builds Sphinx HTML with embedded Remark.js slides
- Publishes automatically via GitHub Actions
- Live at: https://jmchilton.github.io/galaxy-architecture/

**Features Working**:
- All 13 topics rendering correctly
- Embedded slide presentations work
- PlantUML diagrams display properly
- Cross-references and navigation working
- Full-text search enabled
- Image paths correct for all contexts

**Next Phase**: Integration into Galaxy's main docs (future)

### 3. AI Knowledge Base

**Goal**: Use this repository as structured training data for agentic AI work

**Vision**:
- Each topic has focused context (.claude/CLAUDE.md)
- Topics linked via previous_to/continues_to chain
- Clear separation of concerns
- Enough prose for AI to understand relationships

**Current State**:
- 13 topics with metadata and content
- Basic AI context per topic
- Topic sequencing established
- Content organized and validated

**Remaining Work**:
- Add more prose to topics (currently mostly slide content)
- Create better AI context files
- Establish patterns for how AI should reason about architecture
- Test with agentic workflows

**Next Steps**:
1. Identify topics that need more prose
2. Write extended explanations for each topic
3. Create cross-topic linking documentation
4. Test with Claude on architecture questions

### 4. Long-term Migration to Galaxy

**Goal**: Eventually integrate this into Galaxy's main repository

**Timeline**:
- **Phase 1 (Now)**: Maintain as experimental repo, prove value
- **Phase 2 (Months)**: Use for real architecture updates, gather feedback
- **Phase 3 (Later)**: When proven, move topics/ into Galaxy at doc/source/architecture/
- **Phase 4 (Final)**: Integrate builds into Galaxy CI/CD, deprecate old slides

**Requirements**:
- Stable schema and tooling
- Clear contribution guidelines
- Working automation
- Buy-in from Galaxy maintainers

**Success Criteria**:
- Multiple real-world updates show system works
- No regressions in documentation quality
- Community finds it valuable
- Integration is straightforward

---

## Implementation Status

### Completed ✅

- [x] Migration of all 13 topics from training-material
- [x] Pydantic v2 validation schema
- [x] Training slide generation (outputs/training-slides/)
- [x] Sphinx documentation generation (outputs/sphinx-docs/)
- [x] Topic sequencing (previous_to/continues_to chain)
- [x] Asset image copying and path conversion
- [x] Remark.js directive handling
- [x] Documentation (SCHEMA.md, CONTRIBUTING.md, MIGRATION.md, etc.)
- [x] **PlantUML/mindmap diagram infrastructure**
- [x] **GitHub Pages publishing with automated deployment**
- [x] **Training-material sync scripts and make targets**
- [x] **Sphinx build verified and published**
- [x] **Image linting and validation**

### In Progress 🔄

- [ ] Add more prose content to topics (beyond slide content)
- [ ] Create enhanced AI context files (.claude/CLAUDE.md per topic)
- [ ] Test agentic AI workflows with structured content

### Future Phases 📋

- [ ] Hub article generation (outputs/hub-articles/)
- [ ] Integration into Galaxy repository (doc/source/architecture/)
- [ ] Support for additional documentation types
- [ ] Community contribution guidelines and workflows

---

## Detailed Implementation History

For detailed technical documentation of how the migration was accomplished, including:
- Phase-by-phase breakdown of implementation
- Challenges encountered and solutions
- Code examples and architecture decisions
- Statistics and technical details

**See [MIGRATED.md](MIGRATED.md)**

This document focuses on the strategic plan going forward. Implementation details are in MIGRATED.md for reference.
