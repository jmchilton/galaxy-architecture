# Implementation Plan: Add Remark.js Layout Support to Slides

## Goal
Enable content blocks to reference named Remark.js layouts (e.g., `left-aligned`) and add standard layout definitions to generated slides.

## User Requirements
1. Reference existing template layouts (not custom definitions)
2. Rename `slides.layout` → `slides.class` for semantic clarity
3. Place layout blocks at top of slides (before title)

## Implementation Approach

### 1. Schema Changes (scripts/models.py)

**Update SlideRenderConfig (lines 132-142):**
```python
class SlideRenderConfig(BaseModel):
    render: bool = True
    class_: Optional[str] = Field(
        default=None,
        description="CSS classes to apply to slides (e.g., 'center', 'reduce90')"
    )
    layout_name: Optional[str] = Field(
        default=None,
        description="Named layout to reference (e.g., 'left-aligned')"
    )
```

**Update ContentBlock propagation logic (lines 198-202):**
- Keep `class_` convenience field
- Map it to `slides.class_` (not `slides.layout`)
- Update field name: `class_` → maps to `slides.class_`

**Validation:**
- Add validator to ensure `layout_name` references valid layouts
- Valid values: `left-aligned` or None

### 2. Slide Generation (outputs/training-slides/build.py)

**Update generate_slides() function (lines 185-307):**

**Step 2a: Apply layout references (update lines 207-212):**
```python
if block.slides.layout_name:
    for slide in slides:
        # Set layout reference if not already set
        if not slide.get('layout_ref'):
            slide['layout_ref'] = block.slides.layout_name

if block.slides.class_:
    for slide in slides:
        if not slide.get('class'):
            slide['class'] = f"class: {block.slides.class_}"
```

**Step 2b: Format slides with layout references (update lines 214-231):**
```python
formatted_slides = []
for slide in all_slides:
    slide_content = slide['content']
    slide_content = process_code_wrappers(slide_content)

    lines = []

    # Add layout reference if present
    if slide.get('layout_ref'):
        lines.append(f"layout: {slide['layout_ref']}")

    # Add class directive if present
    if slide['class']:
        lines.append(slide['class'])
    elif lines:  # Has layout but no class, add separator
        lines.append('')

    # Add content
    lines.append(slide_content)

    formatted_slides.append('\n'.join(lines))
```

**Step 2c: Add layout definitions at top (update template rendering around line 244):**
```python
# Standard Remark.js layout definitions
layout_definitions = [
    "---",
    "layout: true",
    "name: left-aligned",
    "class: left, middle",
    "---",
    "",
    "---",
    "layout: true",
    "class: center, middle",
    "---",
]

# Prepend to slides
formatted_slides = layout_definitions + formatted_slides
```

### 3. Template Updates (outputs/training-slides/template.html)

**Remove existing layout definitions (lines 19-37):**
- Delete the hardcoded layout blocks
- They'll now be generated dynamically via build.py

**Rationale:** Build script has more context and can conditionally include layouts.

### 4. HTML Wrapper Updates (outputs/training-slides/html_wrapper_template.html)

**Add layout definitions in markdown assembly (around line 268 in build.py):**
```python
# For HTML slides
layout_blocks = [
    "---",
    "layout: true",
    "name: left-aligned",
    "class: left, middle",
    "---",
    "",
    "---",
    "layout: true",
    "class: center, middle",
    "---",
]

# Build markdown for HTML
markdown_parts = layout_blocks + [title_slide] + [questions_md] + ...
```

### 5. Content Migration (topics/*/content.yaml)

**Update all 13 topics to use new field name:**
- Find: `class: center` (convenience field)
- Keep: This still works, but now maps to `slides.class_`
- Find: `slides:\n  layout: center` (explicit field)
- Replace with: `slides:\n  class: center`

**Example migration:**
```yaml
# Before
- type: slide
  class: center
  content: |
    ![Image](../../images/foo.svg)

# After (no change needed - convenience field still works)
- type: slide
  class: center
  content: |
    ![Image](../../images/foo.svg)
```

**Example with layout reference:**
```yaml
# New capability
- type: slide
  slides:
    layout_name: left-aligned
    class: reduce90
  content: |
    ### Some Heading
    Content here
```

### 6. Update Schema Documentation

**Update docs/SCHEMA.md:**
- Document `slides.class_` field
- Document `slides.layout_name` field with valid values
- Add examples of layout references
- Regenerate from models.py: `uv run python scripts/generate_schema_docs.py`

## Files to Modify

1. **scripts/models.py** - Schema changes
   - SlideRenderConfig class (lines 132-142)
   - ContentBlock propagation (lines 198-202)

2. **outputs/training-slides/build.py** - Generation logic
   - generate_slides() layout reference application (lines 207-212)
   - Slide formatting with layout/class (lines 214-231)
   - Layout definition injection (around line 244 for GTN, line 268 for HTML)

3. **outputs/training-slides/template.html** - Remove hardcoded layouts
   - Delete lines 19-37 (layout definitions)

4. **topics/*/content.yaml** - Field migration (13 files)
   - Update explicit `slides.layout` → `slides.class`
   - Convenience field `class:` unchanged

5. **docs/SCHEMA.md** - Documentation update
   - Regenerate via generate_schema_docs.py

## Testing Strategy

1. **Validate schema changes:**
   - Run `make validate` to ensure all topics parse correctly
   - Check that `layout_name` validation works

2. **Test slide generation:**
   - Build slides: `make build-slides`
   - Verify layout blocks appear at top of generated .md files
   - Check that layout references are properly formatted

3. **Visual verification:**
   - Open generated slides.html for a topic
   - Verify slides with `layout_name` reference apply correct classes
   - Check that layout definitions don't create extra blank slides

4. **Test both output formats:**
   - GTN markdown (.md files)
   - Standalone HTML (.html files)

## Migration Steps

1. Update schema (models.py)
2. Update build script (build.py)
3. Update template (template.html)
4. Regenerate schema docs
5. Run validation to catch issues
6. Migrate content.yaml files (automated with sed/scripts)
7. Test build and visual output
8. Commit changes

## Backward Compatibility

- `class:` convenience field continues to work
- Existing content.yaml files work after migration
- Generated output format unchanged (except layout blocks at top)
- Training-material sync unaffected (uses .md files)

## Open Questions

None - all clarified with user.
