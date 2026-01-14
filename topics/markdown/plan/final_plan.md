# Final Slide Plan: Galaxy Markdown Architecture

**Flow:** A (Architecture-First)
**Duration:** 30 minutes
**Audience:** Advanced Galaxy developers

---

## Slide Outline (24 slides)

### Section 1: Introduction (3 slides)

#### Slide 1: What is Galaxy Markdown?
**Type:** concept
**Class:** enlarge150
**Content:**
- Portable, reproducible documentation with embedded Galaxy objects
- Alternative to HTML (instance-locked)
- Powers: workflow reports, pages, tool outputs

#### Slide 2: Contextual Addressing → Internal IDs
**Type:** diagram
**Class:** center
**Diagram:** Component diagram showing convergence
```
Workflow Markdown ───┐  (step/output labels)
Tool Output Markdown ┼──► Internal Galaxy Markdown ──► Render
Page API (encoded) ──┤  (direct object IDs)
History Markdown ────┘  (future: history-relative)
```
- Multiple context-specific formats converge to canonical internal form
- Internal form uses direct numeric IDs (`history_dataset_id=12345`)
- Resolution happens at appropriate boundary for each context

#### Slide 3: Three Document Types
**Type:** concept
**Class:** enlarge120
**Content:**
| Type | Editable | Scope | Use Case |
|------|----------|-------|----------|
| Reports | No | Invocation | Workflow output docs |
| Pages | Yes | Any | User documentation |
| Tool Output | No | Job | Tool-generated reports |

---

### Section 2: Backend Parsing (4 slides)

#### Slide 4: Parser Architecture
**Type:** diagram
**Class:** center
**Diagram:** Component diagram
- `markdown_parse.py`: Pure parsing, no Galaxy deps (reusable in gxformat2)
- `markdown_util.py`: Galaxy integration, ID resolution, rendering
**Code:** `lib/galaxy/managers/markdown_parse.py`

#### Slide 5: Directive Syntax
**Type:** code-pattern
**Class:** reduce90
```markdown
```galaxy
history_dataset_as_table(history_dataset_id=12345, title="Results")
```

Inline: Text with ${galaxy history_dataset_name(output="results")} embedded.
```
**Code:** `lib/galaxy/managers/markdown_parse.py:GALAXY_MARKDOWN_FUNCTION_CALL_LINE`

#### Slide 6: 27 Directives
**Type:** concept
**Class:** enlarge120
- **Dataset:** `display`, `as_image`, `as_table`, `peek`, `info`, `link`, `name`, `type`
- **Workflow:** `display`, `image`, `license`, `invocation_inputs/outputs`
- **Job:** `parameters`, `metrics`, `tool_stdout/stderr`
- **Meta:** `generate_time`, `generate_galaxy_version`, `invocation_time`
- **Instance:** 6 `instance_*_link` variants

#### Slide 7: Validation
**Type:** code-pattern
**Class:** reduce70
```python
def validate_galaxy_markdown(galaxy_markdown, internal=True):
    # Line-by-line fence tracking state machine
    for line, fenced, open_fence, line_no in _split_markdown_lines(markdown):
        if fenced and GALAXY_FUNC_CALL.match(line):
            _check_func_call(match, line_no)  # Validates args
    # Raises ValueError with line number on failure
```
**Code:** `lib/galaxy/managers/markdown_parse.py:validate_galaxy_markdown()`

---

### Section 3: Backend Rendering Pipeline (5 slides)

#### Slide 8: Transformation Pipeline
**Type:** diagram
**Class:** center
**Diagram:** Sequence diagram
1. **Import:** Decode external IDs → internal
2. **Validate:** Check syntax
3. **Resolve:** Expand workflow refs (`output="x"` → `history_dataset_id=123`)
4. **Export:** Collect metadata OR fully expand
5. **Render:** HTML / PDF / UI

#### Slide 9: Handler Pattern
**Type:** diagram
**Class:** center
**Diagram:** Class diagram
```
GalaxyInternalMarkdownDirectiveHandler (abstract)
├── ReadyForExportMarkdownDirectiveHandler
│   └── Lazy: collects metadata, preserves directives
└── ToBasicMarkdownDirectiveHandler
    └── Eager: fully expands to standard markdown
```
**Code:** `lib/galaxy/managers/markdown_util.py`

