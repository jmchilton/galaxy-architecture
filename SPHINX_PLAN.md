# Sphinx Output Plan

This document outlines the plan for generating Galaxy Sphinx documentation from topic content.

## Overview

The plan includes two main phases:
1. **Standalone Test Project**: Set up a Sphinx project in this repository that mirrors Galaxy's setup, allowing local testing and preview
2. **Galaxy Integration**: Eventually integrate generated docs into Galaxy's documentation structure

This approach allows us to test and iterate locally before making changes to Galaxy's repository.

## Galaxy's Sphinx Setup

Galaxy's documentation is located at `~/workspace/galaxy/doc/` and uses:

- **Sphinx** with **MyST Parser** extension for Markdown support
- **Source files** in `doc/source/` directory
- **Mixed format**: Both `.rst` and `.md` files are supported
- **Structure**: Organized by section (`admin/`, `dev/`, `api/`, etc.)

### Key Configuration (from `doc/source/conf.py`)

```python
extensions = ["myst_parser", "sphinx.ext.intersphinx"]
source_suffix = [".rst", ".md"]  # Both formats supported!
myst_enable_extensions = [
    "attrs_block",
    "deflist",
    "substitution",
    "colon_fence",
]
myst_heading_anchors = 5
```

### Current Structure

```
doc/source/
├── index.rst              # Main index
├── admin/                 # Administration docs
│   ├── production.md      # Example .md file
│   ├── config.rst
│   └── ...
├── dev/                   # Developer docs
│   ├── index.rst
│   ├── schema.md          # Example .md file
│   └── ...
├── api/                   # API docs
└── project/               # Project docs
```

## Implementation Plan

### Goal

Generate Markdown files for Galaxy's Sphinx documentation from topic content. **No RST conversion needed** - Galaxy already supports Markdown via MyST parser.

### Approach

1. **Set up standalone Sphinx project** in this repository (test bed)
2. **Generate Markdown files** directly (no conversion)
3. **Use MyST extensions** for advanced features
4. **Test locally** before integrating with Galaxy
5. **Eventually integrate** with Galaxy's existing structure (`doc/source/dev/architecture/`)

### Tasks

#### Phase 1: Set Up Standalone Sphinx Test Project

**Goal**: Create a standalone Sphinx project in this repository that mirrors Galaxy's setup, allowing us to test and preview documentation locally before integrating into Galaxy.

**Location**: `doc/` directory in this repository

**Structure**:
```
doc/
├── Makefile              # Copied from Galaxy (simplified)
├── source/
│   ├── conf.py          # Based on Galaxy's conf.py (standalone version)
│   ├── index.md         # Main index for architecture docs
│   ├── _static/         # Static files (CSS, etc.)
│   │   └── style.css    # Copied from Galaxy
│   ├── _templates/      # Custom templates
│   │   └── layout.html  # Copied from Galaxy
│   └── architecture/    # Generated architecture docs
│       ├── index.md
│       ├── dependency-injection.md
│       └── ...
└── build/               # Generated HTML (gitignored)
```

**Tasks**:

1. **Create doc/ directory structure**
   ```bash
   mkdir -p doc/source/{_static,_templates,architecture}
   ```

2. **Copy Galaxy's configuration** (`~/workspace/galaxy/doc/source/conf.py`)
   - Adapt for standalone use (remove Galaxy-specific imports)
   - Keep MyST parser configuration
   - Keep theme settings (sphinx_rtd_theme)
   - Keep static/template paths
   - Remove autodoc and Galaxy-specific code

3. **Copy Galaxy's static files**
   - `_static/style.css` - Custom CSS
   - Any other static assets needed

4. **Copy Galaxy's templates**
   - `_templates/layout.html` - Custom layout template

5. **Create simplified Makefile**
   - Based on Galaxy's Makefile
   - Remove Galaxy-specific targets
   - Keep basic `html`, `clean` targets

6. **Create initial index.md**
   ```markdown
   # Galaxy Architecture Documentation
   
   This section documents Galaxy's internal architecture.
   
   .. toctree::
     :maxdepth: 2
     :caption: Architecture Topics
   
     architecture/index
   ```

7. **Add Sphinx dependencies to pyproject.toml**
   ```toml
   [project.optional-dependencies]
   dev = [
     "pytest>=7.0.0",
     "sphinx>=7.0.0",
     "myst-parser>=2.0.0",
     "sphinx-rtd-theme>=2.0.0",
   ]
   ```

