# PR-Based Slide Plan: Galaxy Markdown Evolution

Based on analysis of 18 PRs spanning 2019-2025, telling the story of Galaxy Markdown's evolution.

## Phase 1: Foundation (2019) - 6 slides

### Slide 1: Timeline Overview
**Type:** diagram
**Content idea:** Evolution of Galaxy Markdown from 2019 to 2025 with major milestones.
**Proposed Diagram:** Mermaid timeline
- 2019: Initial reports (#8543)
- 2020: PDF export, metadata, visualizations
- 2023: Tool integration
- 2024-25: Cell editor, validation, modernization
**Class:** center

### Slide 2: The Problem - Portability
**Type:** concept
**Content idea:** HTML reports lock to instance; sharing workflows means losing documentation.
**Class:** enlarge150
**PR Reference:** #8543

### Slide 3: Community Syntax Decision
**Type:** quote
**Content idea:** Community voted for fenced code blocks with `galaxy` identifier.
**Class:** enlarge120
```markdown
```galaxy
directive_name(arg=value)
```
```
**PR Reference:** #8543

### Slide 4: Two-Stage Architecture
**Type:** diagram
**Content idea:** Workflow Markdown (labels) → Galaxy Markdown (IDs) enables portability.
**Proposed Diagram:** Sequence showing transformation
- Workflow: `output="results"` (travels with workflow)
- Galaxy: `history_dataset_id=12345` (renders on instance)
**Class:** center
**PR Reference:** #8543

### Slide 5: Initial Directives
**Type:** concept
**Content idea:** First batch: dataset display, workflow embedding, job metrics.
**Class:** enlarge120
- `history_dataset_display`, `_as_image`, `_peek`, `_info`
- `workflow_display`, `job_parameters`, `job_metrics`
- `tool_stdout`, `tool_stderr`
- `invocation_inputs`, `invocation_outputs`
**PR Reference:** #8543

### Slide 6: Client-Side Rendering
**Type:** diagram
**Content idea:** Backend generates neutral format; Vue components handle rendering.
**Proposed Diagram:** Component diagram
- Backend: markdown_util.py → neutral Galaxy Markdown
- Frontend: Markdown.vue → rendered UI
**Class:** center
**PR Reference:** #8543

---

## Phase 2: Making it Portable (2019-2020) - 4 slides

### Slide 7: Export Challenge
**Type:** concept
**Content idea:** Reports need to work outside Galaxy - PDF export requirement.
**Class:** enlarge150
**PR Reference:** #8893

### Slide 8: PDF Export Pipeline
**Type:** diagram
**Content idea:** Five-stage transformation: Galaxy → basic markdown → HTML → sanitized → PDF.
**Proposed Diagram:** Sequence diagram
- ToBasicMarkdownDirectiveHandler fully expands
- markdown.markdown() converts
- Sanitize HTML for security
- WeasyPrint renders PDF
**Class:** center
**PR Reference:** #8893

### Slide 9: The to_basic_markdown Transform
**Type:** code-pattern
**Content idea:** Directives expand to standard markdown: tables, embedded images, formatted text.
**Class:** reduce70
```python
# Galaxy Markdown:
history_dataset_as_table(history_dataset_id=123)

# Basic Markdown (after transform):
| Column A | Column B |
|----------|----------|
| data     | values   |
```
**PR Reference:** #8893

### Slide 10: Security Layer
**Type:** concept
**Content idea:** HTML sanitization prevents XSS; encoded IDs prevent enumeration.
**Class:** enlarge120
**PR Reference:** #8893

---

## Phase 3: Expanding Capabilities (2020-2023) - 7 slides

### Slide 11: Metadata Directives
**Type:** concept
**Content idea:** Provenance: when generated, Galaxy version, invocation timestamp.
**Class:** enlarge120
- `generate_time` - document creation time
- `generate_galaxy_version` - Galaxy version
- `invocation_time` - workflow run timestamp
- `history_dataset_name`, `_type` - dataset metadata
**PR Reference:** #9938

### Slide 12: Interactive Visualizations
**Type:** diagram
**Content idea:** Pages can embed interactive visualizations, not just static content.
**Proposed Diagram:** Component diagram showing viz embedding
- Markdown provides structure + dataset reference
- Visualization component handles interactivity
**Class:** center
**PR Reference:** #10288

### Slide 13: Reports vs Pages
**Type:** concept
**Content idea:** Reports are workflow outputs (immutable); Pages are user documents (editable).
**Class:** enlarge150
- Reports: scoped to invocation, read-only
- Pages: reference any object, editable, versioned
**PR Reference:** #10241

### Slide 14: Workflow Diagram Embedding
**Type:** code-pattern
**Content idea:** SVG workflow visualization embedded directly in documents.
**Class:** reduce90
```galaxy
workflow_image(workflow_id=abc123)
```
**PR Reference:** #10241

### Slide 15: Instance Links
**Type:** concept
**Content idea:** Link to Galaxy help, citations, terms of service - configurable per instance.
**Class:** enlarge120
- `instance_access_link`, `instance_help_link`
- `instance_citation_link`, `instance_terms_link`
**PR Reference:** #16672

### Slide 16: Dataset Tables
**Type:** code-pattern
**Content idea:** Tabular data rendered as formatted HTML tables.
**Class:** reduce90
```galaxy
history_dataset_as_table(history_dataset_id=123, title="Results")
```
**PR Reference:** #16675

### Slide 17: Context-Aware Help
**Type:** diagram
**Content idea:** Single source of truth: directives.yml provides help text for editor UI.
**Proposed Diagram:** Component diagram
- directives.yml: metadata registry
- Mode-specific help (page vs report)
- TypeScript integration
**Class:** center
**PR Reference:** #16681

---

## Phase 4: Tool Integration (2024-2025) - 4 slides

### Slide 18: Tool HTML Output Problems
**Type:** concept
**Content idea:** HTML tool outputs have security risks, limited portability, inconsistent styling.
**Class:** enlarge150
**PR Reference:** #17228

### Slide 19: Tool Markdown Reports
**Type:** diagram
**Content idea:** Tools can output Galaxy Markdown instead of HTML - safe, portable, styled.
**Proposed Diagram:** Sequence showing tool → markdown → rendered output
**Class:** center
**PR Reference:** #17228

### Slide 20: Two Output Patterns
**Type:** code-pattern
**Content idea:** Output references (explicit dataset) vs extra files (tool-generated markdown).
**Class:** reduce70
**PR Reference:** #17228

### Slide 21: Inline Directives
**Type:** code-pattern
**Content idea:** Embed directives in flowing text: `${galaxy history_dataset_name(...)}`.
**Class:** reduce90
```markdown
Analysis of ${galaxy history_dataset_name(output="results")} shows...
```
**PR Reference:** #17228

---

## Phase 5: Modern Editing (2024-2025) - 9 slides

### Slide 22: Component Modularization
**Type:** diagram
**Content idea:** Refactored to subdirectories for modularity, reactivity, caching.
**Proposed Diagram:** File mindmap (YAML)
- client/src/components/Markdown/
  - Sections/ (Default, Galaxy, Vega, etc.)
  - Editor/ (TextEditor, CellEditor)
  - Elements/ (21+ element types)
**Class:** center
**PR Reference:** #19719

### Slide 23: Direct Resource Endpoints
**Type:** diagram
**Content idea:** Components fetch directly from APIs, not through Pages API mediation.
**Proposed Diagram:** Before/after component diagram
- Before: Component → Pages API → Resource
- After: Component → Resource API (with caching)
**Class:** center
**PR Reference:** #19719

### Slide 24: Caching Layer
**Type:** concept
**Content idea:** Simple caching prevents redundant requests for complex documents.
**Class:** enlarge120
**PR Reference:** #19719

### Slide 25: Lazy Client-Side Resolution
**Type:** diagram
**Content idea:** Labels preserved client-side; resolved lazily when data needed.
**Proposed Diagram:** Mermaid flowchart
- Keep both label AND ID in markdown
- Resolve label → ID at render time
- Enables preview during editing
**Class:** center
**PR Reference:** #19721

### Slide 26: Cell-Based Editor
**Type:** diagram
**Content idea:** Jupyter-like experience: cells for markdown and Galaxy directives.
**Proposed Diagram:** Mockup or component diagram
- Add/remove/reorder cells
- Markdown cells: prose
- Galaxy cells: directive from palette
- Live preview
**Class:** center
**PR Reference:** #19769

### Slide 27: Visualization Framework
**Type:** concept
**Content idea:** Vega, Vitessce, Galaxy visualizations all supported as section types.
**Class:** enlarge120
- `vega` blocks: Vega-Lite specs
- `vitessce` blocks: spatial data
- `visualization` blocks: Galaxy viz plugins
**PR Reference:** #19775

### Slide 28: Validation & Alerts
**Type:** diagram
**Content idea:** Context-aware validation catches errors during editing.
**Proposed Diagram:** Flowchart
- Available in this mode?
- Valid object reference?
- Show alert with guidance
**Class:** center
**PR Reference:** #19952

### Slide 29: Math Equations
**Type:** code-pattern
**Content idea:** KaTeX support for mathematical notation.
**Class:** enlarge120
```markdown
The formula $E = mc^2$ explains...
```
**PR Reference:** #19988

### Slide 30: Modern Page Creation
**Type:** diagram
**Content idea:** New frontend page creation flow with Vue 3 composition API.
**Proposed Diagram:** Before/after sequence
- Before: Backend-driven form
- After: Vue 3 reactive form with stores
**Class:** center
**PR Reference:** #19914

---

## Phase 6: Summary & Architecture (6 slides)

### Slide 31: Design Principles
**Type:** diagram
**Content idea:** Core architectural decisions emerged from evolution.
**Proposed Diagram:** Concept mindmap (YAML)
- Two-layer addressing
- Lazy resolution
- Handler extensibility
- Mode awareness
- Separation of concerns
**Class:** center

### Slide 32: Three Document Types
**Type:** diagram
**Content idea:** Reports, Pages, Tool Outputs - capabilities and trust boundaries.
**Proposed Diagram:** Mermaid matrix or table
| Type | Editable | Scope | Trust |
|------|----------|-------|-------|
| Reports | No | Invocation | Workflow |
| Pages | Yes | Any | User |
| Tool Output | No | Job | Tool |
**Class:** center

### Slide 33: Complete Transformation Pipeline
**Type:** diagram
**Content idea:** Full pipeline from workflow definition to rendered document.
**Proposed Diagram:** Large sequence diagram
- Workflow Definition (labels)
- populate_invocation_markdown()
- resolve_invocation_markdown()
- ReadyForExport / ToBasicMarkdown
- Frontend rendering
**Class:** center

### Slide 34: Frontend Component Tree
**Type:** diagram
**Content idea:** Complete component architecture.
**Proposed Diagram:** Component tree
- Markdown.vue → SectionWrapper → Renderers
- MarkdownEditor.vue → TextEditor / CellEditor
- 21+ Element components
**Class:** center

### Slide 35: 30+ Directives Ecosystem
**Type:** concept
**Content idea:** Rich directive library for embedding Galaxy objects.
**Class:** enlarge120
- Datasets (8): display, image, table, peek, info, link, name, type
- Workflows (5): display, image, license, inputs, outputs
- Jobs (4): parameters, metrics, stdout, stderr
- Meta (4): time, version, invocation_time, history_link
- Instance (6): access, help, citation, terms, resources, support links

### Slide 36: Evolution Success
**Type:** concept
**Content idea:** From simple reports to comprehensive documentation platform.
**Class:** enlarge200
- 2019: Basic workflow reports
- 2025: Full editing, validation, multi-format, interactive

---

## Slide 37: Future Directions
**Type:** concept
**Content idea:** Where Galaxy Markdown is heading.
**Class:** enlarge150
- More visualization types
- Collaborative editing
- Template library
- AI-assisted report generation

---

## Diagram TODO List

### 1. Evolution Timeline
**Type:** Mermaid timeline
**Elements:** 2019 foundation, 2020 export, 2023 tools, 2024-25 editor
**Reference:** See MERMAID.md for timeline syntax

### 2. Two-Stage Transformation
**Type:** Sequence diagram
**Participants:** Workflow Definition, markdown_util, Galaxy Markdown
**Key elements:** Label → ID transformation, portability

### 3. Client-Server Rendering Split
**Type:** Component diagram
**Components:** Backend (markdown_util), Frontend (Markdown.vue)
**Key elements:** Neutral format between them

### 4. PDF Export Pipeline
**Type:** Sequence diagram
**Participants:** Galaxy MD, ToBasicMarkdown, markdown lib, sanitizer, WeasyPrint
**Key elements:** Five transformation stages

### 5. Reports vs Pages
**Type:** Comparison diagram or matrix
**Elements:** Mutability, scope, trust level, capabilities

### 6. Help System Architecture
**Type:** Component diagram
**Components:** directives.yml, directives.ts, Editor UI
**Key elements:** Mode-specific help, TypeScript types

### 7. Tool Markdown Flow
**Type:** Sequence diagram
**Participants:** Tool, output markdown, sandbox, renderer
**Key elements:** Safety boundary

### 8. Component Modularization
**Type:** File mindmap (YAML)
**Elements:** Directory structure with component purposes

### 9. Before/After API Flow
**Type:** Two sequence diagrams
**Participants:** Component, Pages API (before), Resource API (after)
**Key elements:** Caching, direct access

### 10. Reference Resolution Flow
**Type:** Mermaid flowchart
**Elements:** Keep label, resolve lazily, enable preview

### 11. Cell Editor Mockup
**Type:** Diagram or mockup
**Elements:** Cell types, add/remove, palette, preview

### 12. Validation Flow
**Type:** Mermaid flowchart
**Elements:** Mode check, reference check, alert display

### 13. Design Principles Mindmap
**Type:** Concept mindmap (YAML)
**Elements:** Core architectural principles

### 14. Capabilities Matrix
**Type:** Mermaid or table
**Elements:** Document types vs features

### 15. Complete Pipeline
**Type:** Large sequence diagram
**Participants:** All major components
**Reference:** Similar to asgi_app.plantuml.txt

### 16. Component Tree
**Type:** Tree diagram
**Components:** All frontend components hierarchically
