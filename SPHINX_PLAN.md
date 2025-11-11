# Sphinx Output Implementation

**Status**: Phase 5 (Testing in Standalone Project) - COMPLETE ✅

This document describes the Sphinx documentation generation system and remaining work.

## Current Status (2025-11-11)

### Completed ✅

- **Phase 1**: Standalone Sphinx project set up in `doc/` directory
- **Phase 2**: Galaxy's documentation structure studied and understood
- **Phase 3**: `outputs/sphinx-docs/build.py` fully implemented
- **Phase 4**: Markdown processing complete with all transformations
- **Phase 5**: Testing with standalone project - all 13 topics generating successfully
  - All markdown files rendering correctly
  - Images displaying properly
  - Topic ordering via `continues_to`/`previous_to` chain working
  - Sphinx build quality verified as "not choppy"

### Verified ✅

- Sphinx output quality is good (not as choppy as initially worried)
- `continues_to`/`previous_to` topic sequencing chain works correctly
- Image paths properly converted (../../images/ → ../_images/)
- All 13 topics generate without errors
- URL hyperlinking working (bare URLs → markdown links)
- Remark.js directives (.pull-left/.pull-right) converted to side-by-side layout with dividers

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

## Remaining Work

### Immediate Next Steps (High Priority)

#### 1. Add "View as Slides" Link to Sphinx Docs

**Goal**: Each topic's Sphinx documentation should have a link to view it as training slides

**Implementation**:
- Add link to top/bottom of each topic markdown: "View this content as slides"
- Link format: `outputs/training-slides/generated/architecture-<topic-id>/slides.html`
- Consider adding to template or as a MyST directive
- Update `outputs/sphinx-docs/build.py` to inject this link

**Options**:
1. **Simple approach**: Add to top of each generated markdown file
   ```markdown
   > 📊 [View as training slides](../../../outputs/training-slides/generated/architecture-{topic}/slides.html)

   # Topic Title
   ```

2. **Fancy approach**: Create MyST directive for consistent styling
   ```markdown
   ```{note}
   📊 [View this content as training slides](../...)
   ```
   ```

**Status**: Not yet implemented

#### 2. Add Prose Content to Topics

**Goal**: Flesh out topics with additional explanatory content beyond slides

**Current State**:
- Topics contain mostly slide content (good for presentations)
- Some topics lack detailed explanations needed for documentation

**Work Needed**:
1. Identify which topics need additional prose:
   - ecosystem - broad topic, may need more detail
   - frameworks - could use more examples
   - plugin-system - conceptual overview missing
   - Others as discovered

2. Write extended explanations for each
3. Organize as separate sections in content.yaml
4. Test rendering in Sphinx

**Status**: Not started - optional for initial release

#### 3. Verify Sphinx Build Quality

**Goal**: Test full Sphinx documentation build to ensure Galaxy integration readiness

**What to Test**:
- Run `cd doc && make html` locally
- Check for warnings or errors
- Verify HTML rendering matches Galaxy's style
- Test cross-references and links
- Check image loading
- Verify mobile rendering

**Command**:
```bash
cd doc && make html
# Open doc/build/html/index.html in browser
```

**Status**: Not yet done

### Medium-term Work (Phase 6: Galaxy Integration)

#### 1. Plan Galaxy Integration

**Goal**: Prepare for eventual migration into Galaxy's official documentation

**Tasks**:
1. Identify exact location in Galaxy docs: `doc/source/dev/architecture/`
2. Plan how to handle:
   - Existing architecture docs in training-material
   - Version numbering and deprecation
   - Image storage in Galaxy repo
   - Build process integration
3. Create integration checklist
4. Document the migration process

**Status**: Planning phase

#### 2. Create Automation for Slide Sync

**Goal**: Keep training-material slides in sync with source content

**Approach**:
- Build script to detect changes in topics/
- Auto-regenerate slides via outputs/training-slides/build.py
- Copy HTML slides to training-material repo
- Eventually: GitHub Actions for automated syncing

**Current State**:
- Manual builds work fine
- No automation yet

**Status**: Not started - defer until Galaxy integration

#### 3. Extend Sphinx Features

**Goal**: Use more MyST features for enhanced documentation

**Possible Additions**:
- Cross-references between topics (using MyST {ref} syntax)
- Callout boxes for important concepts
- Code examples with language highlighting
- Tabbed content for different use cases
- Search indexing optimization

**Status**: Not needed for initial release

### Long-term Work (Phase 7+)

1. **GitHub Hub Article Generation** - Use topics as source for galaxyproject.org articles
2. **AI Training Integration** - Optimize topics for AI/agentic use cases
3. **Interactive Tutorials** - Generate Jupyter notebooks from topics
4. **API Documentation** - Auto-generate from code with architectural context

---

## How It Works

### Generation Process

The Sphinx documentation generation follows this pipeline:

1. **Load Topics** (`scripts/models.py`)
   - Load metadata.yaml (questions, objectives, key points, sequencing)
   - Load content.yaml (content blocks organized by type)
   - Validate with Pydantic v2

2. **Build Sphinx Output** (`outputs/sphinx-docs/build.py`)
   - Filter to slide-type blocks (prose skipped for Sphinx)
   - Generate markdown with:
     - Learning questions section
     - Learning objectives section
     - Content blocks (processed for Sphinx)
     - Key takeaways section
   - Process markdown:
     - Strip speaker notes (content after `???`)
     - Unwrap Remark.js directives (.code[], .reduce90[], etc.)
     - Convert .pull-left/.pull-right to side-by-side divider format
     - Fix image paths (../../images/ → ../_images/)
     - Fix asset paths ({{ site.baseurl }}/assets/images/ → ../_images/)
     - Convert bare URLs to markdown links [URL](URL)

