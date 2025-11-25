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
- Sphinx HTML documentation for all 13 architecture topics
- Embedded Remark.js slide presentations
- PlantUML diagrams and mindmaps
- Full-text search and navigation

See [docs/GITHUB_PAGES_QUICKSTART.md](docs/GITHUB_PAGES_QUICKSTART.md) for setup details.

## Why This Exists

Architecture knowledge was previously locked in presentation slides within the GTN repository. This creates several problems:

- ❌ Single format limitation (hard to reuse for docs/articles)
- ❌ Maintenance burden (editing presentation markup)
- ❌ Poor AI context (monolithic slides)
- ❌ Wrong location (docs should live with code)

**Solution**: Structured content that generates multiple formats, eventually living in the Galaxy repository.

## Quick Links

- **[Published Documentation](https://jmchilton.github.io/galaxy-architecture/)** - Live Sphinx docs with embedded slides
- **[PLAN.md](PLAN.md)** - Detailed implementation plan with phases and progress
- **[docs/SCHEMA.md](docs/SCHEMA.md)** - Complete metadata schema documentation
- **[docs/GITHUB_PAGES_QUICKSTART.md](docs/GITHUB_PAGES_QUICKSTART.md)** - GitHub Pages publishing setup
- **[docs/GITHUB_PAGES_SETUP.md](docs/GITHUB_PAGES_SETUP.md)** - Technical deployment details
- **[BACK_TO_TRAINING_PLAN.md](BACK_TO_TRAINING_PLAN.md)** - Sync strategy to training-material

## Current Status

- ✅ **Phase 0-4**: Core infrastructure, validation, and slide generation
- ✅ **Phase 5**: All 13 architecture topics migrated from training-material
- ✅ **Phase 7**: PlantUML/mindmap diagram infrastructure
- ✅ **Phase 8**: Sphinx documentation with GitHub Pages publishing
- ✅ **Phase 9**: Training-material back-sync infrastructure
- ⏳ **Phase 10**: Hub articles and Galaxy repo integration (future)

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

### Build Targets

```bash
# Validate all topics and metadata
make validate

# Verify file references in mindmaps exist in ~/workspace/galaxy
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
├── topics/                     # 13 architectural topics
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

- **13 Architecture Topics**: Ecosystem, project management, principles, files, frameworks, DI, tasks, components, plugins, client, dependencies, startup, production
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

## Philosophy

- **Clean Content First**: Source of truth is markdown, not presentation markup
- **Generate, Don't Maintain**: Multiple formats from single source
- **Co-location**: Documentation should live with code (migration planned)
- **Validation**: Automated checks ensure quality and consistency
- **Iteration**: Experiment and improve before organizational adoption

## Ongoing Maintenance

Regular tasks to keep the repository healthy:

### File Reference Validation

The `make validate-files` target verifies that all file paths referenced in architecture mindmaps exist in `~/workspace/galaxy`. This ensures documentation stays in sync with the actual codebase.

**When to run:**
- Before committing changes to mindmap files
- When Galaxy repository is updated with new/moved files
- As part of CI/CD pipeline

**What it checks:**
- All files in `images/*.mindmap.yml` files exist in Galaxy repo
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

Long-term goal: Move into Galaxy repository for co-location with code. Current approach:
- Content maintained in this repo as single source of truth
- Slides synced to training-material via `make sync-to-training`
- Sphinx docs published to GitHub Pages
- Future: Integrate into Galaxy's main documentation

## License

MIT

## Contact

John Chilton (@jmchilton)
