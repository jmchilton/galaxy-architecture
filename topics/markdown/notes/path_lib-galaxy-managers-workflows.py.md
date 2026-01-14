# Code Path: lib/galaxy/managers/workflows.py

## Role in Workflow Report Integration

Orchestrates workflow invocation report generation using Galaxy Flavored Markdown. Integrates with markdown processing pipeline to create rich, context-aware documentation of workflow executions.

## Key Components

### Workflow Report Generation Pipeline

**Entry Point:** `WorkflowsManager.get_invocation_report()`
- Accepts optional `invocation_markdown`, `runtime_report_config_json`, target format (json/pdf)
- Delegates to plugin-based report generation system
- Returns report in requested format

**Plugin System:** Uses `workflow/reports/__init__.py:generate_report()`
- Default generator: `DEFAULT_REPORT_GENERATOR_TYPE = "markdown"`
- Pluggable architecture allows additional generators
- Extensible design for future report formats

### Core Report Generator Classes

**Base Plugin Architecture:**
- `WorkflowReportGeneratorPlugin` - Abstract base interface
- `WorkflowMarkdownGeneratorPlugin` - Handles markdown-based reports

**Markdown Plugin Flow:**
```
_generate_report_markdown() [template-based]
    ↓
_generate_internal_markdown() [adds invocation context]
    ↓
generate_report_json() [expands refs + prepares for export]
    ↓
generate_report_pdf() [converts to PDF]
```

## Markdown Processing Layers

### Layer 1: Import Processing
`ready_galaxy_markdown_for_import()` - Converts external encoded IDs to internal numeric IDs

### Layer 2: Invocation Population
`populate_invocation_markdown()` - Adds `invocation_id` attributes to directives
- Converts abstract workflow references to invocation-specific
- Example: `output=name` → `output=name, invocation_id=123`

### Layer 3: Internal Resolution
`resolve_invocation_markdown()` - Maps abstract concepts to actual IDs
- `output=name` → `history_dataset_id=456`
- `input=name` → `history_dataset_id=456`
- `step=name` → `job_id=789`
- Expands invocation-specific directives

### Layer 4: Export Preparation
`ready_galaxy_markdown_for_export()` - Processes through handler walker
- Converts numeric IDs back to encoded IDs
- Collects rendering metadata
- Returns three variants: export_markdown, embed_expanded, extra_rendering_data

### Layer 5: Basic Markdown Conversion
`to_basic_markdown()` - Converts Galaxy directives to plain markdown
- Used for PDF/HTML export
- Example: `history_dataset_display()` → markdown table

## PDF Generation Pipeline

```
internal_galaxy_markdown
    ↓
to_basic_markdown() [expand directives]
    ↓
to_html() [markdown → HTML]
    ↓
to_pdf_raw() [HTML → PDF via weasyprint]
    ↓
to_branded_pdf() [adds prologue/epilogue + CSS]
```

**Branding Support:**
- Document-type specific CSS: `markdown_export_css_{reports|invocations|pages}`
- Prologue/epilogue markdown per-document-type or global
- WeasyPrint dependency (optional)

## Design Patterns

### ID Encoding/Decoding Strategy
- **External (API):** Encoded base36 IDs for security
- **Internal (DB):** Numeric unencoded IDs
- **Transition Points:** Import (encoded → unencoded), Export (unencoded → encoded)

### Multi-Format Rendering
Single markdown source → multiple outputs:
- JSON Export for client-side rendering
- HTML/PDF for static download
- Embedded image data (base64) for standalone exports
- Client widgets with extra rendering data

### Separation of Concerns
- Template/Configuration stored in `workflow.reports_config`
- Content Generation via plugin system
- Markdown Processing via utility layer
- ID Management via security context
- Rendering via format-specific handlers

### Invocation Context Threading
All invocation-aware directives require `invocation_id=` because:
- Same template applies to multiple invocations
- Resolution maps abstract `output=name` to specific execution's dataset
- Enables report reproducibility across re-runs

## Default Report Template

```markdown
# ${title}

## Workflow Inputs
```galaxy
invocation_inputs()
```

## Workflow Outputs
```galaxy
invocation_outputs()
```

## Workflow
```galaxy
workflow_display()
```
```

## Configuration Points

**Workflow Level:**
- `StoredWorkflow.reports_config` - Dict with `title` and `markdown`
- Overridable at invocation time with `runtime_report_config_json`

**Instance Level:**
- `markdown_export_prologue` / `markdown_export_epilogue` - Branding
- `markdown_export_css` - Styling
- Instance URLs for links

## Documentation Highlights

**For training:**
- Plugin architecture enables extensibility
- Lazy rendering - data collection deferred until format determined
- ID security via consistent encoding boundaries
- Handler pattern for directive processing
- Markdown as intermediate representation
- Invocation context threading for reproducibility
