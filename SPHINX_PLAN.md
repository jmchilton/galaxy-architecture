# Sphinx Output Plan

This document outlines the plan for generating Galaxy Sphinx documentation from topic content.

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

1. **Generate Markdown files** directly (no conversion)
2. **Use MyST extensions** for advanced features
3. **Integrate with existing structure** (likely `doc/source/dev/architecture/`)
4. **Maintain compatibility** with Galaxy's Sphinx build

### Tasks

#### 1. Study Galaxy's Documentation Structure

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

#### 2. Create `outputs/sphinx-docs/build.py`

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

**Implementation Notes**:
- **No RST conversion** - output Markdown directly
- Use MyST syntax for advanced features (directives, roles)
- Preserve existing markdown structure from topics
- Handle code blocks (already in markdown format)
- Process images (copy to appropriate location or reference)

#### 3. Markdown Processing

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

#### 4. Integration with Galaxy Docs

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

#### 5. Build Script Features

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

#### 6. Testing

**Test process**:
1. Generate markdown files
2. Copy to Galaxy's `doc/source/dev/architecture/`
3. Update `doc/source/dev/index.rst` to include architecture section
4. Run `make html` in `doc/` directory
5. Verify output looks correct
6. Check cross-references work
7. Verify images display

#### 7. Automation (Future)

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

- [ ] Study Galaxy's doc structure (`~/workspace/galaxy/doc/`)
- [ ] Review existing `.md` files in Galaxy docs
- [ ] Understand MyST parser features used
- [ ] Test markdown generation locally
- [ ] Verify integration with Galaxy's build

## Dependencies

- Galaxy's Sphinx setup (already exists)
- MyST parser (already configured)
- Topic content (from this repo)
- Image files (from `images/` directory)

## Success Criteria

- ✅ Generated markdown files build successfully in Galaxy's Sphinx
- ✅ Images display correctly
- ✅ Cross-references work
- ✅ Formatting matches Galaxy doc style
- ✅ Can be integrated into Galaxy's doc build process

## Timeline

**Phase 1**: Study and planning (1-2 days)
- Review Galaxy's doc structure
- Understand MyST features
- Plan integration approach

**Phase 2**: Build script (2-3 days)
- Create `outputs/sphinx-docs/build.py`
- Implement markdown processing
- Handle images and paths

**Phase 3**: Testing (1-2 days)
- Generate docs for existing topics
- Test in Galaxy's build
- Fix issues

**Phase 4**: Integration (1-2 days)
- Create architecture section in Galaxy docs
- Update index files
- Document process

**Total**: ~1 week

## Future Enhancements

- Auto-generate architecture index from topics
- Cross-reference between architecture topics
- Link to code examples
- Generate API docs from architecture topics
- Integrate with Galaxy's doc build CI

---

**Status**: Planning phase  
**Last Updated**: 2025-01-15