#### Slide 10: ID Encoding
**Type:** code-pattern
**Class:** reduce70
```python
# Storage (internal): numeric IDs
history_dataset_display(history_dataset_id=12345)

# Export (external): encoded IDs for URLs
history_dataset_display(history_dataset_id=a1b2c3d4e5f6)

# Regex patterns for conversion
UNENCODED_ID_PATTERN = r"(history_dataset_id)=([\d]+)"
ENCODED_ID_PATTERN = r"(history_dataset_id)=([a-z0-9]+)"
```

#### Slide 11: Invocation Resolution
**Type:** code-pattern
**Class:** reduce70
```python
# Input: workflow-relative references
invocation_outputs(output="alignment_results")
job_metrics(step="bwa_mem")

# Output: instance-specific IDs
history_dataset_display(history_dataset_id=98765)
job_metrics(job_id=54321)
```
**Code:** `lib/galaxy/managers/markdown_util.py:resolve_invocation_markdown()`

#### Slide 12: PDF Export
**Type:** diagram
**Class:** center
**Diagram:** Sequence
- `ToBasicMarkdownDirectiveHandler` → expands all directives
- `markdown.markdown()` → HTML
- `sanitize()` → security
- `WeasyPrint` → PDF
**Code:** `lib/galaxy/managers/markdown_util.py:internal_galaxy_markdown_to_pdf()`

---

### Section 4: Frontend Components (5 slides)

#### Slide 13: Component Tree
**Type:** diagram
**Class:** center
**Diagram:** Component tree
```
Markdown.vue
├── parseMarkdown() → Section[]
└── SectionWrapper (dispatcher)
    ├── MarkdownDefault (standard MD + KaTeX)
    ├── MarkdownGalaxy (Galaxy directives)
    ├── MarkdownVega (Vega-Lite specs)
    ├── MarkdownVisualization (Galaxy viz plugins)
    └── MarkdownVitessce (spatial data)
```
**Code:** `client/src/components/Markdown/Markdown.vue`

#### Slide 14: Section Parsing
**Type:** code-pattern
**Class:** reduce90
```typescript
// Triple-backtick splits content into typed sections
parseMarkdown(content) → [
  { type: 'markdown', content: '# Title...' },
  { type: 'galaxy', content: 'history_dataset_as_table(...)' },
  { type: 'vega', content: '{"$schema": "..."}' }
]
```
**Code:** `client/src/components/Markdown/parse.ts`

#### Slide 15: Galaxy Directive Processing
**Type:** diagram
**Class:** center
**Diagram:** Sequence
- Parse directive name + args
- Validate against mode (page vs report)
- Lookup data via stores (invocationStore, workflowStore)
- Render appropriate Element component
**Code:** `client/src/components/Markdown/Sections/MarkdownGalaxy.vue`

#### Slide 16: Element Components
**Type:** concept
**Class:** enlarge120
- **21+ specialized renderers:**
  - `HistoryDatasetAsTable`, `HistoryDatasetAsImage`
  - `WorkflowImage`, `WorkflowDisplay`
  - `JobMetrics`, `JobParameters`
  - `ToolStdout`, `ToolStderr`
- Each handles data fetching + rendering
**Code:** `client/src/components/Markdown/Sections/Elements/`

#### Slide 17: Store-Centric Data Flow
**Type:** diagram
**Class:** center
**Diagram:** Component diagram
- Elements → Pinia stores (invocationStore, workflowStore)
- Stores → API endpoints
- Caching prevents redundant fetches across elements

---

### Section 5: Editor Architecture (3 slides)

#### Slide 18: Dual-Mode Editor
**Type:** diagram
**Class:** center
**Diagram:** Component diagram
- **TextEditor:** Raw markdown, full control
- **CellEditor:** Jupyter-like, structured cells
  - Markdown cells (prose)
  - Galaxy directive cells (from palette)
  - Add/remove/reorder
**Code:** `client/src/components/Markdown/MarkdownEditor.vue`

#### Slide 19: Directive Registry
**Type:** code-pattern
**Class:** reduce90
```yaml
# directives.yml - metadata for editor UI
history_dataset_as_table:
  side_panel_name:
    page: "Dataset Table"
    report: "Output Table"
  help: "Embed dataset as formatted table..."

# templates.yml - insertion templates
history_dataset_as_table:
  template: 'history_dataset_as_table(history_dataset_id="%ID%")'
```
**Code:** `client/src/components/Markdown/directives.yml`

#### Slide 20: Mode-Aware Design
**Type:** concept
**Class:** enlarge120
- **Page mode:** Reference any workflow/dataset in instance
- **Report mode:** Reference "this" invocation (step labels)
- Same directives, different presentation and validation

