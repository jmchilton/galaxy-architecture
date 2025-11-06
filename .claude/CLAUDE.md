# Galaxy Architecture Documentation Repository

This repository maintains source of truth for Galaxy architecture docs and generates multiple output formats.

## Repository Purpose

Experimental POC to prove that maintaining architecture content as structured markdown + metadata enables:
- Multiple output formats (slides, Sphinx docs, Hub articles)
- Better maintainability
- Focused AI context per topic
- Eventually: migrate to Galaxy repo

## Structure

- `topics/` - One directory per architectural topic, each contains:
  - metadata.yaml (structured data)
  - *.md files (narrative content)
  - .claude/CLAUDE.md (topic-specific context)
- `outputs/` - Build scripts for different formats
- `scripts/` - Validation and utilities
- `docs/` - Meta-documentation

## Key Files

- **PLAN.md** - Detailed implementation plan with all phases, templates, examples
- **docs/SCHEMA.md** - Metadata schema specification (to be created)
- **docs/CONTRIBUTING.md** - How to add/update content (to be created)

## Common Tasks

### Add new topic
1. Create `topics/<topic-id>/` directory
2. Create metadata.yaml from schema
3. Write overview.md and other content files
4. Add .claude/CLAUDE.md for topic context
5. Validate: `python scripts/validate.py`

### Update existing topic
1. Edit markdown files in `topics/<topic-id>/`
2. Update metadata.yaml if needed
3. Validate and regenerate outputs

### Generate training slides
```bash
python outputs/training-slides/build.py <topic-id>
```

### Validate all content
```bash
python scripts/validate.py
```

## Current Topics

- **dependency-injection** - How Galaxy uses DI patterns (planned)
- **startup** - Application startup sequence (planned)

## Output Formats

1. **Training slides**: GTN-compatible Remark.js slides (Phase 3)
2. **Sphinx docs**: RST for Galaxy documentation (Phase 9)
3. **Hub articles**: Markdown for galaxyproject.org (future)

## Implementation Status

See PLAN.md for detailed phases. Currently in Phase 0 (bootstrap).

## When helping with this repo

- Follow the PLAN.md phases
- Validate before committing
- Keep tooling simple (no Obsidian integration)
- Document pain points for iteration
