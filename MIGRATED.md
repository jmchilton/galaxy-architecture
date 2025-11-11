# Architecture Documentation Migration

**Date Completed**: 2025-11-11

This document describes what was migrated from the Galaxy Training Network to this repository and how the migration was accomplished.

## Executive Summary

All 13 architecture topics were successfully migrated from `~/workspace/training-material/topics/dev/tutorials/` into this structured repository. The migration transforms architecture documentation from presentation slides into a single source of truth that generates multiple output formats.

### Topics Migrated (13 total)

- ecosystem
- project-management
- principles
- files
- frameworks
- dependency-injection
- tasks
- application-components
- plugins
- client
- dependencies
- startup
- production

## Migration Strategy

### Phase 1: Define Schema & Standards

Before migrating content, we established a validation schema using Pydantic v2:

**Pydantic Models** (`scripts/models.py`):
- `TopicMetadata` - Validates metadata.yaml structure
- `TrainingMetadata` - Nested training configuration
- `SphinxMetadata` - Sphinx documentation metadata
- `TopicContent` - Validates content.yaml structure
- `ContentBlock` - Individual slide/prose blocks

**Key Design Decisions**:
- Metadata separate from content (YAML + Markdown)
- Content blocks can be inline or external files
- Smart defaults: slides render in both formats, prose in docs only
- Topic sequences tracked via `previous_to`/`continues_to` chain

**Validation** (`scripts/validate.py`):
- Comprehensive checks of all topics
- Clear error messages for schema violations
- Related topic verification
- File reference validation

### Phase 2: Migrate Content Structure

Each topic extracted from GTN slides and reorganized:

**Source Format** (GTN Training Material):
```
training-material/topics/dev/tutorials/architecture-N-<topic>/
  slides.html                    # Remark.js presentation
  ../../assets/images/           # Asset images
  ../../images/                  # Topic-specific images
```

**Target Format** (this repository):
```
topics/<topic-id>/
  metadata.yaml                  # Topic configuration
  content.yaml                   # Content blocks
  .claude/
    CLAUDE.md                    # AI context for this topic
```

### Phase 3: Extract and Restructure Content

For each topic, we:

1. **Extracted slides** from HTML presentations
2. **Created metadata.yaml** with:
   - Training metadata (questions, objectives, key points, time estimation)
   - Sphinx metadata (section, subsection, level, toc_depth)
   - Hub metadata (audience, tags)
   - Related topics and code paths
   - Contributors and versioning info

3. **Created content.yaml** with:
   - One block per slide
   - Type indicator (slide vs prose)
   - Unique block ID
   - Heading from slide
   - Content as markdown

4. **Extracted footnotes** for topic sequencing:
   - Parsed navigation footnotes from last slides
   - Populated `continues_to`/`previous_to` fields
   - Established complete topic chain

5. **Copied assets**:
   - Images from `assets/` directory → `doc/source/_images/`
   - PlantUML source files (.plantuml.txt) preserved alongside SVGs
   - Topic-specific images → `images/` directory
   - Asset references updated in content

### Phase 4: Handle Remark.js Directives

The original slides used Remark.js directives for styling. We implemented smart handling:

**Handled Directives**:
- `.code[...]` - Code block styling
- `.reduce90[...]`, `.enlarge150[...]` - Layout classes
- `.pull-left[...]` / `.pull-right[...]` - Side-by-side layout
- `.footnote[...]` - Navigation footer

**Processing**:
- Speaker notes stripped per-block (removed content after `???`)
- Directives unwrapped using bracket-counting algorithm
- Pull directives converted to side-by-side with horizontal dividers
- Bracket-counting approach handles nested brackets correctly

### Phase 5: Build Output Generators

Two output formats now supported:

#### Training Slides Generator (`outputs/training-slides/build.py`)

Generates GTN-compatible Remark.js slides:

**Process**:
1. Load metadata.yaml (title, questions, objectives, key points)
2. Load content.yaml blocks
3. Filter to slide-type blocks
4. Render with Jinja2 template matching GTN style
5. Output to outputs/training-slides/generated/

**Features**:
- Dynamic metadata sections (questions, objectives, key points)
- Proper layout directives and classes
- Image integration
- Contributor attribution
- Time estimation display

#### Sphinx Documentation Generator (`outputs/sphinx-docs/build.py`)

Generates Galaxy Sphinx documentation in Markdown:

**Process**:
1. Load metadata.yaml (title, questions, objectives, key points)
2. Load content.yaml blocks
3. Filter to slide-type blocks (prose skipped in Sphinx)
4. Process markdown:
   - Strip speaker notes per-block
   - Unwrap Remark.js directives
   - Convert .pull-left/.pull-right to divider format
   - Convert image paths: `../../images/` → `../_images/`
   - Convert asset paths: `{{ site.baseurl }}/assets/images/` → `../_images/`
   - Convert bare URLs to markdown links
5. Generate learning sections (questions, objectives, key takeaways)
6. Write to doc/source/architecture/

