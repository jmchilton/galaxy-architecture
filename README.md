# Galaxy Architecture Documentation

**Experimental repository for maintaining Galaxy architecture documentation as structured content**

## Status: Proof of Concept

This repository is exploring whether maintaining architecture documentation as structured markdown + metadata (instead of presentation slides) enables:

- Multiple output formats from single source (slides, Sphinx docs, Hub articles)
- Better maintainability and consistency
- Focused Claude/AI context per topic
- Eventually: source of truth living with Galaxy code

## Quick Links

- **[PLAN.md](PLAN.md)** - Detailed implementation plan with phases, templates, and examples
- **[docs/SCHEMA.md](docs/SCHEMA.md)** - Metadata schema (to be created)
- **[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Contribution guide (to be created)

## Current Status

- ✅ Repository structure defined
- ✅ Detailed implementation plan written
- ✅ Schema definition (Phase 1)
- ⏳ First topic migration (Phase 2)
- ⏳ Slide generation (Phase 3)

## Quick Start

```bash
# Install dependencies (requires uv: https://github.com/astral-sh/uv)
uv sync

# Validate topics
uv run python scripts/validate.py

# Generate training slides for a topic
uv run python outputs/training-slides/build.py <topic-id>
```

## Structure

```
topics/                    # Content organized by architectural topic
outputs/                   # Build scripts for different formats
scripts/                   # Validation and utilities
docs/                      # Meta-documentation
.claude/                   # AI context and commands
```

## Philosophy

- Source of truth should be **clean content**, not presentation markup
- Multiple output formats should be **generated**, not manually maintained
- Documentation should live **with the code** (eventually in Galaxy repo)
- Experimentation before organization-wide adoption

## License

MIT

## Contact

John Chilton (@jmchilton)
