# Galaxy Architecture Documentation - Implementation Plan

## Context & Background

### The Problem

Galaxy architecture knowledge is currently locked in presentation slides within the Galaxy Training Network (GTN) repository. These slides serve as training material but also attempt to be the source of truth for Galaxy's architecture documentation. This creates several issues:

1. **Wrong home** - Architecture docs should live with Galaxy code, not in training materials
2. **Single format limitation** - Content trapped in Remark.js slides, hard to reuse for Sphinx docs, Hub articles, or other formats
3. **Maintenance burden** - Updating architecture info requires editing presentation markup instead of clean content
4. **Poor Claude context** - Large monolithic slides make it hard for AI to be an expert on specific topics
5. **Political overhead** - Can't experiment freely in repositories you don't fully control

### The Solution

Create an experimental repository that:
- Treats architecture knowledge as structured content (markdown + metadata)
- Generates multiple output formats (slides, Sphinx docs, Hub articles)
- Uses topic-based organization for focused Claude context
- Lives independently during proof-of-concept phase
- Can eventually migrate into Galaxy's documentation once proven

### Key Decisions Made

- **Repository**: `github.com/jmchilton/galaxy-architecture`
- **License**: MIT (matching Galaxy's direction)
- **Location**: `~/workspace/galaxy-architecture`
- **Initial Topics**: dependency-injection, startup (complex and important topics)
- **Output Targets**: GTN slides (immediate), Galaxy Sphinx docs (next), Hub articles (future)
- **No Obsidian**: Keep tooling simple - just markdown, YAML, Python, Git

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
│   │   ├── metadata.yaml          # Structured metadata for all outputs
│   │   ├── overview.md            # Main narrative content
│   │   ├── examples.md            # Code examples and patterns
│   │   ├── testing.md             # How to test DI patterns
│   │   └── .claude/
│   │       └── CLAUDE.md          # Topic-specific AI context
│   │
│   └── startup/
│       ├── metadata.yaml
│       ├── overview.md
│       ├── sequence.md            # Startup sequence details
│       ├── configuration.md       # Config loading
│       └── .claude/
│           └── CLAUDE.md
│
├── outputs/                       # Generated content (gitignored)
│   ├── training-slides/           # GTN slide generation
│   │   ├── build.py               # Builder script
│   │   ├── template.html          # Remark.js template
│   │   └── generated/             # Output directory
│   │
│   ├── sphinx-docs/               # Galaxy docs generation
│   │   ├── build.py               # Builder script
│   │   ├── templates/             # RST templates
│   │   └── generated/             # Output directory
│   │
│   └── hub-articles/              # Galaxy Hub generation
│       ├── build.py               # Builder script
│       ├── templates/             # Markdown templates
│       └── generated/             # Output directory
│
├── scripts/                       # Utility scripts
│   ├── validate.py                # Validate metadata completeness
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

## Implementation Phases

## Progress Summary

**Last Updated**: 2025-01-15

### ✅ Completed Phases

**Phase 0: Repository Bootstrap** - Complete
- Repository initialized with git remote configured
- Directory structure created (topics/, outputs/, scripts/, tests/, docs/, .claude/)
- LICENSE, .gitignore, and README.md in place
- Initial commit completed

**Phase 1: Define Schema & Standards** - Complete
- `docs/SCHEMA.md` - Full metadata schema documentation created
- `docs/CONTRIBUTING.md` - Contributing guidelines written
- `topics/dependency-injection/metadata.yaml` - Example metadata file created
- `scripts/validate.py` - Validation script implemented with comprehensive checks
- Python project structure set up with `uv` (pyproject.toml, dependencies managed)
- All documentation updated to use `uv` instead of `pip`

**Phase 2: Migrate First Topic** - Complete
- Extracted content from GTN slides (`~/workspace/training-material/topics/dev/tutorials/architecture-6-dependency-injection/slides.html`)
- Created overview.md, examples.md, testing.md content files matching actual slides
- Created .claude/CLAUDE.md for topic-specific AI context
- Updated metadata.yaml with correct questions, objectives, and key points from slides
- Validated all content structure successfully
- Content accurately reflects Galaxy's type-based DI with Lagom (not generic PasteScript-style)

### 🔄 Next Phase

**Phase 8-9: Real-World Usage & Sphinx Output** - Future work
- Use system for actual architecture updates
- Gather feedback and iterate
- Build Sphinx documentation generator
- Integrate with Galaxy docs structure

---

### Phase 0: Repository Bootstrap (Day 1) ✅ COMPLETE

**Goal**: Get basic repo structure in place

**Tasks**:

1. **Initialize repository**
   ```bash
   cd ~/workspace/galaxy-architecture
   git init
   git remote add origin git@github.com:jmchilton/galaxy-architecture.git
   ```

2. **Create LICENSE file**
   ```
   MIT License

   Copyright (c) 2025 John Chilton

   Permission is hereby granted, free of charge, to any person obtaining a copy...
   [full MIT license text]
   ```

3. **Create .gitignore**
   ```
   # Python
   __pycache__/
   *.py[cod]
   *$py.class
   *.so
   .Python
   env/
   venv/

   # Build outputs
   outputs/*/generated/

   # IDE
   .vscode/
   .idea/
   *.swp
   *.swo

   # OS
   .DS_Store
   ```

4. **Create initial README.md** (see template below)

5. **Create directory structure**
   ```bash
   mkdir -p topics/{dependency-injection,startup}/.claude
   mkdir -p outputs/{training-slides,sphinx-docs,hub-articles}/{templates,generated}
   mkdir -p scripts tests docs .claude/commands
   ```

6. **Initial commit**
   ```bash
   git add .
   git commit -m "Initial repository structure"
   ```

### Phase 1: Define Schema & Standards (Days 2-3) ✅ COMPLETE

**Goal**: Establish metadata schema and content standards before writing content

**Status**: ✅ All tasks completed

**Tasks**:

1. **Write docs/SCHEMA.md** - ✅ Complete
   - Full schema documentation with required and optional fields
   - Examples for all field types
   - Validation notes included

2. **Write docs/CONTRIBUTING.md** - ✅ Complete
   - Step-by-step guide for adding new topics
   - Content style guidelines (markdown, writing, code examples)
   - Testing and PR process documented

3. **Create example metadata.yaml** - ✅ Complete
   - Created `topics/dependency-injection/metadata.yaml` as reference
   - Includes all required fields and optional examples
   ```yaml
   # Example structure
   topic_id: dependency-injection
   title: Dependency Injection in Galaxy
   status: draft  # draft | stable | deprecated

   # Tracking
   created: 2025-01-15
   last_updated: 2025-01-15
   last_updated_by: jmchilton

   # Training slide metadata
   training:
     questions:
       - What is dependency injection?
       - How does Galaxy implement DI?
     objectives:
       - Understand DI patterns in Galaxy
       - Identify dependency injection points
     key_points:
       - Galaxy uses PasteScript-style DI
       - Managers are injected via app object
     time_estimation: 30m
     prerequisites:
       - architecture-frameworks

   # Sphinx documentation metadata
   sphinx:
     section: Architecture
     subsection: Core Patterns
     level: intermediate  # beginner | intermediate | advanced
     toc_depth: 2

   # Galaxy Hub metadata
   hub:
     audience: [developers, contributors]
     tags: [architecture, design-patterns, dependency-injection]

   # Cross-references
   related_topics:
     - application-components
     - frameworks
   related_code_paths:
     - lib/galaxy/managers/
     - lib/galaxy/app.py

   # Claude context
   claude:
     priority: high  # How important for dev questions
     focus_areas:
       - Dependency injection patterns
       - Manager initialization
       - Testing with injected dependencies
   ```

4. **Write validation schema** - ✅ Complete
   - Implemented `scripts/validate.py` with comprehensive validation
   - Checks required fields, topic_id matching, status enum, related topics
   - Provides clear error and warning reporting
   - Works with `uv run python scripts/validate.py`

**Additional Work Completed**:
- Set up Python project with `uv` package manager
- Created `pyproject.toml` with dependencies (PyYAML)
- Updated all documentation to use `uv` commands
- Updated `.gitignore` for uv-specific files

### Phase 2: Migrate First Topic (Days 4-6) ✅ COMPLETE

**Goal**: Fully migrate dependency-injection topic as proof of concept

**Status**: ✅ All tasks completed

**Tasks**:

1. **Extract content from existing slides** - ✅ Complete
   - Source: `~/workspace/training-material/topics/dev/tutorials/architecture-6-dependency-injection/slides.html`
   - Extracted all content from actual GTN slides
   - Identified key sections: overview, examples, testing

2. **Create metadata.yaml** - ✅ Complete
   - Extracted questions, objectives, key_points from slide frontmatter
   - Updated with correct content (type-based DI with Lagom)
   - Added related code paths (lib/galaxy/di/, structured_app.py, etc.)
   - Time estimation corrected to 15m

3. **Create overview.md** - ✅ Complete
   - Content matches actual slides
   - Focus on `app` god object problem
   - Type-based DI with Lagom explanation
   - Interfaces breaking circular dependencies
   - Benefits of typing

4. **Create examples.md** - ✅ Complete
   - Old vs new pattern comparisons
   - FastAPI controller examples
   - Legacy WSGI controller examples
   - Celery task examples with `@galaxy_task`
   - Container usage patterns

5. **Create testing.md** - ✅ Complete
   - Testing with type-based DI
   - Mocking individual dependencies
   - Controller and task testing examples
   - Best practices for DI testing

6. **Create .claude/CLAUDE.md** - ✅ Complete
   - Created comprehensive AI context file
   - Documents type-based DI with Lagom
   - Includes key files, patterns, and common questions
   - Updated with correct information from slides

7. **Validate content structure** - ✅ Complete
   - All required metadata present
   - Markdown properly formatted
   - Validation passes successfully
   - Content accurately reflects source slides

**Key Learnings**:
- Actual content focuses on type-based DI with Lagom, not generic PasteScript-style
- Slides emphasize `app` god object problem and solution with interfaces
- DI works uniformly across FastAPI, WSGI controllers, and Celery tasks
- Container-based construction simplifies object creation significantly

### Phase 3: Build Slide Generator (Days 7-9) ✅ COMPLETE

**Goal**: Generate GTN-compatible slides from structured content

**Status**: ✅ All core tasks completed, slide generator fully functional

**Tasks**:

1. **Create outputs/training-slides/template.html** - ✅ Complete
   - Remark.js template matching GTN style
   - Dynamic metadata rendering (questions, objectives, key_points, contributors)
   - Proper layout directives (left-aligned, center, introduction slides)
   - Content slide iteration

2. **Create outputs/training-slides/build.py** - ✅ Complete
   ```python
   #!/usr/bin/env python3
   """
   Generate GTN-compatible slides from topic content.

   Usage:
       python outputs/training-slides/build.py dependency-injection
   """

   import sys
   import yaml
   from pathlib import Path
   from jinja2 import Template

   def load_topic(topic_name):
       """Load all files for a topic."""
       topic_dir = Path(f"topics/{topic_name}")

       # Load metadata
       with open(topic_dir / "metadata.yaml") as f:
           metadata = yaml.safe_load(f)

       # Load content files
       content = {}
       for md_file in topic_dir.glob("*.md"):
           content[md_file.stem] = md_file.read_text()

       return metadata, content

   def markdown_to_slides(markdown_text):
       """Convert markdown to Remark.js slides."""
       # Split on ## headings or --- separators
       # Each becomes a slide
       slides = []
       current_slide = []

       for line in markdown_text.split('\n'):
           if line.startswith('## ') or line.strip() == '---':
               if current_slide:
                   slides.append('\n'.join(current_slide))
               current_slide = [line]
           else:
               current_slide.append(line)

       if current_slide:
           slides.append('\n'.join(current_slide))

       return slides

   def generate_slides(topic_name):
       """Generate slides for a topic."""
       metadata, content = load_topic(topic_name)

       # Load template
       template_path = Path("outputs/training-slides/template.html")
       template = Template(template_path.read_text())

       # Convert content to slides
       all_slides = []
       for section_name, section_content in content.items():
           slides = markdown_to_slides(section_content)
           all_slides.extend(slides)

       # Render template
       output = template.render(
           title=metadata['title'],
           questions=metadata['training']['questions'],
           objectives=metadata['training']['objectives'],
           key_points=metadata['training']['key_points'],
           time_estimation=metadata['training']['time_estimation'],
           slides=all_slides,
           topic_id=metadata['topic_id'],
       )

       # Write output
       output_dir = Path(f"outputs/training-slides/generated/architecture-{topic_name}")
       output_dir.mkdir(parents=True, exist_ok=True)
       output_file = output_dir / "slides.html"
       output_file.write_text(output)

       print(f"✓ Generated slides: {output_file}")
       print(f"  Copy to training-material/topics/dev/tutorials/")
       return output_file

   if __name__ == "__main__":
       if len(sys.argv) != 2:
           print("Usage: python build.py <topic-name>")
           sys.exit(1)

       generate_slides(sys.argv[1])
   ```

3. **Test slide generation** - ✅ Complete
   ```bash
   uv run python outputs/training-slides/build.py dependency-injection
   ```
   - Successfully generates slides matching original structure
   - All content sections included (overview, examples)
   - Testing content excluded (not in original slides)

4. **Compare with original slides** - ✅ Complete
   - Visual comparison performed
   - All core content present and verified
   - Formatting matches GTN style
   - Images integrated correctly

5. **Iterate on template/builder** - ✅ Complete
   - Fixed formatting issues
   - Added layout class support (`reduce90`, `enlarge150`)
   - Implemented `.code[]` wrapper for special code formatting
   - Added diff format support for unified approach slide
   - Dynamic contributor rendering from metadata
   - Proper slide splitting on `---` and `##` headings

6. **Additional enhancements completed**:
   - ✅ Added all 5 images (PlantUML diagrams + Lagom screenshot) to `images/` directory
   - ✅ Created `images/build.sh` for regenerating PlantUML SVGs
   - ✅ Added missing slides: "Constructing the Object Is Still Brittle" and "DI and Controllers - FastAPI Limitations"
   - ✅ Restored missing contributor (bgruening) to metadata
   - ✅ Created GitHub issue #1 for navigation footer implementation
   - ✅ Verified diff format rendering correctly

**Additional Work Completed**:
- Image management infrastructure in `images/` directory
- Support for layout classes (`class: reduce90`, `class: enlarge150`)
- `.code[]` wrapper processing for special code block styling
- Dynamic contributor list from metadata
- Content alignment with original slides (95%+ match)

**Known Remaining Items** (tracked in GitHub issues):
- Navigation footer (Issue #1) - needs metadata schema and template updates

### Phase 4: Add Validation (Days 10-11) ✅ COMPLETE

**Goal**: Automated checking of content quality and completeness

**Status**: ✅ All tasks completed, validation framework fully functional

**Tasks**:

1. **Create scripts/validate.py** - ✅ Complete (enhanced)
   ```python
   #!/usr/bin/env python3
   """
   Validate all topics for completeness and correctness.

   Checks:
   - metadata.yaml has all required fields
   - All referenced files exist
   - Internal topic references are valid
   - Markdown is well-formed
   - No broken code paths
   """

   import sys
   import yaml
   from pathlib import Path

   REQUIRED_METADATA_FIELDS = [
       'topic_id', 'title', 'status',
       'training.questions', 'training.objectives',
       'training.key_points', 'training.time_estimation',
   ]

   def validate_topic(topic_dir):
       """Validate a single topic directory."""
       errors = []
       warnings = []

       # Check metadata exists
       metadata_file = topic_dir / "metadata.yaml"
       if not metadata_file.exists():
           errors.append(f"Missing metadata.yaml")
           return errors, warnings

       # Load and validate metadata
       with open(metadata_file) as f:
           metadata = yaml.safe_load(f)

       # Check required fields
       for field in REQUIRED_METADATA_FIELDS:
           keys = field.split('.')
           value = metadata
           for key in keys:
               value = value.get(key, {})
           if not value:
               errors.append(f"Missing required field: {field}")

       # Check content files exist
       if not (topic_dir / "overview.md").exists():
           warnings.append("Missing overview.md")

       # Check Claude context
       if not (topic_dir / ".claude" / "CLAUDE.md").exists():
           warnings.append("Missing .claude/CLAUDE.md")

       # Check related topics are valid
       if 'related_topics' in metadata:
           for related in metadata['related_topics']:
               related_dir = Path(f"topics/{related}")
               if not related_dir.exists():
                   errors.append(f"Related topic not found: {related}")

       return errors, warnings

   def validate_all():
       """Validate all topics."""
       topics_dir = Path("topics")
       all_errors = {}
       all_warnings = {}

       for topic_dir in topics_dir.iterdir():
           if topic_dir.is_dir() and not topic_dir.name.startswith('.'):
               errors, warnings = validate_topic(topic_dir)
               if errors:
                   all_errors[topic_dir.name] = errors
               if warnings:
                   all_warnings[topic_dir.name] = warnings

       # Report results
       print(f"\n{'='*60}")
       print("VALIDATION REPORT")
       print(f"{'='*60}\n")

       if all_errors:
           print("❌ ERRORS:\n")
           for topic, errors in all_errors.items():
               print(f"  {topic}:")
               for error in errors:
                   print(f"    - {error}")
           print()

       if all_warnings:
           print("⚠️  WARNINGS:\n")
           for topic, warnings in all_warnings.items():
               print(f"  {topic}:")
               for warning in warnings:
                   print(f"    - {warning}")
           print()

       if not all_errors and not all_warnings:
           print("✅ All topics valid!")

       return len(all_errors) == 0

   if __name__ == "__main__":
       success = validate_all()
       sys.exit(0 if success else 1)
   ```

2. **Create tests/test_validate.py** - ✅ Complete
   - Unit tests for metadata validation
   - Tests for content quality checks
   - Tests for markdown validation
   - Tests for image validation
   - All 11 tests passing

3. **Run validation on existing topic** - ✅ Complete
   ```bash
   uv run python scripts/validate.py
   ```
   - Successfully validates all topics
   - Detects missing metadata, broken images, content quality issues

4. **Enhanced validation features** - ✅ Complete
   - ✅ Content quality checks (minimum length, heading hierarchy, code block language)
   - ✅ Markdown validation (broken images, unclosed code blocks)
   - ✅ Cross-reference validation (code paths mentioned in content)
   - ✅ Image path validation (metadata and markdown)
   - ✅ Better error reporting with file context

5. **CI Integration** - ✅ Complete
   - ✅ Created `.github/workflows/validate.yml`
   - ✅ Runs validation on push and PR
   - ✅ Runs test suite automatically
   - ✅ Uses `uv` for dependency management

### Phase 5: Migrate Second Topic (Days 12-14)

**Goal**: Migrate startup topic to prove repeatability

**Tasks**:

1. **Extract from existing slides**
   - Source: `training-material/topics/dev/tutorials/architecture-12-startup/slides.html`

2. **Create all required files**
   - metadata.yaml
   - overview.md (startup overview)
   - sequence.md (step-by-step startup sequence)
   - configuration.md (config loading)
   - .claude/CLAUDE.md

3. **Generate slides**
   ```bash
   uv run python outputs/training-slides/build.py startup
   ```

4. **Validate**
   ```bash
   uv run python scripts/validate.py
   ```

5. **Document any process improvements**
   - What was harder than expected?
   - What tooling gaps exist?
   - Update CONTRIBUTING.md with lessons learned

### Phase 6: Claude Integration (Days 15-16)

**Goal**: Create Claude commands for common workflows

**Tasks**:

1. **Create .claude/CLAUDE.md** (repository-level)
   ```markdown
   # Galaxy Architecture Documentation Repository

   This repository maintains the source of truth for Galaxy architecture documentation
   and generates multiple output formats (slides, Sphinx docs, Hub articles).

   ## Repository Structure
   - `topics/` - One directory per architectural topic
   - `outputs/` - Build scripts for different formats
   - `scripts/` - Validation and utility scripts
   - `docs/` - Meta-documentation

   ## Common Workflows

   ### Adding a New Topic
   1. Create directory: `topics/<topic-name>/`
   2. Create metadata.yaml following SCHEMA.md
   3. Create overview.md with main content
   4. Create .claude/CLAUDE.md for topic context
   5. Validate: `/validate-topic <topic-name>`
   6. Generate outputs: `/sync-slides <topic-name>`

   ### Updating Existing Topic
   1. Edit markdown files in topics/<topic-name>/
   2. Update metadata.yaml if structure changed
   3. Validate: `/validate-topic <topic-name>`
   4. Regenerate: `/sync-slides <topic-name>`

   ### Before Committing
   1. Run `/validate-all` to check all topics
   2. Build affected outputs
   3. Check git diff for unintended changes

   ## Output Formats
   - Training slides: For GTN, Remark.js format
   - Sphinx docs: For Galaxy documentation
   - Hub articles: For galaxyproject.org

   ## Key Files
   - SCHEMA.md - Metadata requirements
   - CONTRIBUTING.md - Content guidelines
   - PLAN.md - Implementation roadmap
   ```

2. **Create .claude/commands/sync-slides.md**
   ```markdown
   # Sync Slides Command

   Generate GTN training slides for a topic.

   ## Usage
   `/sync-slides <topic-name>`

   ## What this does
   1. Validates the topic metadata and content
   2. Runs outputs/training-slides/build.py
   3. Shows path to generated slides
   4. Reminds to copy to training-material repo

   ## Implementation
   Run these commands:

   ```bash
   python scripts/validate.py # optional but recommended
   python outputs/training-slides/build.py {{topic-name}}
   ```

   Then tell the user:
   - Where the slides were generated
   - How to preview them locally
   - Path to copy to training-material
   ```

3. **Create .claude/commands/validate-topic.md**
   ```markdown
   # Validate Topic Command

   Check a single topic for completeness and correctness.

   ## Usage
   `/validate-topic <topic-name>`

   ## What this checks
   - metadata.yaml has all required fields
   - Content files exist
   - Claude context exists
   - Related topics are valid
   - No obvious formatting issues

   ## Implementation
   Create a simple script or use validate.py with topic filter.
   ```

4. **Create .claude/commands/validate-all.md**
   ```markdown
   # Validate All Command

   Check all topics for issues.

   ## Usage
   `/validate-all`

## Implementation
```bash
uv run python scripts/validate.py
```
   ```

5. **Create .claude/commands/new-topic.md**
   ```markdown
   # New Topic Command

   Scaffold a new architectural topic.

   ## Usage
   `/new-topic <topic-name>`

   ## What this creates
   ```
   topics/<topic-name>/
     metadata.yaml       (from template)
     overview.md         (stub)
     .claude/
       CLAUDE.md         (template)
   ```

   ## Implementation
   Create a scaffolding script or manually create files from templates.
   ```

6. **Test each command**
   - Use them in Claude Code
   - Verify they work as expected
   - Document any issues

### Phase 7: Documentation (Days 17-18) ✅ COMPLETE

**Goal**: Write comprehensive documentation for contributors

**Status**: ✅ All documentation tasks completed

**Tasks**:

1. **Complete docs/SCHEMA.md** - ✅ Complete
   - Documented all metadata fields including new ones (contributors, images)
   - Explained purpose and usage with examples
   - Clearly marked required vs optional fields
   - Added validation rules section
   - Updated command references to use `uv run`

2. **Complete docs/CONTRIBUTING.md** - ✅ Complete
   - Updated with latest information (validation, CI, tests)
   - Added markdown formatting details (layout classes, code wrappers, diff format)
   - Enhanced testing section with CI integration
   - Updated all command examples to use `uv run`

3. **Write docs/OUTPUTS.md** - ✅ Complete
   - Documented training-slides output format
   - Explained how builder works
   - Added troubleshooting section
   - Documented how to add new output formats
   - Included best practices

4. **Write docs/MIGRATION.md** - ✅ Complete
   - Long-term migration plan to Galaxy repository
   - Prerequisites and decision criteria
   - Integration strategy and timeline
   - Challenges and solutions
   - Success metrics

5. **Polish README.md** - ✅ Complete
   - Clear value proposition and overview
   - Comprehensive quick start guide
   - Updated status with current progress
   - Links to all documentation
   - Examples and common tasks
   - Repository structure diagram
   - Features list (implemented and planned)

**Note**: Some Phase 7 tasks referenced Phase 5/6 (Claude commands), but core documentation is complete and independent.

### Phase 8: Real-World Usage (Ongoing)

**Goal**: Use the system for actual work to find issues

**Tasks**:

1. **Next time architecture info needs updating**
   - Update source content, not slides directly
   - Generate outputs
   - Compare with manual process
   - Document pain points

2. **Track metrics**
   - Time to update content: before vs after
   - Number of outputs generated from one source
   - Consistency improvements
   - Issues found during real use

3. **Gather feedback**
   - From yourself after using it
   - From other contributors if any
   - What's awkward?
   - What's missing?

4. **Iterate on tooling**
   - Fix bugs found
   - Add missing features
   - Improve DX (developer experience)

### Phase 9: Sphinx Output (Weeks 3-4)

**Goal**: Generate Galaxy Sphinx documentation from topics

**Tasks**:

1. **Study Galaxy's Sphinx setup**
   - Clone Galaxy repo
   - Look at doc/source/ structure
   - Understand existing patterns
   - Check build process

2. **Create outputs/sphinx-docs/build.py**
   - Convert markdown to RST
   - Generate proper Sphinx directives
   - Create index files
   - Handle cross-references

3. **Create templates**
   - RST template for topics
   - Index template
   - Table of contents

4. **Test in Galaxy docs build**
   - Copy generated files to Galaxy
   - Run Sphinx build
   - Check output
   - Fix issues

5. **Optional: PR to Galaxy**
   - If docs look good
   - Create PR to add architecture section
   - Explain source
   - Get feedback

### Phase 10: Automation (Weeks 5-6)

**Goal**: GitHub Actions for validation and preview

**Tasks**:

1. **Create .github/workflows/validate.yml**
   ```yaml
   name: Validate Content

   on: [push, pull_request]

   jobs:
     validate:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - name: Install dependencies
           run: pip install -r requirements.txt
         - name: Validate all topics
           run: python scripts/validate.py
   ```

2. **Create .github/workflows/build-preview.yml**
   - Build all outputs on PR
   - Upload as artifacts
   - Comment on PR with links

3. **Optional: Auto-sync to training-material**
   - On push to main
   - Generate slides
   - Create PR to training-material
   - Automated but requires approval

### Future Phases (Months)

- **Hub article generation**
- **More topics migrated**
- **Community contributions**
- **Migration to Galaxy repo**
- **Deprecate old slides**

## Templates & Examples

### README.md Template

```markdown
# Galaxy Architecture Documentation

**Source of truth for Galaxy architecture documentation**

This repository maintains structured documentation about Galaxy's architecture
and generates multiple output formats:

- **Training slides** for the Galaxy Training Network
- **Sphinx documentation** for Galaxy's official docs
- **Hub articles** for galaxyproject.org

## Why?

Architecture knowledge shouldn't be locked in presentation slides. By maintaining
content as structured markdown + metadata, we can:

- Generate multiple output formats from one source
- Keep documentation in sync across platforms
- Make it easier to maintain and update
- Provide better AI context for topic-specific questions

## Quick Start

```bash
# Clone
git clone https://github.com/jmchilton/galaxy-architecture.git
cd galaxy-architecture

# Install dependencies (requires uv: https://github.com/astral-sh/uv)
uv sync

# Validate content
uv run python scripts/validate.py

# Generate training slides for a topic
uv run python outputs/training-slides/build.py dependency-injection

# View generated slides
open outputs/training-slides/generated/architecture-dependency-injection/slides.html
```

## Repository Structure

- `topics/` - Architecture topics (one per directory)
  - Each contains: metadata.yaml, *.md content files, .claude/ context
- `outputs/` - Build scripts for different formats
- `scripts/` - Validation and utilities
- `docs/` - Meta-documentation

## Topics

Currently documented:
- **dependency-injection** - How Galaxy uses DI patterns
- **startup** - Galaxy application startup sequence

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for:
- How to add a new topic
- Content guidelines
- Validation and testing

## Generated Outputs

This repo generates:
1. **Training slides**: Remark.js slides for GTN
2. **Sphinx docs**: RST files for Galaxy documentation (coming soon)
3. **Hub articles**: Markdown for galaxyproject.org (future)

## License

MIT - See LICENSE

## Long-term Plan

This is currently an experimental repository. Once proven, the plan is to:
1. Migrate content into Galaxy's main repository under `doc/source/architecture/`
2. Integrate builds into Galaxy's documentation pipeline
3. Deprecate architecture slides in training-material (or auto-generate them)

See [MIGRATION.md](docs/MIGRATION.md) for details.
```

### docs/SCHEMA.md Template

```markdown
# Metadata Schema

Every topic must have a `metadata.yaml` file following this schema.

## Required Fields

### `topic_id` (string)
Unique identifier for the topic. Must match directory name.
```yaml
topic_id: dependency-injection
```

### `title` (string)
Human-readable title for the topic.
```yaml
title: Dependency Injection in Galaxy
```

### `status` (enum: draft | stable | deprecated)
Current status of the documentation.
```yaml
status: stable
```

### `training` (object)
Metadata for training slides.

#### `training.questions` (list of strings)
Learning questions this topic addresses.
```yaml
training:
  questions:
    - What is dependency injection?
    - How does Galaxy implement DI?
```

#### `training.objectives` (list of strings)
Learning objectives.
```yaml
training:
  objectives:
    - Understand DI patterns in Galaxy
    - Identify injection points
```

#### `training.key_points` (list of strings)
Key takeaways.
```yaml
training:
  key_points:
    - Galaxy uses PasteScript-style DI
    - Managers are injected via app
```

#### `training.time_estimation` (string)
Estimated time to learn this material.
```yaml
training:
  time_estimation: 30m
```

## Optional Fields

### `created` (date: YYYY-MM-DD)
When topic was first created.

### `last_updated` (date: YYYY-MM-DD)
When topic was last significantly updated.

### `last_updated_by` (string)
Who last updated the topic.

### `training.prerequisites` (list of strings)
Other topics to learn first.
```yaml
training:
  prerequisites:
    - frameworks
    - application-components
```

### `sphinx` (object)
Metadata for Sphinx documentation.
```yaml
sphinx:
  section: Architecture
  subsection: Core Patterns
  level: intermediate  # beginner | intermediate | advanced
  toc_depth: 2
```

### `hub` (object)
Metadata for Galaxy Hub articles.
```yaml
hub:
  audience: [developers, contributors]
  tags: [architecture, design-patterns]
```

### `related_topics` (list of strings)
Cross-references to other topics.
```yaml
related_topics:
  - application-components
  - startup
```

### `related_code_paths` (list of strings)
Galaxy code paths relevant to this topic.
```yaml
related_code_paths:
  - lib/galaxy/managers/
  - lib/galaxy/app.py
```

### `claude` (object)
AI context metadata.
```yaml
claude:
  priority: high  # low | medium | high
  focus_areas:
    - Dependency injection patterns
    - Manager initialization
```

## Validation

Run `python scripts/validate.py` to check all metadata files.

Required fields are enforced. Optional fields improve output quality.
```

### docs/CONTRIBUTING.md Template

```markdown
# Contributing Guide

## Adding a New Topic

1. **Choose a topic ID**
   - Lowercase, hyphenated (e.g., `plugin-system`)
   - Must be unique

2. **Create directory**
   ```bash
   mkdir -p topics/<topic-id>/.claude
   ```

3. **Create metadata.yaml**
   - Use another topic as template
   - Fill in all required fields
   - See docs/SCHEMA.md for details

4. **Write content**
   - Create overview.md at minimum
   - Additional .md files for subtopics
   - Use clear markdown headings

5. **Add Claude context**
   - Create .claude/CLAUDE.md
   - Explain what this topic covers
   - List relevant Galaxy code paths
   - Note how to update this topic

6. **Validate**
   ```bash
   python scripts/validate.py
   ```

7. **Generate outputs**
   ```bash
   python outputs/training-slides/build.py <topic-id>
   ```

8. **Commit**
   ```bash
   git add topics/<topic-id>
   git commit -m "Add <topic-id> documentation"
   ```

## Content Guidelines

### Markdown Style

- Use `##` for major sections (becomes slides)
- Use `###` for subsections
- Use `---` to force slide breaks
- Code blocks with language hints
- Speaker notes after `???`

### Example
```markdown
## What is Dependency Injection?

Pattern for managing dependencies.

???

Speaker note: Explain the difference between DI and service locator.

---

### Benefits

- Testability
- Loose coupling
- Flexibility
```

### Writing Style

- Clear and concise
- Assume intermediate Python knowledge
- Link to Galaxy code examples
- Prefer showing over telling

### Code Examples

- Use real Galaxy code when possible
- Keep examples short (< 20 lines)
- Include imports
- Add comments for clarity

## Updating Existing Topics

1. **Edit markdown files** in topics/<topic-id>/
2. **Update metadata.yaml** if needed
3. **Validate**: `python scripts/validate.py`
4. **Regenerate outputs**: `/sync-slides <topic-id>`
5. **Commit with descriptive message**

## Testing Changes

Before committing:

1. **Validate**: `python scripts/validate.py`
2. **Build slides**: `python outputs/training-slides/build.py <topic-id>`
3. **Preview slides**: Open generated HTML in browser
4. **Check links**: `python scripts/check-links.py`

## Pull Request Process

1. Validate and build outputs locally
2. Include generated outputs if helpful for review
3. Describe what changed and why
4. Reference related Galaxy PRs if applicable

## Questions?

Open an issue or reach out to @jmchilton
```

## Success Criteria

**Phase 1-2 Success** (Schema and first topic):
- ✅ Metadata schema documented
- ✅ dependency-injection topic fully migrated
- ✅ Content is cleaner and more maintainable than slides

**Phase 3-4 Success** (Build and validate):
- ✅ Generated slides visually match original GTN slides
- ✅ Validation catches common mistakes
- ✅ Build process is simple and fast

**Phase 5-6 Success** (Second topic and Claude):
- ✅ startup topic migrated with less effort than first
- ✅ Claude commands work smoothly
- ✅ Process feels repeatable

**Phase 7-8 Success** (Docs and usage):
- ✅ Documentation is clear enough for others to contribute
- ✅ Using it for real work is easier than editing slides directly
- ✅ Can update content and regenerate outputs in < 5 minutes

**Long-term Success**:
- ✅ Multiple output formats generated from one source
- ✅ Content stays in sync across platforms
- ✅ Easier to maintain than before
- ✅ Galaxy team interested in adopting
- ✅ Can migrate into Galaxy repo seamlessly

## Next Steps

1. **Start with Phase 0**: Initialize repo, create structure
2. **Complete Phase 1**: Define schema before writing content
3. **Work through Phase 2**: First topic migration is the hardest
4. **Build automation**: Make subsequent topics easier
5. **Iterate**: Learn and improve as you go

This plan is detailed enough to hand off but flexible enough to adapt as you learn what works.
