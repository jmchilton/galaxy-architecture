# Code-Based Slide Plan: Galaxy Markdown Architecture

Based on analysis of 12 code paths covering backend parsing, rendering, and frontend components.

## Section 1: Introduction & Problem Space (4 slides)

### Slide 1: What is Galaxy Markdown?
**Type:** concept
**Content idea:** Galaxy Markdown enables portable, reproducible documentation that embeds live Galaxy objects.
**Class:** enlarge150

### Slide 2: The Portability Problem
**Type:** diagram
**Content idea:** HTML embeds are instance-specific and break when shared; markdown with labels is portable.
**Proposed Diagram:** Component diagram showing HTML (instance-locked) vs Markdown (portable)
- Two paths: HTML with embedded URLs → breaks on export
- Markdown with labels → resolves anywhere
**Class:** center

### Slide 3: Two-Flavor Architecture
**Type:** diagram
**Content idea:** Workflow Markdown (labels) transforms to Galaxy Markdown (IDs) at render time.
**Proposed Diagram:** PlantUML sequence showing transformation
- Workflow Markdown: `output="results"` (portable)
- Galaxy Markdown: `history_dataset_id=12345` (renderable)
**Class:** center

### Slide 4: Three Document Types
**Type:** concept
**Content idea:** Reports (workflow outputs), Pages (persistent docs), Tool Outputs share the same markdown engine with different capabilities.
**Class:** enlarge120

---

## Section 2: Backend Parsing Layer (4 slides)

### Slide 5: Parser Architecture
**Type:** diagram
**Content idea:** Two-file separation: markdown_parse.py (validation) vs markdown_util.py (resolution).
**Proposed Diagram:** Component diagram
- markdown_parse.py: Pure parsing, no Galaxy deps, reusable
- markdown_util.py: ID resolution, object loading, rendering
**Class:** center
**Code Reference:** `lib/galaxy/managers/markdown_parse.py`

### Slide 6: Directive Syntax
**Type:** code-pattern
**Content idea:** Fenced code blocks with `galaxy` identifier contain directive function calls.
**Class:** reduce90
```markdown
```galaxy
history_dataset_as_table(history_dataset_id=12345, title="Results")
```
```

### Slide 7: Supported Directives
**Type:** concept
**Content idea:** 27+ directives across five categories: datasets, workflows, jobs, metadata, instance links.
**Class:** enlarge120
- Dataset: `history_dataset_display`, `_as_image`, `_as_table`, `_peek`, `_info`
- Workflow: `workflow_display`, `workflow_image`, `workflow_license`
- Job: `job_parameters`, `job_metrics`, `tool_stdout`, `tool_stderr`
- Meta: `generate_time`, `generate_galaxy_version`

### Slide 8: Validation Flow
**Type:** diagram
**Content idea:** Line-by-line fence tracking state machine validates syntax before any resolution.
**Proposed Diagram:** Flowchart or activity diagram
- Track fence state (open/closed)
- Match directive patterns
- Validate arguments against allowed list
- Fail fast with line number
**Class:** center

---

## Section 3: Backend Rendering Pipeline (5 slides)

### Slide 9: Transformation Pipeline
**Type:** diagram
**Content idea:** Five-stage pipeline from raw markdown to rendered output.
**Proposed Diagram:** PlantUML sequence
- Import (decode external IDs)
- Validation
- Resolution (expand workflow refs)
- Export (collect metadata OR expand fully)
- Render (HTML/PDF)
**Class:** center

### Slide 10: Handler Pattern
**Type:** diagram
**Content idea:** Abstract handler pattern enables multiple rendering contexts from same codebase.
**Proposed Diagram:** Class diagram
```
GalaxyInternalMarkdownDirectiveHandler (abstract)
├── ReadyForExportMarkdownDirectiveHandler (lazy - metadata only)
└── ToBasicMarkdownDirectiveHandler (eager - full expansion)
```
**Class:** center
**Code Reference:** `lib/galaxy/managers/markdown_util.py`

### Slide 11: ID Encoding Strategy
**Type:** code-pattern
**Content idea:** Internal numeric IDs stored; encoded IDs for URLs/export; decoded on import.
**Class:** reduce70
```python
# Storage (internal):
history_dataset_display(history_dataset_id=12345)

# Export (external):
history_dataset_display(history_dataset_id=a1b2c3d4e5f6)

# Regex patterns extract and convert
UNENCODED_ID_PATTERN = r"(history_dataset_id)=([\d]+)"
ENCODED_ID_PATTERN = r"(history_dataset_id)=([a-z0-9]+)"
```

