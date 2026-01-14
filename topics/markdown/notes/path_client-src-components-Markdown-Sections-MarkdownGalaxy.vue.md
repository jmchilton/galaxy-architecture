# Code Path: client/src/components/Markdown/Sections/MarkdownGalaxy.vue

## Component Role

Central directive renderer for Galaxy's markdown documentation system. Processes special `galaxy` code blocks containing Galaxy directives and dynamically renders appropriate components based on directive types.

**Core Responsibility:** Transform Galaxy directives (e.g., `history_dataset_as_table(history_dataset_id="123", compact=true)`) into interactive UI elements that visualize Galaxy runtime objects.

## Directive Syntax

**Fenced Block Directives:**
```markdown
```galaxy
directive_name(arg1="value1", arg2="value2")
```
```

**Inline Embed Directives:**
```markdown
Text with ${galaxy history_dataset_name(invocation_id=ABC)} embedded.
```

**Parsing Rules:**
- Argument values support quoted and unquoted formats: `"double"`, `'single'`, or bare values
- Regex-based parser extracts function name and arguments
- Validation ensures directive name is registered in `requirements.yml`

## Processing Pipeline

```
Input (markdown content)
   ↓
getArgs() - Parse directive structure
   ↓
handleAttributes() - Extract name & args
   ↓
Validation checks - Name, labels, required objects
   ↓
Dynamic rendering - Route to appropriate component
   ↓
Output - Interactive UI element
```

## Key Props

| Prop | Type | Purpose |
|------|------|---------|
| `content` | String (required) | Raw directive text from markdown block |
| `labels` | Array (optional) | Workflow labels for validating `input`, `output`, `step` references |

## Core Data & Methods

### Reactive Data
```javascript
attributes       // Parsed directive args: { name, args }
error           // User-facing error messages
toggle          // Collapse/expand state
workflowLoading // Workflow fetch in progress
```

### Key Computed Properties

| Property | Purpose |
|----------|---------|
| `args` | Merges invocation data with directive args |
| `invocation` | Fetches from store by ID |
| `workflowId` | Resolves from invocation |
| `isCollapsible` | `args.collapse !== undefined` |
| `isVisible` | Shows content when uncollapsed |
| `compact` | `Boolean(args.compact)` - Dense layouts |

### Key Methods

**handleAttributes()** - Parses directive
- Calls `getArgs(content)` to extract structure
- Sets `error` if parsing fails
- Watches content changes reactively

**fetchWorkflow()** - Loads workflow data
- Triggered when invocation detected
- Caches results in workflow store
- Manages `workflowLoading` state

## Directive Requirements & Validation

### 1. Name Validation - `hasValidName(name)`
Checks against `requirements.yml` registry:
- Dataset directives: `history_dataset_as_table`, `history_dataset_as_image`, etc.
- Job directives: `job_metrics`, `job_parameters`, `tool_stdout`, etc.
- Workflow directives: `workflow_display`, `workflow_image`, `workflow_license`
- Instance directives: `instance_access_link`, `instance_help_link`, etc.
- Metadata directives: `generate_galaxy_version`, `generate_time`

### 2. Object Validation - `hasValidObject(name, args)`
Checks that required objects are present:
```javascript
{
  "history_dataset_id": ["history_dataset_as_table", ...],
  "job_id": ["job_metrics", "job_parameters", ...],
  "workflow_id": ["workflow_display", "workflow_image", ...],
  "invocation_id": ["invocation_inputs", "invocation_outputs", ...],
  "none": ["generate_galaxy_version", "instance_*_link"]
}
```

### 3. Label Validation - `hasValidLabel(name, args, labels)`
For workflow invocations, validates labels reference valid workflow elements:
```javascript
{
  "history_dataset_id": ["input", "output"],
  "history_dataset_collection_id": ["input", "output"],
  "job_id": ["step"]
}
```

## Dynamic Rendering: Directive → Component Mapping