---

### Section 6: Design & Extensibility (2 slides)

#### Slide 21: Design Principles
**Type:** diagram
**Class:** center
**Diagram:** Concept mindmap (YAML)
- **Contextual addressing:** multiple formats → internal IDs
  - Workflow: step/output labels
  - Tool: output references
  - API: encoded IDs
  - (Future) History: history-relative refs
- **Lazy resolution:** resolve at appropriate boundary
- **Handler extensibility:** add rendering contexts
- **Mode awareness:** pages vs reports vs tool outputs
- **Separation:** parse vs resolve, frontend vs backend

#### Slide 22: Adding a Directive
**Type:** code-pattern
**Class:** reduce70
```python
# 1. markdown_parse.py - add to ALLOWED_ARGUMENTS
ALLOWED_ARGUMENTS["new_directive"] = frozenset(["arg1", "arg2"])

# 2. markdown_util.py - add handler method
def handle_new_directive(self, ...):
    ...

# 3. Frontend - add element component
# client/src/components/Markdown/Sections/Elements/NewDirective.vue

# 4. directives.yml - add metadata
```

---

### Section 7: Summary (2 slides)

#### Slide 23: Architecture Overview
**Type:** diagram
**Class:** center
**Diagram:** Large end-to-end sequence or component diagram
- Workflow definition → markdown_util → Frontend → Rendered doc

#### Slide 24: Key Takeaways
**Type:** concept
**Class:** enlarge200
- **Portable:** Context-specific refs → internal IDs at boundaries
- **Extensible:** Handler pattern, directive registry, new contexts
- **Multi-format:** Same internal form → HTML, PDF, interactive UI
- **27+ directives** for embedding Galaxy objects

---

## Diagram TODO List (Priority Order)

### Must Have
1. ~~**Contextual Addressing Convergence** (Slide 2)~~ ✓
   - [images/markdown_contextual_addressing.plantuml.svg](../../images/markdown_contextual_addressing.plantuml.svg)

2. ~~**Transformation Pipeline** (Slide 8)~~ ✓
   - [images/markdown_transformation_pipeline.plantuml.svg](../../images/markdown_transformation_pipeline.plantuml.svg)

3. ~~**Handler Pattern** (Slide 9)~~ ✓
   - [images/markdown_handler_pattern.plantuml.svg](../../images/markdown_handler_pattern.plantuml.svg)

4. ~~**Frontend Component Tree** (Slide 13)~~ ✓
   - [images/markdown_frontend_components.plantuml.svg](../../images/markdown_frontend_components.plantuml.svg)

5. ~~**Design Principles** (Slide 21)~~ ✓
   - [images/markdown_design_principles.mindmap.plantuml.svg](../../images/markdown_design_principles.mindmap.plantuml.svg)

### Should Have
6. ~~**Parser Components** (Slide 4)~~ ✓
   - [images/markdown_parser_components.plantuml.svg](../../images/markdown_parser_components.plantuml.svg)

7. ~~**PDF Export Pipeline** (Slide 12)~~ ✓
   - [images/markdown_pdf_export.plantuml.svg](../../images/markdown_pdf_export.plantuml.svg)

8. ~~**Galaxy Directive Processing** (Slide 15)~~ ✓
   - [images/markdown_directive_processing.plantuml.svg](../../images/markdown_directive_processing.plantuml.svg)

9. ~~**Store Data Flow** (Slide 17)~~ ✓
   - [images/markdown_store_data_flow.plantuml.svg](../../images/markdown_store_data_flow.plantuml.svg)

10. ~~**Editor Architecture** (Slide 18)~~ ✓
    - [images/markdown_editor_architecture.plantuml.svg](../../images/markdown_editor_architecture.plantuml.svg)

### Nice to Have
11. ~~**Architecture Overview** (Slide 23)~~ ✓
    - [images/markdown_architecture_overview.plantuml.svg](../../images/markdown_architecture_overview.plantuml.svg)

---

## Next Steps

1. **Review this plan** - adjust slide count/content as needed
2. **Create diagrams** - start with Must Have list
3. **Write content.yaml** - implement slides with actual content
4. **Build and preview** - `make build-slides`

---

## User Preferences

- **Flow:** Architecture-First
- **Duration:** 30 min (~25 slides)
- **Audience:** Advanced Galaxy developers
- **Focus:** Technical depth, implementation details, code patterns
