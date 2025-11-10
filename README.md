# Galaxy Architecture Documentation

**Source of truth for Galaxy architecture documentation - generates multiple output formats**

## Overview

This repository maintains Galaxy architecture knowledge as structured content (markdown + metadata) and generates multiple output formats:

- **Training Slides** - GTN-compatible Remark.js slides for architecture tutorials
- **Sphinx Docs** - Planned for Galaxy documentation (Phase 9)
- **Hub Articles** - Planned for galaxyproject.org

## Why This Exists

Architecture knowledge was previously locked in presentation slides within the GTN repository. This creates several problems:

- ❌ Single format limitation (hard to reuse for docs/articles)
- ❌ Maintenance burden (editing presentation markup)
- ❌ Poor AI context (monolithic slides)
- ❌ Wrong location (docs should live with code)

**Solution**: Structured content that generates multiple formats, eventually living in the Galaxy repository.

## Quick Links

- **[PLAN.md](PLAN.md)** - Detailed implementation plan with phases and progress
- **[docs/SCHEMA.md](docs/SCHEMA.md)** - Complete metadata schema documentation
- **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Guide for adding/updating topics
- **[docs/OUTPUTS.md](docs/OUTPUTS.md)** - Output format documentation
- **[docs/MIGRATION.md](docs/MIGRATION.md)** - Long-term migration plan

## Current Status

- ✅ **Phase 0-1**: Repository structure and schema defined
- ✅ **Phase 2**: First topic migrated (dependency-injection)
- ✅ **Phase 3**: Slide generator complete with all features
- ✅ **Phase 4**: Validation framework with CI integration
- ⏳ **Phase 5-6**: Additional topics and Claude integration (skipped for now)
- ✅ **Phase 7**: Documentation complete
- ⏳ **Phase 8-9**: Real-world usage and Sphinx output (future)

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

### Common Tasks

```bash
# Validate all topics
uv run python scripts/validate.py

# Generate training slides for a topic
uv run python outputs/training-slides/build.py dependency-injection

# Run tests
uv run pytest tests/ -v

# View generated slides
open outputs/training-slides/generated/architecture-dependency-injection/slides.html
```

### Example: Adding a New Topic

```bash
# 1. Create topic directory
mkdir -p topics/my-topic/.claude

# 2. Create metadata.yaml (see docs/SCHEMA.md)
# 3. Create overview.md with content
# 4. Create .claude/CLAUDE.md for context

# 5. Validate
uv run python scripts/validate.py

# 6. Generate slides
uv run python outputs/training-slides/build.py my-topic
```

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed instructions.

## Repository Structure

```
galaxy-architecture/
├── topics/                 # Content organized by architectural topic
│   └── dependency-injection/
│       ├── metadata.yaml  # Structured metadata
│       ├── overview.md     # Main content
│       ├── examples.md     # Code examples
│       └── .claude/
│           └── CLAUDE.md   # AI context
├── outputs/               # Build scripts for different formats
│   └── training-slides/
│       ├── build.py       # Slide generator
│       ├── template.html  # GTN template
│       └── generated/     # Output directory
├── scripts/               # Validation and utilities
│   └── validate.py       # Content validation
├── tests/                 # Test suite
│   └── test_validate.py   # Validation tests
├── docs/                  # Meta-documentation
│   ├── SCHEMA.md         # Metadata schema
│   ├── CONTRIBUTING.md   # Contribution guide
│   ├── OUTPUTS.md        # Output format docs
│   └── MIGRATION.md      # Migration plan
├── images/                # Shared images (PlantUML diagrams)
└── .github/workflows/     # CI configuration
    └── validate.yml       # Validation workflow
```

## Features

### ✅ Implemented

- **Structured Content**: Markdown + YAML metadata per topic
- **Slide Generation**: GTN-compatible Remark.js slides
- **Validation Framework**: Automated quality checks
- **CI Integration**: GitHub Actions for validation and testing
- **Image Management**: Shared image directory with PlantUML support
- **Layout Classes**: Support for `reduce90`, `enlarge150` classes
- **Code Formatting**: `.code[]` wrapper and diff format support

### ⏳ Planned

- **Sphinx Output**: Generate Galaxy documentation (Phase 9)
- **Hub Articles**: Generate galaxyproject.org articles
- **Claude Commands**: AI-assisted workflows (Phase 6)
- **Navigation Footer**: Previous/next tutorial links (Issue #1)

## Philosophy

- **Clean Content First**: Source of truth is markdown, not presentation markup
- **Generate, Don't Maintain**: Multiple formats from single source
- **Co-location**: Documentation should live with code (migration planned)
- **Validation**: Automated checks ensure quality and consistency
- **Iteration**: Experiment and improve before organizational adoption

## Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for:
- How to add new topics
- Content style guidelines
- Testing and validation
- Pull request process

## Migration Plan

Long-term goal: Move into Galaxy repository. See [docs/MIGRATION.md](docs/MIGRATION.md) for:
- Migration strategy
- Prerequisites
- Integration plan
- Timeline estimates

## License

MIT

## Contact

John Chilton (@jmchilton)
