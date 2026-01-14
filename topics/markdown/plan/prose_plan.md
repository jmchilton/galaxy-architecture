# Prose Plan: Galaxy Markdown Architecture

This document plans prose sections to add connective tissue for Sphinx documentation.

**Updated:** After reviewing 12 code path research notes.

---

## Section 1: Introduction

### After slide `what_is_galaxy_markdown` — ✅ ADDED

**Prose ID:** `prose_why_galaxy_markdown`

---

### After slide `contextual_addressing` — ✅ ADDED

**Prose ID:** `prose_contextual_addressing`

---

### After slide `three_document_types` — ✅ ADDED

**Prose ID:** `prose_three_document_types`

---

## Section 2: Backend Parsing

### After slide `parser_architecture` — ✅ ADDED

**Prose ID:** `prose_parser_architecture`

---

### After slide `directive_syntax` — ✅ ADDED

**Prose ID:** `prose_directive_syntax`

---

### After slide `directive_categories` — ✅ ADDED

**Prose ID:** `prose_directive_categories`

---

### After slide `validation` — ✅ ADDED

**Prose ID:** `prose_validation`

---

## Section 3: Backend Rendering Pipeline

### After slide `transformation_pipeline` — ✅ ADDED

**Prose ID:** `prose_transformation_pipeline`

---

### After slide `handler_pattern` — ✅ ADDED

**Prose ID:** `prose_handler_pattern`

---

### After slide `id_encoding` — SKIPPED

Slide content is self-explanatory.

---

### After slide `invocation_resolution` — ✅ ADDED

**Prose ID:** `prose_invocation_resolution`

---

### After slide `pdf_export` — ✅ ADDED

**Prose ID:** `prose_pdf_export`

---

## Section 4: Frontend Components

### After slide `component_tree` — ✅ ADDED

**Prose ID:** `prose_component_tree`

---

### After slide `section_parsing` — ✅ ADDED

**Prose ID:** `prose_section_parsing`

---

### After slide `directive_processing` — ✅ ADDED

**Prose ID:** `prose_directive_processing`

---

### After slide `element_components` — ✅ ADDED

**Prose ID:** `prose_element_components`

---

### After slide `store_data_flow` — ✅ ADDED

**Prose ID:** `prose_store_data_flow`

---

## Section 5: Editor Architecture

### After slide `dual_mode_editor` — ✅ ADDED

**Prose ID:** `prose_dual_mode_editor`

---

### After slide `directive_registry` — ✅ ADDED

**Prose ID:** `prose_directive_registry`

---

### After slide `mode_aware_design` — Prose needed: NO

**Purpose:** Slide content is complete.

**Notes:** The three bullets capture mode awareness well.

---

## Section 6: Design & Extensibility

### After slide `design_principles` — ✅ ADDED

**Prose ID:** `prose_design_principles`

---

### After slide `adding_directive` — ✅ ADDED

**Prose ID:** `prose_adding_directive`

---

## Section 7: Summary

### After slide `architecture_overview` — ✅ ADDED

**Prose ID:** `prose_architecture_overview`

---

### After slide `key_takeaways` — Prose needed: NO

**Purpose:** Slide is complete.

**Notes:** Takeaways stand alone as bullet points.

---

## Prose Summary

| Section | Prose Needed | Research Status |
|---------|--------------|-----------------|
| Introduction | 3 blocks | ✅ Complete |
| Backend Parsing | 4 blocks | ✅ Complete |
| Rendering Pipeline | 5 blocks | ✅ Complete |
| Frontend Components | 5 blocks | ✅ Complete |
| Editor Architecture | 2 blocks | ✅ Complete |
| Design & Extensibility | 2 blocks | ✅ Complete |
| Summary | 1 block | ✅ Complete |

**Total:** ~22 prose blocks

---

## Research Tasks Status

### High Priority — ✅ COMPLETE
1. [x] Extract complete directive list from `ALLOWED_ARGUMENTS` — **30+ directives documented**
2. [x] List all Element components — **21 components in 6 categories**
3. [x] Document directives.yml and templates.yml structure — **Complete schema documented**

### Medium Priority — ✅ COMPLETE
4. [x] Check resolve_invocation_markdown() for edge cases — **Happy path documented; error handling unclear**
5. [x] Verify section types in parse.ts — **5 types: markdown, galaxy, vega, visualization, vitessce**
6. [x] Check which Pinia stores are used — **6 stores identified**

### Low Priority — ✅ COMPLETE
7. [x] Document PDF export customization options — **CSS, prologue/epilogue, branding documented**
8. [x] Document adding directive workflow — **6-step process complete**

---

## Remaining Open Questions

1. **Error handling:** What happens when `resolve_invocation_markdown()` encounters missing steps or failed jobs?
2. **History Markdown future:** Is there a PR or plan for history-relative addressing?
3. **Third-party section types:** Are there plugins that add new section types beyond the core 5?
4. **Directive deprecation:** Are any of the 30+ directives deprecated or rarely used?
5. **gxformat2 integration:** Is markdown_parse.py already being reused in gxformat2?

---

## Additional Insights from Research

### Pages System Integration
- Pages use **revision-based history**: every content change creates new `PageRevision`
- Supports **revision rollback** and version comparison
- **Embedded object strategy**: objects stored as placeholders, rendered on-demand
- **Soft deletion**: pages marked `deleted=true`, not hard-deleted

### Workflow Report System
- **Plugin architecture**: `WorkflowReportGeneratorPlugin` base class
- **Default template**: includes `invocation_inputs()`, `invocation_outputs()`, `workflow_display()`
- **Invocation context threading**: same template applies to multiple invocations
- **Runtime config override**: `runtime_report_config_json` parameter

### SVG Workflow Rendering
- `WorkflowCanvas` class in `lib/galaxy/workflow/render.py`
- Two-pass rendering: coordinate calculation → SVG drawing
- Color coding: `#EBD9B2` (normal), `#EBBCB2` (tool error)
- Resilient connection lookup for variable outputs

---

## Next Steps

1. ~~Run research tasks (high priority first)~~ ✅ Complete
2. Write prose blocks for diagrams (legends)
3. Create reference tables (directives, components)
4. Add tutorial content (adding directive walkthrough)
5. Integrate prose into content.yaml with `type: prose`