3. **Output Management**
   - Generate to: `outputs/sphinx-docs/generated/architecture/`
   - Copy to: `doc/source/architecture/` (for local build)
   - Topic ordering via `continues_to` chain in index file

4. **Build with Sphinx**
   - Sphinx processes markdown via MyST parser
   - Generates HTML documentation
   - Output: `doc/build/html/`


## Implementation Summary

### Completed Components ✅

1. **Standalone Sphinx Project** (`doc/` directory)
   - ✅ Sphinx configuration (`doc/source/conf.py`)
   - ✅ Makefile with build targets
   - ✅ Static files and templates
   - ✅ Builds successfully with `make html`

2. **Build Script** (`outputs/sphinx-docs/build.py`)
   - ✅ Loads topics via Pydantic v2 models
   - ✅ Generates learning questions/objectives/key points
   - ✅ Processes markdown with all transformations
   - ✅ Handles image path conversion
   - ✅ Manages topic ordering via `continues_to` chain
   - ✅ Generates index files

3. **Markdown Processing**
   - ✅ Speaker notes stripping (per-block)
   - ✅ Remark.js directive unwrapping
   - ✅ .pull-left/.pull-right conversion to divider format
   - ✅ Image path conversion (../../images/ → ../_images/)
   - ✅ Asset path conversion ({{ site.baseurl }}/assets/images/ → ../_images/)
   - ✅ Bare URL hyperlinking to markdown links

4. **Testing**
   - ✅ All 13 topics generating successfully
   - ✅ Output quality verified as good (not choppy)
   - ✅ Images displaying correctly
   - ✅ Topic sequencing working correctly

---

## Remaining Deliverables

### Priority 1: "View as Slides" Link (HIGH)

**What**: Add link in each topic to view as training slides

**Why**: Create connection between documentation and presentation formats

**Where to add**:
- Top of each Sphinx markdown file generated by `outputs/sphinx-docs/build.py`
- Or in a note/callout box

**Link format**:
```
📊 [View this as training slides](../../../outputs/training-slides/generated/architecture-{topic-id}/slides.html)
```

**Implementation in build.py**:
```python
# After generating markdown, inject link at top
slides_link = f"📊 [View as training slides](../../../outputs/training-slides/generated/architecture-{topic_id}/slides.html)\n\n"
markdown = slides_link + markdown
```

**Status**: ❌ Not implemented - ready to code

### Priority 2: Verify Full Sphinx Build (MEDIUM)

**What**: Test `make html` build to ensure Galaxy readiness

**How**:
1. Run `cd doc && make html`
2. Verify no warnings or errors
3. Check HTML rendering quality
4. Test all cross-references and links
5. Verify images load correctly
6. Check responsive design

**Expected output**: `doc/build/html/index.html`

**Status**: ❌ Not yet tested

### Priority 3: Add Prose Content (MEDIUM)

**What**: Expand topics beyond slide content

**Current state**: Topics contain mostly slides (good for presentations)

**Gaps**:
- Some topics need more detailed explanations
- Missing conceptual overviews for complex topics
- Examples could be more detailed

**Approach**:
1. Identify topics needing prose (ecosystem, frameworks, etc.)
2. Write extended sections
3. Add to content.yaml
4. Regenerate Sphinx output

**Status**: ❌ Not started - optional for MVP

### Priority 4: Plan Galaxy Integration (LOW)

**What**: Prepare for eventual migration to Galaxy's doc structure

**Tasks**:
1. Document exact location: `~/workspace/galaxy/doc/source/dev/architecture/`
2. Plan handling of:
   - Existing architecture docs elsewhere
   - Version numbering
   - Image storage in Galaxy repo
   - Build process integration
3. Create integration checklist
4. Document step-by-step migration process

**Status**: 🔄 Partially planned - needs documentation

### Priority 5: Automation & CI (FUTURE)

**What**: Automate slide generation and syncing

**Scope**: Defer to Phase 7+

**Includes**:
- GitHub Actions for validation
- Auto-generate slides on topic changes
- Sync to training-material repository
- Build previews on PRs

**Status**: ❌ Not started

---

## How to Generate Sphinx Docs

```bash
# Generate markdown for all topics
python outputs/sphinx-docs/build.py all

# Build HTML locally
cd doc && make html

# View at browser
open doc/build/html/index.html
```

All 13 topics are now in `doc/source/architecture/*.md` ready for building.

---

## Implementation Decisions

### Image Strategy (COMPLETED)
**Chosen**: Option 1 - Copy to doc/source/_images/
- Implemented via migration scripts
- All 40+ images already copied
- Paths converted in generated markdown
- Self-contained and works offline

### Metadata Handling (COMPLETED)
**Chosen**: Metadata sections in generated markdown
- Learning questions as section
- Learning objectives as section
- Key takeaways as section
- Simple, clean approach

### Topic Ordering (COMPLETED)
**Chosen**: `continues_to`/`previous_to` chain
- Extracted from navigation footnotes
- Used in Sphinx index toctree
- Falls back to alphabetical if chain breaks
- Maintains conceptual flow

---

**Status**: Phase 5 Complete - Ready for Priority 1 work
**Last Updated**: 2025-11-11

