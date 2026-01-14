# Code Path: lib/galaxy/managers/markdown_util.py

## Role in Architecture

Processing engine for Galaxy Flavored Markdown - bridges stored markdown content and multiple output formats (HTML, PDF, web UI). Resolves Galaxy objects referenced by ID and renders them appropriately for different contexts.

## Core Design Pattern: Directive Handler Pattern

Abstract handler pattern where different rendering contexts implement the same directive interface:

```
GalaxyInternalMarkdownDirectiveHandler (abstract base)
├── ReadyForExportMarkdownDirectiveHandler (collects rendering metadata)
├── ToBasicMarkdownDirectiveHandler (converts to exportable markdown)
└── Custom handlers for specific contexts
```

## Key Responsibilities

### 1. Markdown Validation & ID Conversion

- **`ready_galaxy_markdown_for_import()`** - Converts external (encoded) IDs to internal (numeric) IDs
- **`_validate()`** - Wraps validation with Galaxy exception handling
- **Regex patterns** - Match and extract encoded/unencoded IDs, invocation IDs, parameters

**Example flow:**
```
External: history_dataset_display(history_dataset_id=a1b2c3d4e5f6g7h8)
↓ (decode)
Internal: history_dataset_display(history_dataset_id=12345)
```

### 2. Directive Processing & Resolution

30+ custom directives for Galaxy objects:

- **Dataset:** `history_dataset_display`, `history_dataset_as_image`, `history_dataset_as_table`, `history_dataset_peek`
- **Workflow:** `workflow_display`, `workflow_image`, `workflow_license`
- **Job:** `tool_stdout`, `tool_stderr`, `job_parameters`, `job_metrics`
- **Invocation:** `invocation_inputs`, `invocation_outputs`, `invocation_time`
- **Instance:** `instance_access_link`, `instance_help_link`, etc.

### 3. Context-Specific Rendering

**ReadyForExportMarkdownDirectiveHandler:**
- Collects metadata for client-side rendering
- Stores dataset names, types, peek data in `extra_rendering_data` dict
- Preserves encoded IDs for external links

**ToBasicMarkdownDirectiveHandler:**
- Fully expands to standard markdown
- Converts datasets to formatted tables
- Embeds images as base64 data URIs
- Materializes all content for PDF/HTML export

### 4. Invocation-Specific Processing

**`populate_invocation_markdown()`** - Adds invocation context:
```
workflow output "results" → invocation_id=inv123, output="results"
```

**`resolve_invocation_markdown()`** - Converts abstract references:
```
output="step_name" → history_dataset_id=98765
input="input_name" → history_dataset_id=12345
step="tool_name" → job_id=54321
```

## Rendering Pipeline

```
Raw Markdown
    ↓
[Import] Decode IDs + Validate
    ↓
Internal Markdown (numeric IDs)
    ↓
[Resolution] Expand invocation/job references
    ↓
[Export] Convert to target format:
    ├→ ReadyForExport: Collect metadata + encode IDs
    ├→ ToBasicMarkdown: Fully expand directives
    ├→ to_html(): Standard markdown → HTML (with sanitization)
    └→ to_pdf_raw(): HTML → PDF (via WeasyPrint)
```

## PDF Export Workflow

**`internal_galaxy_markdown_to_pdf()`** orchestrates:

1. Convert Galaxy directives to basic markdown via `ToBasicMarkdownDirectiveHandler`
2. Convert markdown to HTML via `markdown.markdown()`
3. Sanitize HTML (security layer)
4. Convert HTML to PDF using WeasyPrint
5. Apply base CSS + optional custom CSS
6. Add custom prologue/epilogue markdown for branding

## ID Encoding/Decoding Strategy

- **Storage:** Numeric IDs (`history_dataset_id=12345`)
- **Export/URLs:** Encoded IDs (`history_dataset_id=a1b2c3d4e5f6`)
- **Import:** Validates and decodes external content

**Regex patterns extract IDs for remapping:**
```python
UNENCODED_ID_PATTERN = r"(history_id|workflow_id|...)=([\d]+)"
ENCODED_ID_PATTERN = r"(history_id|workflow_id|...)=([a-z0-9]+)"
```

## Important Design Patterns

1. **Extensibility via Abstract Handlers** - New rendering contexts only need to implement the abstract interface
2. **Lazy vs. Eager Expansion** - ReadyForExport (lazy), ToBasicMarkdown (eager)
3. **Regex-Based Parsing** - Compiled patterns for efficiency
4. **Container Types** - Fenced blocks and embedded directives
5. **Separation of Concerns** - Syntactic validation (markdown_parse.py) vs. semantic resolution (markdown_util.py)

## Key Implementation Details

**Parameter Extraction:**
```python
ARG_VAL_CAPTURED_REGEX = r"(?:([\w_\-\|]+)|\"([^\"]+)\"|\'([^\']+)\')"
```

**Image Embedding:**
- Base64 encodes binary data for data URI: `data:image/png;base64,...`

**Workflow Visualization:**
- Calls `workflow_manager.get_workflow_svg()` for SVG export
- Embeds as data URI for portability

**Job Metrics/Parameters:**
- Formats as markdown tables with plugin organization
- Handles nested parameter depths

## Documentation Highlights

**For training:**
- Explain two-layer addressing (workflow markdown → Galaxy markdown)
- Show PDF export pipeline
- Demonstrate ID encoding/decoding security
- Illustrate lazy vs eager rendering strategies
- Show how to add new directives
