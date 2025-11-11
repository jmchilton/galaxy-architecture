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
│   │   ├── template.html          # Remark.js template
│   │   └── generated/             # Output directory
│   │
│   ├── sphinx-docs/               # Galaxy docs generation (planned)
│   │   ├── build.py               # Builder script (generates Markdown)
│   │   └── generated/             # Output directory
│   │
│   └── hub-articles/              # Galaxy Hub generation
│       ├── build.py               # Builder script
│       ├── templates/             # Markdown templates
│       └── generated/             # Output directory
│
├── scripts/                       # Utility scripts
│   ├── models.py                  # Pydantic models for validation
│   ├── validate.py                # Validate all topics
│   ├── generate_schema_docs.py    # Generate SCHEMA.md from models
│   ├── list-topics.py             # List all topics and status
│   ├── check-links.py             # Verify internal references
│   └── preview.py                 # Local preview server
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
│   └── MIGRATION.md               # Plan for eventually moving to Galaxy
│
└── tests/                         # Validation tests
    ├── test_metadata.py           # Test metadata validity
    ├── test_content.py            # Test content formatting
    └── test_builds.py             # Test output generation
```

## Strategic Initiatives

### 1. Keep Training Material in Sync

**Goal**: Automatically sync generated slides back to training-material repository

**Approach**:
- Build system that detects changes in topics/
- Automatically regenerates training slides via outputs/training-slides/build.py
- Creates PRs or copies to ~/workspace/training-material/
- Keeps GTN training material in sync without manual intervention

**Benefits**:
- Single source of truth in this repo
- Training slides auto-updated
- No need to maintain dual copies
- Clear audit trail of what changed

**Next Steps**:
1. Establish copy/sync workflow (local script first)
2. Test with single topic update
3. Eventually GitHub Actions for automated sync

### 2. Enhance Sphinx Output for Galaxy Integration

**Goal**: Full integration with Galaxy's documentation system

**Current State**:
- Generates Markdown successfully
- All 13 topics rendering
- Proper image paths and formatting
- Topic ordering working

**Remaining Work**:
- Test build with `cd doc && make html`
- Verify all images display correctly
- Check cross-references and links
- Add prose content to flesh out topics
- Consider formatting for Galaxy's doc style

**Next Steps**:
1. Build Sphinx locally to validate output quality
2. Fix any rendering issues discovered
3. Add additional prose sections if needed
4. Plan integration into Galaxy/doc/

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
- [x] Documentation (SCHEMA.md, CONTRIBUTING.md, MIGRATION.md)

### In Progress 🔄

- [ ] Verify Sphinx build quality (test with `make html`)
- [ ] Add prose content to topics
- [ ] Create enhanced AI context files
- [ ] Build automation workflow (copy slides to training-material)

### Future Phases 📋

- [ ] GitHub Actions for validation and preview
- [ ] Automated slide sync to training-material
- [ ] Hub article generation
- [ ] Integration into Galaxy repository
- [ ] Support for additional documentation types

---

## Detailed Implementation History

For detailed technical documentation of how the migration was accomplished, including:
- Phase-by-phase breakdown of implementation
- Challenges encountered and solutions
- Code examples and architecture decisions
- Statistics and technical details

**See [MIGRATED.md](MIGRATED.md)**

This document focuses on the strategic plan going forward. Implementation details are in MIGRATED.md for reference.
