# Code Path: client/src/components/Markdown/Markdown.vue

## Component Role

Main markdown renderer and document orchestrator in Galaxy's client interface. Transforms raw markdown configuration (narrative content + Galaxy directives) into fully-rendered, interactive document with metadata display, export capabilities, and user actions.

## High-Level Design Pattern

```
MarkdownConfig Input
    ↓
parseMarkdown() → Section objects[]
    ↓
SectionWrapper dispatcher
    ↓
Specialized renderers (Default/Galaxy/Vega/Visualization/Vitessce)
    ↓
Rendered UI + Actions (Edit, Export, Metadata)
```

## Key Responsibilities

### 1. Configuration Management
Receives `MarkdownConfig` object containing:
- `content` or `markdown`: Raw markdown with embedded Galaxy directives
- `errors`: Parsing/validation errors from backend
- Metadata: `title`, `id`, `update_time`, `generate_version`, `model_class`

Props control export options, edit capability, download mechanisms.

### 2. Content Parsing & Segmentation
- Calls `parseMarkdown()` which splits input by triple-backtick delimiters
- Segments content into typed sections (e.g., `markdown`, `galaxy`, `vega`)
- Each section becomes discrete rendering unit

### 3. Section Routing & Rendering
Delegates to `SectionWrapper` which dispatches to appropriate renderer:
- **MarkdownDefault:** Standard markdown via markdown-it (with KaTeX for math)
- **MarkdownGalaxy:** Galaxy directives (job results, workflow outputs, dataset tables)
- **MarkdownVega:** Data visualizations via Vega grammar
- **MarkdownVisualization:** Galaxy built-in interactive visualizations
- **MarkdownVitessce:** Spatial/single-cell data viewers
- Falls back to error alert for unknown types

### 4. User Interactions
- **Edit button:** Emits `onEdit` event (parent handles editing mode)
- **Export/Download:** Two strategies:
  - Direct download via endpoint (if `directDownloadLink=true`)
  - STS-based secure download (fallback mechanism)
- Both respect feature flag `enable_beta_markdown_export`

### 5. Status Display & Error Handling
- **Loading state:** Shows spinner while parsing
- **Error alerts:** Displays backend parsing errors (with message + line)
- **Metadata footer:** Shows last update timestamp (UTC formatted) and document ID
- **Sticky header:** Page title and action buttons remain visible during scroll

## Core Props Interface

```typescript
interface MarkdownConfig {
    content?: string;              // Raw markdown
    markdown?: string;             // Alternative to content
    errors?: Array<{error, line}>; // Parsing errors
    title?: string;                // Document title
    id?: string;                   // Document identifier
    update_time?: string;          // ISO timestamp
    generate_time?: string;        // Ignored (uses update_time)
    generate_version?: string;     // Backend version
    model_class?: string;          // Fallback if title not provided
}

// Component props
enable_beta_markdown_export: boolean;
downloadEndpoint: string;           // URL for PDF generation
readOnly?: boolean;                 // Disable edit button
exportLink?: string;                // Fallback export link
directDownloadLink?: boolean;       // Choose download strategy
```

## Data & State

| Ref | Type | Purpose |
|-----|------|---------|
| `markdownObjects` | `any[]` | Parsed section objects from parseMarkdown() |
| `markdownErrors` | `any[]` | Accumulated parsing errors |
| `loading` | `boolean` | Tracks parse completion |

## Computed Properties

| Property | Purpose |
|----------|---------|
| `effectiveExportLink` | Returns export link only if beta feature enabled |
| `updateTime` | ISO → human-readable locale string (UTC) |
| `pageTitle` | Title or model_class fallback |

## Methods

```typescript
initConfig()
  // Triggered on mount and config prop change
  // Extracts markdown, parses sections, clears loading

onDirectGeneratePDF()
  // Window redirect to downloadEndpoint
  // Used when directDownloadLink=true
```

## Lifecycle & Reactivity

```typescript
onMounted() → initConfig()
watch(markdownConfig) → initConfig()
  // Reactive to config changes (enables live preview)
```

## Layout Structure

```html
<div class="markdown-wrapper">
  [Loading spinner OR]
  <sticky-header>
    <h1>{{ pageTitle }}</h1>
    [Export button | Edit button]
  </sticky-header>

  [Error alerts]

  <section.markdown-component>
    <SectionWrapper v-for=section>

  <transparent-scroll-overlay/>

  <footer>
    Last updated + Identifier
  </footer>
</div>
```

## Integration Points

**Upstream (Parent Components):**
- Receives `markdownConfig` from parent (workflow context, notebook, history item)
- Emits `onEdit` when user clicks edit
- Unidirectional data flow

**Downstream (Section Renderers):**
- Parsing delegated to `parseMarkdown()` utility
- Section-specific validation in MarkdownGalaxy
- Galaxy directives: `` ```galaxy_function(arg1="val1") ... ``` ``

**Stores Consumed:**
- MarkdownGalaxy uses: `invocationStore`, `workflowStore`, `config`
- Enables rich rendering of job/workflow/dataset context

## Design Decisions

1. **Separation of concerns:** Parsing isolated in `parse.ts`, rendering delegated to specialized components
2. **Graceful degradation:** Unknown section types show error alert instead of breaking
3. **Lazy validation:** Backend provides errors; frontend validates Galaxy directives on render
4. **Export strategy polymorphism:** Two download paths chosen per-instance
5. **Sticky UI:** Header remains visible during scroll
6. **Timestamp normalization:** Handles both `update_time` and `generate_time`, renders in user's locale

## Example Configuration

```javascript
{
  title: "My Analysis Results",
  id: "abc123xyz",
  update_time: "2025-11-28T14:32:00Z",
  markdown: `
# Results Summary

\`\`\`galaxy
history_dataset_as_table(history_dataset_id="dataset-456", title="Expression Matrix")
\`\`\`

\`\`\`vega
{"$schema": "https://vega.github.io/schema/vega/v5.json", ...}
\`\`\`
  `,
  errors: []
}
```

## Documentation Highlights

**For training:**
- Multi-format support: markdown is structural container for domain-specific directives
- Error transparency: parsing errors bubble to UI immediately
- Extensibility: adding new section types straightforward
- State locality: minimal component state, logic in specialized children
- Performance: computed properties defer timezone formatting