Large conditional chain routes directives to 20+ specialized components:

```javascript
// Dataset components
v-if="name == 'history_dataset_as_table'"
  → <HistoryDatasetAsTable :dataset-id :title :compact />

v-if="name == 'history_dataset_as_image'"
  → <HistoryDatasetAsImage :dataset-id />

// Job components
v-if="name == 'job_metrics'"
  → <JobMetrics :job-id :title :footer />

// Workflow components
v-if="name == 'workflow_display'"
  → <WorkflowDisplay :workflow-id :workflow-version />

// Metadata components
v-if="name == 'generate_galaxy_version'"
  → <TextContent :content="`Galaxy Version ${config.version_major}`" />
```

## Important Architectural Patterns

### 1. Invocation-Based Automatic Resolution
When invocation provided, component automatically resolves symbolic labels to runtime IDs:

```javascript
// Directive uses workflow labels
invocation_inputs(invocation_id="inv-42")

// Component internally resolves via parseInvocation():
- Finds inputs in invocation.inputs
- Maps label names to dataset IDs
- Injects resolved IDs into child components
```

### 2. Lazy Loading with Caching
Workflows fetched on-demand and cached:
```javascript
// watch invocation → fetchWorkflow()
// Uses fetchWorkflowForInstanceIdCached() to avoid redundant requests
```

### 3. Error Boundary Pattern
Errors handled gracefully with cascading alerts:
1. Parse error? → "directive is invalid"
2. Invocation load error? → specific error from store
3. Invalid name? → "Invalid component type"
4. Missing label? → "Invalid or missing label"
5. Missing required object? → "Missing [object_type]"
6. Still loading? → `<LoadingSpan />`
7. Otherwise → render component

### 4. Composable State Management
Uses Pinia stores:
- `useInvocationStore()` - Caches loaded invocations
- `useWorkflowStore()` - Caches workflow definitions
- `useDatasetStore()` - Caches dataset metadata
- `useConfig()` - Galaxy instance configuration

### 5. Collapse/Expand for Large Content
Optional collapsible wrapper:
```javascript
// Directive: job_metrics(..., collapse="Show Job Metrics")
// Renders: <BCollapse :visible="toggle"> with clickable title
```

## Examples

### Simple Metadata
```markdown
```galaxy
generate_galaxy_version()
```
→ "Galaxy Version 21"
```

### Dataset Display with Invocation
```markdown
```galaxy
history_dataset_as_table(
    invocation_id="inv-abc123",
    output="final_result",
    title="Analysis Results",
    compact=true
)
```

**Resolution:**
1. Fetch invocation object
2. Look up `output="final_result"` in `invocation.outputs`
3. Get dataset ID
4. Pass to `HistoryDatasetAsTable`
5. Render with compact layout
```

### Job Metrics from Workflow Step
```markdown
```galaxy
job_metrics(
    invocation_id="inv-abc123",
    step="assembly_step",
    collapse="Show Metrics"
)
```

**Resolution:**
1. Find step by label
2. Extract job_id
3. Pass to JobMetrics
4. Wrap in collapsible container
```

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Function-call syntax** | Familiar; supports named args; self-documenting |
| **Regex-based parsing** | Fast, lightweight; avoids heavyweight parsers |
| **Invocation-based resolution** | Single `invocation_id` instead of separate IDs |
| **Component-per-type strategy** | Specialized rendering logic; easier to test |
| **Store-based caching** | Prevents redundant API calls |
| **Validation layers** | Catches errors early with user-friendly messages |

## Documentation Use Cases

Enables embedding **live, interactive Galaxy data** in markdown:
1. **Training Materials** - Show actual workflow outputs
2. **Hub Articles** - Embed interactive job metrics and visualizations
3. **Sphinx Docs** - Generate multi-format outputs with embedded objects
4. **Invocation Reports** - Summarize analysis results with formatted datasets

This renders as **dynamic, data-backed documentation** instead of static screenshots.