### Slide 12: Invocation Resolution
**Type:** code-pattern
**Content idea:** Workflow labels resolve to concrete IDs: `output="results"` → `history_dataset_id=98765`.
**Class:** reduce90
**Code Reference:** `lib/galaxy/managers/markdown_util.py:resolve_invocation_markdown()`

### Slide 13: PDF Export Pipeline
**Type:** diagram
**Content idea:** Galaxy markdown → basic markdown → HTML → sanitized HTML → PDF via WeasyPrint.
**Proposed Diagram:** Sequence diagram
- ToBasicMarkdownDirectiveHandler expands all directives
- markdown.markdown() converts to HTML
- Sanitize for security
- WeasyPrint renders PDF
**Class:** center

---

## Section 4: Frontend Component Architecture (5 slides)

### Slide 14: Component Tree
**Type:** diagram
**Content idea:** Markdown.vue orchestrates parsing and delegates to specialized section renderers.
**Proposed Diagram:** Component tree
```
Markdown.vue
├── parseMarkdown() → Section[]
└── SectionWrapper
    ├── MarkdownDefault (standard markdown, KaTeX)
    ├── MarkdownGalaxy (Galaxy directives)
    ├── MarkdownVega (visualizations)
    ├── MarkdownVisualization (interactive viz)
    └── MarkdownVitessce (spatial data)
```
**Class:** center
**Code Reference:** `client/src/components/Markdown/Markdown.vue`

### Slide 15: Section Parsing
**Type:** code-pattern
**Content idea:** Triple-backtick delimiters split content into typed sections for routing.
**Class:** reduce90
**Code Reference:** `client/src/components/Markdown/parse.ts`

### Slide 16: Galaxy Directive Processing
**Type:** diagram
**Content idea:** MarkdownGalaxy.vue validates directive, loads data, renders appropriate element.
**Proposed Diagram:** Sequence diagram
- Parse directive name + arguments
- Validate against mode (page vs report)
- Fetch data via store/API
- Render element component
**Class:** center
**Code Reference:** `client/src/components/Markdown/Sections/MarkdownGalaxy.vue`

### Slide 17: Element Components
**Type:** concept
**Content idea:** 21+ specialized elements render specific Galaxy objects (tables, images, job outputs).
**Class:** enlarge120
- HistoryDatasetAsTable, HistoryDatasetAsImage
- WorkflowImage, WorkflowDisplay
- JobMetrics, JobParameters
- ToolStdout, ToolStderr
**Code Reference:** `client/src/components/Markdown/Sections/Elements/`

### Slide 18: Store-Centric Data Flow
**Type:** diagram
**Content idea:** Pinia stores cache invocation/workflow data; elements fetch via stores for efficiency.
**Proposed Diagram:** Component diagram showing data flow
- Components → Stores (invocationStore, workflowStore)
- Stores → API endpoints
- Caching prevents redundant fetches
**Class:** center

---

## Section 5: Editor Architecture (4 slides)

### Slide 19: Dual-Mode Editor
**Type:** diagram
**Content idea:** TextEditor (raw markdown) vs CellEditor (Jupyter-like structured editing).
**Proposed Diagram:** Component diagram or mockup
- TextEditor: Full markdown control
- CellEditor: Cell-by-cell with add/remove/reorder
**Class:** center
**Code Reference:** `client/src/components/Markdown/MarkdownEditor.vue`

### Slide 20: Cell-Based Editing
**Type:** concept
**Content idea:** CellEditor provides Jupyter-like experience with typed cells and live preview.
**Class:** enlarge120
- Add markdown cells
- Insert Galaxy directive cells from palette
- Reorder cells drag-and-drop
- Live preview as you edit

### Slide 21: Directive Registry
**Type:** code-pattern
**Content idea:** directives.yml provides metadata; templates.yml provides insertion templates.
**Class:** reduce90
```yaml
# directives.yml
history_dataset_as_table:
  side_panel_name:
    page: "Dataset Table"
    report: "Output Table"
  help: "Embed dataset as formatted table..."
```
**Code Reference:** `client/src/components/Markdown/directives.yml`

### Slide 22: Mode-Aware Design
**Type:** concept
**Content idea:** Same directives present differently in pages vs reports based on context.
**Class:** enlarge120
- Page mode: references to any workflow/dataset
- Report mode: references to "this" invocation

---

## Section 6: Design Principles (3 slides)

