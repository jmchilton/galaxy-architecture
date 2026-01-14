# Code Path: client/src/components/Markdown/Sections/Elements/

## Role in Architecture

Implements Galaxy-specific markdown rendering components that extend standard Markdown with interactive, data-driven elements. Dynamically loads and displays Galaxy objects (datasets, jobs, workflows, histories, invocations) within markdown documentation.

## Directory Structure

21 component files in two categories:
- **Main Elements** (16 files) - Core implementations
- **Workflow Subdirectory** (5 files) - Workflow-specific elements

## Key Element Types

### 1. Dataset Elements (6 components)
- `HistoryDatasetDisplay.vue` - Full dataset with type-aware rendering (PDF/HTML as iframe, images, tables, text)
- `HistoryDatasetDetails.vue` - Metadata extraction (name, info, peek, type)
- `HistoryDatasetAsTable.vue` - Tabular rendering with configurable headers/footers
- `HistoryDatasetAsImage.vue` - Image display
- `HistoryDatasetIndex.vue` - Collection/index display
- `HistoryDatasetLink.vue` - Clickable links with navigation

### 2. Job Elements (3 components)
- `JobMetrics.vue` - Performance metrics with optional AWS/carbon cost estimates
- `JobParameters.vue` - Execution parameters display
- `ToolStd.vue` - Tool stdout/stderr output

### 3. Workflow Elements (3 components)
- `WorkflowDisplay.vue` - Full visualization with step details
- `WorkflowImage.vue` - Diagram preview (sizes: sm/md/lg)
- `WorkflowLicense.vue` - Licensing information

### 4. Instance/Configuration Elements (5 components)
- `InstanceUrl.vue` - Dynamic instance URLs (7 types via `href` prop)

### 5. Invocation Elements (2 components)
- `InvocationTime.vue` - Workflow execution timestamp
- `HistoryLink.vue` - History import with one-click actions

### 6. Utility Elements (2 components)
- `TextContent.vue` - Simple text rendering (Galaxy version, current time)
- `JobSelection.vue` - Dropdown for selecting jobs from implicit collection

## Common Patterns Across Implementations

### 1. Three-Layer Data Architecture
- **Props Layer:** Minimal identifiers (IDs, configuration flags)
- **Store Layer:** Pinia stores for caching/state (`useDatasetStore`, `useJobStore`, etc.)
- **API Layer:** Direct axios calls or store-managed async operations

### 2. Reactive State Management
- Vue 3 Composition API (`computed`, `ref`, `watch`)
- Loading states tracked with `loading` refs
- Error states via `error` refs
- Cascading watchers for dependent data

### 3. Type Safety
- TypeScript with interface definitions for props
- Props validation via `defineProps<T>()`
- Type-aware rendering decisions

### 4. Content Variants & Conditional Rendering
- Type-aware rendering: datasets detect format (PDF/HTML/image/tabular/text)
- Expansion toggles: embed vs. expanded views with CSS constraints
- Loading states: `LoadingSpan` component
- Error boundaries: `BAlert` components

### 5. Dual Identity Pattern (Jobs)
`handlesMappingJobs.ts` composable enables elements to accept:
- Single `jobId` (direct job reference)
- `implicitCollectionJobsId` (batch jobs with dropdown selection)

Used by `JobMetrics`, `JobParameters`, `ToolStd` via `useMappingJobs()` hook.

### 6. Lazy Loading & Optimization
- Data fetched on-demand as components mount
- Pinia stores cache results to avoid duplicate requests
- Text content truncation with "Show More..." links
- Tabular data pagination (100 items per page default)

### 7. Bootstrap Vue Integration
All major UI uses `b-card`, `b-alert`, `b-table`, `b-button`. Consistent card-based layouts.

## Integration with MarkdownGalaxy

MarkdownGalaxy.vue dispatcher:

1. **Parses markdown directives** - Uses `parse.ts` to extract Galaxy blocks
2. **Validates elements** - Checks against `requirements.yml`
3. **Manages requirements** - Ensures required objects/labels present
4. **Conditionally renders** - Large if/else-if chain routing to 20+ element components
5. **Props mapping** - Extracts arguments from directive and passes to elements

**Directive Syntax:**
```
```galaxy
component_name(arg1="value", arg2="value")
```
```

**Requirements System:** (`requirements.yml`)
- Maps object types to element names
- Defines required vs. optional objects per element
- Enables validation: `hasValidObject()`, `hasValidName()`, `hasValidLabel()`

## Important Design Decisions

### 1. Store-Centric Architecture
Pinia stores provide single source of truth. Prevents N+1 API calls. Cache-friendly.

### 2. Progressive Enhancement
Base elements work without invocation context. Optional invocation parsing provides richer data. Graceful fallbacks.

### 3. Type Awareness as First-Class
`useDatatypesMapperStore()` provides datatype hierarchy queries. Dataset rendering adapts to file type.

### 4. Composition Over Inheritance
No shared base component. Utility functions reused via composition. Clean separation.

### 5. Embedded vs. Full Display
Most elements support `embedded` flag for size-constrained rendering. CSS-based constraints.

### 6. Error Resilience
All async operations wrapped in try-catch. User-facing error messages via BAlert. Never silent failures.

## Data Flow Example: HistoryDatasetDisplay

```
User sees: <history_dataset_display dataset_id="..." />
           ↓
Parsed as: { name: "history_dataset_display", args: { ... } }
           ↓
MarkdownGalaxy validates, routes to HistoryDatasetDisplay.vue
           ↓
Component loads:
  - Metadata from useDatasetStore
  - Content from useDatasetTextContentStore
  - Datatypes from useDatatypesMapperStore
           ↓
Rendering decision:
  - PDF/HTML → iframe embed
  - Image → HistoryDatasetAsImage
  - Tabular → b-table with pagination
  - Otherwise → <pre> code block
           ↓
Fully rendered, interactive element
```

## Documentation Highlights

**For training:**
- Store-centric architecture for performance
- Progressive enhancement with graceful fallbacks
- Type-aware rendering adapts to data formats
- Dual identity pattern for job collections
- Bootstrap Vue for consistent UI
- Error resilience with user-facing messages