**Advanced Features**:
- Bracket-counting algorithm for multi-line directive extraction
- Per-block speaker notes handling
- Topic ordering via `continues_to`/`previous_to` chain
- Index file generation with proper toctree ordering

### Phase 6: Establish Topic Sequencing

Topics are ordered using metadata fields:

**Chain Setup**:
```
ecosystem → project-management → principles → files
→ frameworks → dependency-injection
```

Later topics:
- tasks, application-components, plugins, client, dependencies, startup, production

**How It Works**:
- Each topic has `previous_to` (what came before) and `continues_to` (what comes next)
- Extracted from navigation footnotes in original slides
- Sphinx index follows chain: `continues_to` links
- Falls back to alphabetical if chain breaks

### Phase 7: Validate All Content

All 13 topics validate successfully:

**Validation Checks**:
- Metadata schema compliance (Pydantic v2)
- Content block structure validation
- File reference resolution
- Related topic existence
- Image file verification
- Topic chain consistency

**Command**:
```bash
make validate
# or
python scripts/validate.py
```

### Phase 8: Generated Outputs

**Training Slides**:
- Location: `outputs/training-slides/generated/`
- Can be copied to training-material repository
- Matches original GTN slide format
- All 13 topics generate successfully

**Sphinx Documentation**:
- Location: `doc/source/architecture/*.md`
- Ready for Galaxy documentation build
- Topic index with proper ordering
- All 13 topics with learning questions/objectives/key points
- Images properly linked

## Key Challenges & Solutions

### Challenge: Directive Parsing

**Problem**: Remark.js directives with nested brackets failed with simple regex.

Example: `.footnote[[Dependency Injection](url)]` - regex matched wrong closing bracket.

**Solution**: Implemented bracket-counting algorithm that:
- Tracks nesting depth
- Only closes at matching depth
- Handles multiple directives in sequence
- Works for all directive types

### Challenge: Speaker Notes

**Problem**: Initial implementation stripped notes at document level, removing all content after first `???`.

**Solution**: Moved speaker note stripping to per-block level in `generate_topic_markdown()`.

### Challenge: Directive Detection False Positives

**Problem**: Markdown links with colons in URLs (e.g., `https://`) were matched as YAML directive syntax.

**Solution**: Changed regex from `':' in line` to `^[\w_-]+:` to only match identifier-style YAML keys.

### Challenge: Multi-Footnote Extraction

**Problem**: Some slides had both informational and navigation footnotes; code only extracted first one.

**Solution**: Updated extraction loop to remove ALL footnotes from last slide, not just first.

### Challenge: Pull Directive Handling

**Problem**: Missing `import re` in `_unwrap_remark_directives()` caused NameError.

**Solution**: Added missing import; verified bracket-counting extraction works for pull directives.

### Challenge: Asset Image Paths

**Problem**: Asset images used different path than topic images.

**Solution**: Implemented separate path handling:
- `{{ site.baseurl }}/assets/images/` → `../_images/` (assets)
- `../../images/` → `../_images/` (topic images)

## Files Modified/Created

### Core Migration

| File | Purpose |
|------|---------|
| `scripts/models.py` | Pydantic v2 validation models |
| `scripts/validate.py` | Topic validation script |
| `scripts/migrate_topic.py` | Migration helper (used during initial migration) |
| `outputs/training-slides/build.py` | Slide generation |
| `outputs/training-slides/template.html` | Remark.js template |
| `outputs/sphinx-docs/build.py` | Sphinx doc generation |

### Topics (13 total)

Each topic directory contains:
- `metadata.yaml` - Configuration
- `content.yaml` - Content blocks
- `.claude/CLAUDE.md` - AI context

### Generated Outputs

| Location | Contents | Should Commit |
|----------|----------|---------------|
| `outputs/training-slides/generated/` | Built slides (HTML) | No - gitignored |
| `outputs/sphinx-docs/generated/` | Built Sphinx markdown | No - gitignored |
| `doc/source/architecture/*.md` | Sphinx output for build | Yes - this is final output |
| `doc/source/_images/` | Copied asset images | Yes - source of images |
| `images/` | Topic images & PlantUML source | Yes - source files |

## Statistics

- **Topics migrated**: 13
- **Total slides extracted**: ~150+
- **Images copied**: 40+
- **Asset files**: 10+
- **PlantUML diagrams**: 10+
- **Lines of Python**: ~500+ (build scripts)
- **Lines of YAML**: ~1000+ (metadata & content)

## What Changed

### Before
- Architecture docs locked in GTN slides (training-material repo)
- Single presentation format
- Hard to maintain across versions
- Difficult to extract for other uses
- Presentation markup mixed with content

### After
- Single source of truth in this repo
- Multiple output formats (slides, Sphinx docs, future: Hub articles)
- Easy to update: edit markdown, regenerate outputs
- Clear separation: metadata + content
- Validation ensures consistency
- Topic sequencing tracked in metadata

## Next Steps

See PLAN.md for roadmap covering:
1. Real-world usage to find pain points
2. GitHub Actions automation
3. Migration to Galaxy repository
4. Support for AI-driven knowledge base use cases