8. **Test Sphinx build**
   ```bash
   cd doc
   make html
   # View at doc/build/html/index.html
   ```

**Key Adaptations from Galaxy's Setup**:
- Remove `sys.path.insert` for Galaxy lib (not needed)
- Remove autodoc extensions (not documenting code)
- Remove Galaxy version imports
- Simplify to focus on architecture docs only
- Keep MyST parser and theme settings identical

#### Phase 2: Study Galaxy's Documentation Structure

**Location**: `~/workspace/galaxy/doc/`

**What to review**:
- How `.md` files are structured in existing docs
- How they're included in `index.rst` files
- What MyST features are commonly used
- How cross-references work
- Image handling

**Example files to study**:
- `doc/source/admin/production.md` - Full markdown example
- `doc/source/dev/schema.md` - Developer doc example
- `doc/source/dev/index.rst` - How markdown files are included

#### Phase 3: Create `outputs/sphinx-docs/build.py`

**Purpose**: Generate Markdown files for Galaxy Sphinx docs

**Key Features**:
- Load topic metadata and content
- Generate MyST-compatible Markdown
- Handle images (copy or reference)
- Create proper heading structure
- Generate index/table of contents

**Output Structure**:
```
outputs/sphinx-docs/generated/
└── architecture/
    ├── index.md           # Architecture section index
    ├── dependency-injection.md
    ├── startup.md
    └── ...
```

**Also copies to test project**:
```
doc/source/architecture/
├── index.md               # Auto-updated from generated
├── dependency-injection.md
└── ...
```

**Implementation Notes**:
- **No RST conversion** - output Markdown directly
- Use MyST syntax for advanced features (directives, roles)
- Preserve existing markdown structure from topics
- Handle code blocks (already in markdown format)
- Process images (copy to appropriate location or reference)

#### Phase 4: Markdown Processing

**What needs processing**:
- **Images**: Convert `../../images/` paths to Sphinx-relative paths
- **Code blocks**: Already in markdown, ensure language tags work
- **Cross-references**: Use MyST syntax for internal links
- **Metadata**: Convert YAML metadata to MyST frontmatter or directives

**Example transformations**:
```markdown
# Input (from topic)
![Alt](../../images/app_py2.plantuml.svg)

# Output (for Sphinx)
![Alt](../_images/app_py2.plantuml.svg)
```

#### Phase 5: Testing in Standalone Project

**Test process**:
1. Generate markdown files using `outputs/sphinx-docs/build.py`
2. Copy generated files to `doc/source/architecture/`
3. Update `doc/source/index.md` if needed
4. Run `make html` in `doc/` directory
5. View output at `doc/build/html/index.html`
6. Verify formatting, images, cross-references
7. Iterate until output matches Galaxy's style

**Benefits of standalone project**:
- Test without modifying Galaxy repo
- Preview changes locally
- Verify MyST features work correctly
- Ensure images and paths are correct
- Validate before integration

#### Phase 6: Integration with Galaxy Docs (Future)

**Location in Galaxy repo**:
```
doc/source/dev/architecture/
├── index.md               # Architecture section index
├── dependency-injection.md
└── ...
```

**Index file** (`doc/source/dev/index.rst`):
```rst
.. toctree::
  :maxdepth: 1

  schema
  api_guidelines
  ...
  architecture/index        # Add architecture section
```

**Architecture index** (`doc/source/dev/architecture/index.md`):
```markdown
# Architecture Documentation

This section documents Galaxy's internal architecture.

.. toctree::
  :maxdepth: 2

  dependency-injection
  startup
  ...
```

#### Phase 7: Build Script Features

**Core functionality**:
```python
def generate_sphinx_docs(topic_name):
    """Generate Sphinx markdown for a topic."""
    # Load topic
    metadata, content = load_topic(topic_name)
    
    # Process markdown
    # - Fix image paths
    # - Add MyST frontmatter if needed
    # - Handle cross-references
    
    # Write output
    output_file = f"outputs/sphinx-docs/generated/architecture/{topic_name}.md"
    output_file.write_text(processed_markdown)
```

**Image handling**:
- Copy images to `doc/source/_images/` or reference existing location
- Update paths in generated markdown

**Metadata integration**:
- Use MyST frontmatter for topic metadata
- Or convert to Sphinx directives

#### Phase 8: Automation (Future)

