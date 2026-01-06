# Code Path: client/src/components/Markdown/Editor/

## Role in Architecture

Vue 3 component system enabling structured markdown editing as a sequence of editable "cells". Provides notebook-like interface with support for templates, syntax highlighting, and data configuration.

## Key Architecture Components

### 1. CellEditor (Root Container)
**File:** `CellEditor.vue`

**Purpose:** Top-level orchestrating component

**Key Responsibilities:**
- Parses markdown text into cells using `parseMarkdown()`
- Manages cell array state
- Routes cell events (add, delete, move, clone, configure, toggle, update)
- Emits updated markdown to parent via `update` event
- Handles smooth scrolling to modified cells

**Design Pattern:** Container component following state container pattern, delegating UI to CellWrapper.

### 2. CellWrapper (Cell Container & UI Controller)
**File:** `CellWrapper.vue`

**Purpose:** Wraps individual cells and manages expanded/collapsed state

**Key Features:**
- Expand/collapse toggle via `toggle` prop
- Hover state highlights
- Content rendering via SectionWrapper (markdown) or CellCode (executable)
- Mode detection: auto-selects editor mode (python, markdown, json)
- Configuration UI routing based on cell type

**Structure:** Two-row layout when expanded:
```
Row 1: [Toggle] [Editor] [Type Label]
Row 2: [Actions] [Config UI or Code Editor]
```

### 3. Cell UI Components

**CellButton** - Icon buttons with tooltips, three states (active/inactive/hidden)

**CellAdd** - Floating action button (+) positioned between cells
- Searchable dropdown with categorized templates
- Dynamic visualization templates from Galaxy API
- Emits full `CellType` to parent

**CellAction** - Hamburger menu for cell operations
- Operations: Clone, Delete, Move Up/Down
- Confirmation modal for destructive actions
- Context-aware (disables Move at boundaries)

**CellCode** - Ace editor wrapper with syntax highlighting
- Props: `mode`, `maxLines`, `value`
- Debounced change emission (300ms)
- Focus/blur visual feedback
- Dynamically loads Ace language/theme modules

**CellOption** - Reusable menu item
- Displays title, description, optional icon/logo
- Used in CellAdd templates and CellAction menus

### 4. Configuration Components (Pluggable Architecture)
Located in `Configurations/`, mapped by cell type:

**ConfigureGalaxy.vue** - For `galaxy` cells
- Parses function names and arguments
- Selector UI for choosing datasets/invocations
- Validates required parameters
- Emits function call with parameters

**ConfigureVisualization.vue** - For `visualization` cells
- JSON configuration editor
- Galaxy visualization plugin integration

**ConfigureVitessce.vue** - For `vitessce` cells
- Complex JSON configuration
- Vitessce visualization specs

**ConfigureHeader.vue** - Shared UI header

**ConfigureSelector.vue** - Reusable dropdown for data elements

## Supported Cell Types

| Type | Purpose | Configurable |
|------|---------|--------------|
| `markdown` | Document content, headings, lists, equations | No |
| `galaxy` | Display workflows, datasets, metrics, parameters | Yes |
| `vega` | Vega-lite visualizations (charts) | No |
| `visualization` | Dynamic Galaxy visualization plugins | Yes |
| `vitessce` | Interactive spatial data viewer | Yes |

## Common Patterns

### Event Flow Pattern
```
CellEditor (state)
  → emits: @change, @move, @delete, @clone, @configure, @toggle
  ← receives: onAdd, onDelete, onChange, onMove

CellWrapper (child state)
  → emits: change, move, delete, clone, configure, toggle
  ← receives: cell-index, content, labels
```

### Props Propagation
- `labels` (WorkflowLabel[]): Workflow context through editor → wrapper → configs
- `content`: Cell markdown/code, bidirectionally synced
- `name`: Cell type identifier for routing
- `configure`: Boolean toggle for configuration UI

### Content Parsing & Serialization
- **Input:** Markdown with fenced code blocks: ` ```type\ncontent\n``` `
- **Parsing:** `parseMarkdown()` converts to `CellType[]`
- **Serialization:** `onUpdate()` reconstructs markdown from cells
- **Type Safety:** `getArgs()` parses Galaxy function calls

### Debounced Updates
- `CellCode`: 300ms debounce on change
- `TextEditor`: 300ms debounce on content update
- Prevents excessive re-renders during typing

### Template System
- `templates.yml`: Categorized templates (Markdown, Galaxy, Vega, Vitessce)
- `getVisualizations()`: Async API call for dynamic templates
- `CellAdd`: Filters and displays templates with search

## Design Decisions

### Cell as State Unit
Each cell independent with minimal coupling. State mutations copy arrays for Vue reactivity.

### Toggle vs. Expand Pattern
`toggle` property controls visibility of cell controls. Reduces cognitive load for read-only views.

### Configuration as Plugin System
Configuration UI pluggable via `configureComponent` computed property. New cell types can be added without modifying core logic.

### Content Type Switching
Mode detection uses cell `name` to determine editor mode automatically. No manual selection.

### Markdown as Serialization Format
Preserves markdown fencing for compatibility with Galaxy ecosystem. Allows Jupyter-style integration.

### Lazy-loaded Code Editor
CellCode uses dynamic import: `() => import("./CellCode.vue")`. Reduces bundle size.

## Integration Points

- **Parent:** Receives markdown string, emits updated markdown
- **API:** `getVisualizations()` fetches Galaxy plugin catalog
- **Markdown Parser:** `parseMarkdown()` from sibling component
- **Galaxy Context:** `WorkflowLabel` provides invocation/dataset context
- **Editor Engine:** Ace.js for syntax highlighting
- **UI Framework:** Bootstrap Vue

## File Structure

```
Editor/
├── CellEditor.vue              # Root container
├── CellWrapper.vue             # Cell UI controller
├── CellAdd.vue                 # Template insertion
├── CellAction.vue              # Operations menu
├── CellCode.vue                # Ace editor wrapper
├── CellButton.vue              # Icon button primitive
├── CellOption.vue              # Menu item primitive
├── TextEditor.vue              # Plain textarea variant
├── types.ts                    # TypeScript interfaces
├── services.ts                 # API integration
├── templates.yml               # Built-in cell templates
└── Configurations/
    ├── ConfigureGalaxy.vue
    ├── ConfigureVisualization.vue
    ├── ConfigureVitessce.vue
    ├── ConfigureHeader.vue
    └── ConfigureSelector.vue
```

## Documentation Highlights

**For training:**
- Cell-based editing mirrors Jupyter notebooks
- Pluggable configuration system
- Template system for quick insertion
- Debouncing for performance
- Lazy loading reduces bundle size
- Clean separation of concerns
