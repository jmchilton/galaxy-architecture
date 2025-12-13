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
  - content.yaml (narrative content)
  - .claude/CLAUDE.md (topic-specific context)
- `outputs/` - Build scripts for different formats
- `scripts/` - Validation and utilities
- `doc/` - Sphinx project for this content.
- `docs/` - Meta-documentation

## Key Files

- **PLAN.md** - Detailed implementation plan with all phases, templates, examples
- **docs/SCHEMA.md** - Auto-generated schema documentation from Pydantic models
- **Makefile** - Top-level build targets (validate, build-slides, build-sphinx, etc.)
- **scripts/models.py** - Pydantic v2 models for validation (metadata.yaml, content.yaml)
- **scripts/validate.py** - Topic validation script
- **scripts/generate_schema_docs.py** - Auto-generates docs/SCHEMA.md from models
- **outputs/training-slides/build.py** - Generates GTN-compatible slides
- **outputs/sphinx-docs/build.py** - Generates Sphinx markdown with URL conversion
- **images/MERMAID.md** - Mermaid diagram support documentation (PlantUML vs Mermaid usage guide)

## Common Tasks

### Add new topic
1. Create `topics/<topic-id>/` directory
2. Create metadata.yaml from schema
3. Write content.yaml and other content files
4. Add .claude/CLAUDE.md for topic context
5. Validate: `make validate`

### Update existing topic
1. Edit markdown files in `topics/<topic-id>/`
2. Update metadata.yaml if needed
3. Validate and regenerate outputs

### Generate training slides
```bash
make build-slides
```

### Generate Sphinx documentation
```bash
make build-sphinx
```

### Validate all content
```bash
make validate
```

### Sync to training-material
```bash
# Compare slides with training-material
make compare-slides

# Dry-run sync (shows what would change)
make sync-to-training

# Actually sync
uv run python scripts/sync_to_training_material.py --all

# Validate sync
make validate-sync
```

### Build everything
```bash
make build
```

### Build diagrams
```bash
# Build all PlantUML and Mermaid diagrams
make images

# Watch for diagram source changes
make watch-images
```

See **images/MERMAID.md** for details on PlantUML vs Mermaid diagram types and usage.

## Content Model

Each topic is defined by three files:

1. **metadata.yaml** - Topic configuration (training, sphinx, hub metadata)
   - Learning questions, objectives, key points
   - Audience, target level, time estimation
   - Related topics and code paths

2. **content.yaml** - Ordered sequence of content blocks
   - Each block: type (prose/slide), id, heading, content source
   - Smart defaults: prose renders in docs only; slides render everywhere
   - Content from inline, single file, or multiple fragments

3. **fragments/** - Actual content (optional for granular organization)
   - Slides defined with markdown (supports code, images, blockquotes)
   - Can use single fragment per block or multiple fragments per block

All content validated with Pydantic v2 models before build.

## Build Artifacts

- **outputs/training-slides/generated/** - GTN-compatible Remark.js slides
- **outputs/sphinx-docs/generated/architecture/** - Markdown for Sphinx
- **doc/source/architecture/** - Markdown copied for local Sphinx build
- **doc/build/html/** - Built HTML documentation (published to GitHub Pages)

## Current Topics

- **dependency-injection** - How Galaxy uses DI patterns

## Output Formats

1. **Training slides** - GTN-compatible Remark.js slides (outputs/training-slides/generated/)
2. **Sphinx docs** - Markdown for Galaxy Sphinx documentation (outputs/sphinx-docs/generated/)
3. **GitHub Pages** - Published HTML documentation at https://jmchilton.github.io/galaxy-architecture/
4. **Hub articles** - Markdown for galaxyproject.org (planned)

## Publishing

Documentation is automatically built and published to GitHub Pages on every push to main:
- See **docs/GITHUB_PAGES_QUICKSTART.md** for initial setup
- See **docs/GITHUB_PAGES_SETUP.md** for technical details
- Workflow: `.github/workflows/deploy-docs.yml`
- Published URL: https://jmchilton.github.io/galaxy-architecture/

## Implementation Status

See PLAN.md for detailed phases.

## Slash Commands

### /research-topic <topic-id>
Research a topic using its metadata to prepare for content generation.
- Loads metadata.yaml, creates `notes/` directory
- For each `related_code_paths`: examines code, writes summary to `notes/path_<path>.md`
- For each `related_pull_requests`: fetches PR via gh CLI, writes summary + diff to `notes/pr_<org>_<repo>_<num>.md`
- Supports string and object formats for paths/PRs

### /research-find-code-paths <topic-id>
Extract relevant code paths from PR diffs and add to metadata.
- Reads `.diff` files from `notes/`
- Identifies 8-12 architecturally significant paths (managers, APIs, core components)
- Verifies paths exist in `~/workspace/galaxy`
- Appends to `related_code_paths` in metadata.yaml
- Requires: run `/research-topic` first

### /plan-a-topic <topic-id>
Generate structured slide plan by analyzing research notes.
1. Validates prerequisites (metadata.yaml, notes/ with path_*.md and pr_*.md)
2. Spawns two parallel agents:
   - **Code-based plan**: slides from architecture/implementation → `plan/code_based_plan.md`
   - **PR-based plan**: slides from evolution/history → `plan/pr_based_plan.md`
3. Merges into 3 flow options (Architecture-First, Evolution-First, Hybrid) → `plan/merged_plan.md`
4. Prompts user for flow choice, duration, audience level
5. Creates `plan/final_plan.md` with chosen flow and next steps
- Requires: run `/research-topic` first

## When helping with this repo

- Follow the PLAN.md phases
- Validate before committing
- Keep tooling simple
- Document pain points for iteration
