# Code Path: client/src/components/Markdown/MarkdownEditor.vue

## Component Role

Primary entry point for markdown editing in Galaxy's workflow and page documentation. Smart wrapper coordinating between two fundamentally different editing modes.

## Architecture Pattern: Modal Switching

Dual-mode coordinator pattern:

```
MarkdownEditor (coordinator)
├── TextEditor (raw markdown)
│   ├── MarkdownToolBox (insertion helper panel)
│   └── textarea (direct content editing)
└── CellEditor (structured content)
    ├── CellWrapper[] (individual content units)
    ├── CellAdd (insertion UI)
    └── Configuration components
```

**Key Design:** Mode selection depends on context:
- If `labels` prop undefined → text mode only
- If `labels` prop provided → both modes available (workflow report context)

## Props and Configuration

```typescript
markdownText: string;        // Actual markdown content
mode: "report" | "page";     // Context: workflow report or page
labels?: WorkflowLabel[];    // Optional: workflow step/input/output labels
steps?: Record<string, any>; // Workflow step metadata
title: string;               // Display title in header
```

**WorkflowLabel Interface:**
```typescript
interface WorkflowLabel {
    label: string;
    type: "input" | "output" | "step";
}
```

## Data Flow and State Management

**Single Source of Truth:** Parent owns `markdownText`; MarkdownEditor doesn't modify directly.

**Update Mechanism:**
- Both child editors emit `@update` events
- Parent receives via `$emit('update', $event)` passthrough
- Changes flow up to parent state

**Event Emission:**
```javascript
// TextEditor or CellEditor → MarkdownEditor → Parent
emit("update", updatedMarkdownString)
```

## TextEditor Mode: Raw Markdown with Tooling

**Architecture:**
```
TextEditor
├── MarkdownToolBox (left sidebar)
│   ├── ToolSection[] (categorized directives)
│   ├── MarkdownDialog (selection/configuration)
│   └── Directive handlers
└── textarea (right panel)
    ├── Direct editing
    ├── Cursor position preservation
    └── Debounced updates (300ms)
```

**Key Features:**
- Two-panel layout: MarkdownToolBox left, textarea right
- Insert mechanism: Toolbox provides Galaxy directives
- Smart insertion: Wraps in code fence with `galaxy` tag
- Cursor preservation on parent updates
- Debounced updates (300ms) prevents excessive re-renders

## CellEditor Mode: Structured Cell-Based Editing

**Architecture:**
```
CellEditor
├── CellAdd (top)
├── [CellWrapper (expandable)]
│   ├── CellButton (toggle/collapse)
│   ├── SectionWrapper (preview)
│   ├── CellAction (clone/delete/move)
│   ├── CellCode (syntax-highlighted editor)
│   └── ConfigureGalaxy/Visualization/Vitessce
├── CellAdd (bottom)
```

**Cell Concept:** Decomposes markdown into discrete units

**Parsing:** Uses `parseMarkdown()` - splits on ` ``` ` delimiters

**Core Operations:**
- Add, Change, Clone, Delete, Move, Configure, Toggle

**Update Serialization:** `onUpdate()` reconstructs markdown from cells

## CellWrapper: Individual Cell Container

**Responsibilities:**
- Render cell preview (collapsed)
- Expand to show full content editor
- Toggle configuration panel for data-aware cells
- Provide action buttons (clone, delete, move)
- Apply syntax highlighting based on cell type

**Conditional Configuration:**
- `ConfigureGalaxy` → For galaxy directives
- `ConfigureVisualization` → For vega/visualization blocks
- `ConfigureVitessce` → For Vitessce configuration

## MarkdownToolBox: Directive Insertion Interface

**Role:** Tool palette for inserting Galaxy directives in text mode

**Structure:** ActivityPanel with tool sections:
- History objects: dataset display, images, tables, links
- Job metadata: parameters, metrics, stdout/stderr
- Workflow elements: invocation metadata, workflow info
- Links section
- Visualizations (conditional)

**Interaction Flow:**
1. User clicks tool item
2. `MarkdownDialog` opens for parameter configuration
3. Dialog captures context-specific data
4. On confirm, emits markdown string
5. TextEditor inserts at cursor

## Integration Points

**With Parent:**
- Receives props from parent holding markdown state
- Emits `update` event for state management
- Unidirectional data flow

**With Markdown Rendering:**
- Uses `SectionWrapper` for cell preview
- Integrates with `MarkdownDefault/Galaxy/Vega` for display
- Shares parse logic with rendering pipeline

**With Workflow System:**
- Accepts `WorkflowLabel` array for workflow context
- Conditional UI based on workflow context

## Important Patterns

### Content Ownership
Parent owns state; editor is controlled component. Updates flow through events.

### Mode Visibility Logic
```javascript
const hasLabels = computed(() => props.labels !== undefined);
```

### Debouncing Strategy
TextEditor debounces textarea input (300ms). Reduces parent re-render frequency.

### Cursor Preservation (TextEditor)
Watches parent `markdownText` changes. Preserves cursor position using `nextTick()`.

### Smooth Scrolling (CellEditor)
Auto-scrolls to newly added/moved cells. Uses `scrollIntoView({ behavior: "smooth" })`.

### Type Safety in Cell Operations
Cells deeply copied during mutations. Prevents Vue reactivity issues.

### Lazy Component Loading
CellCode loaded dynamically: `const CellCode = () => import("./CellCode.vue")`. Reduces bundle size.

## Documentation Highlights

**For training:**
- Dual-mode architecture (text vs cell)
- Content ownership pattern (parent state)
- Debouncing for performance
- Cursor preservation in text mode
- Cell-based structure in workflow reports
- Lazy loading for code editor