### Slide 23: Core Design Principles
**Type:** diagram
**Content idea:** Key architectural decisions that make Galaxy Markdown work.
**Proposed Diagram:** Concept mindmap
- Two-layer addressing (labels → IDs)
- Lazy resolution (resolve at render time)
- Handler extensibility (add new contexts)
- Mode awareness (pages vs reports)
**Class:** center

### Slide 24: Separation of Concerns
**Type:** concept
**Content idea:** Parse vs resolve, frontend vs backend, validation vs rendering.
**Class:** enlarge150
- markdown_parse.py: syntax only (reusable)
- markdown_util.py: Galaxy integration
- Frontend: rendering and interactivity
- Backend: data access and export

### Slide 25: Extensibility Pattern
**Type:** code-pattern
**Content idea:** Adding a new directive requires: allowed_arguments, handler method, frontend element.
**Class:** reduce70

---

## Section 7: Validation & Security (2 slides)

### Slide 26: Multi-Layer Validation
**Type:** diagram
**Content idea:** Validation at parse time (syntax), resolve time (references), render time (context).
**Proposed Diagram:** Flowchart
- Parse: valid directive syntax?
- Resolve: valid object IDs?
- Render: available in this mode?
**Class:** center

### Slide 27: Security Boundaries
**Type:** concept
**Content idea:** HTML sanitization, encoded IDs, trust boundaries between document types.
**Class:** enlarge120
- Pages: user-created, can reference any history
- Reports: workflow-generated, scoped to invocation
- Tool outputs: tool-generated, restricted sandbox

---

## Section 8: Summary (2 slides)

### Slide 28: Architecture Overview
**Type:** diagram
**Content idea:** Full end-to-end flow from workflow definition to rendered document.
**Proposed Diagram:** Large sequence or component diagram showing complete flow
**Class:** center

### Slide 29: Key Takeaways
**Type:** concept
**Content idea:** Main points for developers working with Galaxy Markdown.
**Class:** enlarge200
- Portable: workflow labels → instance IDs
- Extensible: handler pattern, directive registry
- Multi-format: same source → HTML, PDF, UI

---

## Diagram TODO List

### 1. Two-Flavor Transformation
**Type:** Sequence diagram
**Participants:** Workflow Definition, markdown_util, Galaxy Markdown, Frontend
**Key elements:** Label resolution, ID injection
**Reference:** Similar to images/core_tool_sequence.plantuml.txt

### 2. Parser Component Diagram
**Type:** Component diagram
**Components:** markdown_parse.py, markdown_util.py, pages.py, workflows.py
**Key elements:** Dependencies, separation of concerns

### 3. Validation State Machine
**Type:** Activity diagram or Flowchart
**Components:** Line parser, fence tracker, directive validator
**Key elements:** State transitions, error paths

### 4. Rendering Pipeline
**Type:** Sequence diagram
**Participants:** Raw Markdown, Import, Validate, Resolve, Export, Render
**Key elements:** Five stages, data transformations

### 5. Handler Class Hierarchy
**Type:** Class diagram
**Classes:** GalaxyInternalMarkdownDirectiveHandler, ReadyForExport, ToBasicMarkdown
**Key elements:** Abstract methods, inheritance

### 6. PDF Export Sequence
**Type:** Sequence diagram
**Participants:** markdown_util, markdown lib, sanitizer, WeasyPrint
**Key elements:** Transformations, security layer

### 7. Frontend Component Tree
**Type:** Component diagram or tree
**Components:** Markdown.vue, SectionWrapper, MarkdownGalaxy, Elements/*
**Key elements:** Hierarchy, delegation

### 8. Galaxy Directive Processing
**Type:** Sequence diagram
**Participants:** MarkdownGalaxy.vue, validation, stores, API, Element
**Key elements:** Data flow, caching

### 9. Store Data Flow
**Type:** Component diagram
**Components:** Element components, Pinia stores, API endpoints
**Key elements:** Caching, data paths

### 10. Editor Modes
**Type:** Component diagram or mockup
**Components:** TextEditor, CellEditor, directive palette
**Key elements:** Two editing experiences

### 11. Design Principles Mindmap
**Type:** Concept mindmap (YAML)
**Elements:** Two-layer addressing, Lazy resolution, Handler extensibility, Mode awareness

### 12. Validation Layers
**Type:** Flowchart
**Elements:** Parse validation, resolve validation, render validation
**Key elements:** Error handling at each layer

### 13. Complete Architecture Overview
**Type:** Large sequence or component diagram
**Participants:** All major components end-to-end
**Reference:** Similar to images/asgi_app.plantuml.txt