**Integration options**:
- **Manual**: Copy generated files to Galaxy repo
- **Script**: Sync script to copy files
- **CI**: Generate on changes, create PR to Galaxy
- **Migration**: Once in Galaxy repo, generate as part of Galaxy's doc build

## Key Differences from Training Slides

| Aspect | Training Slides | Sphinx Docs |
|--------|---------------|-------------|
| Format | HTML (Remark.js) | Markdown (MyST) |
| Images | `../../images/` | `../_images/` or absolute |
| Structure | Slides (sections) | Continuous docs |
| Metadata | YAML frontmatter | MyST frontmatter or directives |
| Code blocks | `.code[]` wrapper | Standard markdown |
| Cross-refs | N/A | MyST link syntax |

## Implementation Notes

### MyST Features to Use

- **Frontmatter**: For metadata
- **Directives**: For special formatting
- **Roles**: For inline formatting
- **Cross-references**: `{ref}` role for internal links
- **Substitutions**: For reusable content

### Image Strategy

**Option 1**: Copy images to Galaxy's `_images/` directory
- Pros: Self-contained, works offline
- Cons: Duplication, sync needed

**Option 2**: Reference images in this repo (if accessible)
- Pros: Single source of truth
- Cons: Requires repo to be accessible

**Option 3**: Generate images as part of Galaxy doc build
- Pros: Always up-to-date
- Cons: Requires PlantUML setup in Galaxy CI

**Recommendation**: Start with Option 1 (copy), migrate to Option 3 later.

### Metadata Handling

**Option 1**: MyST Frontmatter
```markdown
---
title: Dependency Injection in Galaxy
status: stable
---

# Dependency Injection in Galaxy
```

**Option 2**: Sphinx Directives
```markdown
.. topic:: Dependency Injection in Galaxy
   :status: stable

# Dependency Injection in Galaxy
```

**Recommendation**: Use MyST frontmatter for consistency with existing Galaxy docs.

## Prerequisites

- [x] Galaxy's doc structure available at `~/workspace/galaxy/doc/`
- [ ] Set up standalone Sphinx project in this repo
- [ ] Copy configuration and assets from Galaxy
- [ ] Review existing `.md` files in Galaxy docs
- [ ] Understand MyST parser features used
- [ ] Test markdown generation in standalone project
- [ ] Verify output matches Galaxy's style
- [ ] Eventually verify integration with Galaxy's build

## Dependencies

- Galaxy's Sphinx setup (already exists)
- MyST parser (already configured)
- Topic content (from this repo)
- Image files (from `images/` directory)

## Success Criteria

### Standalone Project
- ✅ Sphinx project builds successfully (`make html`)
- ✅ Output matches Galaxy's doc style and theme
- ✅ Generated markdown files render correctly
- ✅ Images display correctly
- ✅ Cross-references work
- ✅ Can preview locally before Galaxy integration

### Future Integration
- ✅ Generated markdown files build successfully in Galaxy's Sphinx
- ✅ Formatting matches Galaxy doc style exactly
- ✅ Can be integrated into Galaxy's doc build process
- ✅ No manual editing needed after generation

## Timeline

**Phase 1**: Set up standalone Sphinx project (1-2 days)
- Copy configuration from Galaxy
- Copy static files and templates
- Create simplified Makefile
- Test basic Sphinx build
- Add dependencies to pyproject.toml

**Phase 2**: Study Galaxy's documentation structure (1 day)
- Review existing `.md` files in Galaxy docs
- Understand MyST features used
- Study cross-reference patterns
- Review image handling

**Phase 3**: Build script (2-3 days)
- Create `outputs/sphinx-docs/build.py`
- Implement markdown processing
- Handle images and paths
- Generate architecture index

**Phase 4**: Markdown processing (1 day)
- Process image paths
- Handle code blocks
- Add MyST frontmatter
- Test transformations

**Phase 5**: Testing in standalone project (1-2 days)
- Generate docs for existing topics
- Build and preview locally
- Verify formatting matches Galaxy style
- Fix any issues

**Phase 6**: Integration with Galaxy (future, 1-2 days)
- Copy to Galaxy's `doc/source/dev/architecture/`
- Update Galaxy's index files
- Test in Galaxy's build
- Document process

**Total**: ~1-2 weeks (with standalone project setup)

## Future Enhancements

- Auto-generate architecture index from topics
- Cross-reference between architecture topics
- Link to code examples
- Generate API docs from architecture topics
- Integrate with Galaxy's doc build CI

---

**Status**: Planning phase  
**Last Updated**: 2025-01-15

