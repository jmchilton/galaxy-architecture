# Code Path: client/src/components/Markdown/directives.yml

## Role in Architecture

Metadata registry defining all Galaxy-specific markdown directives. Provides structured configuration enabling UI components and editors to discover and present directive options with contextual help.

## File Structure & Purpose

**Location:** `client/src/components/Markdown/directives.yml`

**Contents:**
- **Key:** Directive ID (e.g., `history_dataset_display`)
- **Values:** Metadata object with standardized fields

## Metadata Schema

Each directive entry:

```yaml
directive_id:
  side_panel_name: String | {page: String, report: String}
  side_panel_description: String | {page: String, report: String}  # Optional
  help: String | {page: String, report: String}  # Optional
```

**Key Fields:**

- **`side_panel_name`** (required): Display name in editor UI. Simple string or mode-indexed object.

- **`side_panel_description`** (optional): Brief descriptor. Mode-specific variants supported.

- **`help`** (optional): Comprehensive help text. Supports mode-specific variants and `%MODE%` placeholder.

## Directive Categories

30+ directives in five functional categories:

### 1. Dataset Display Directives (8 total)
- `history_dataset_display`, `history_dataset_embedded`, `history_dataset_as_table`
- `history_dataset_as_image`, `history_dataset_peek`, `history_dataset_info`
- `history_dataset_index`, `history_dataset_link`

### 2. Dataset Collection Directives
- `history_dataset_collection_display`

### 3. Dataset Metadata Directives (3 total)
- `history_dataset_type`, `history_dataset_name`, `history_dataset_peek`

### 4. Workflow Directives (5 total)
- `workflow_display`, `workflow_image`, `workflow_license`
- `invocation_time`, `invocation_inputs/outputs`

### 5. Job/Tool Execution Directives (4 total)
- `job_parameters`, `job_metrics`, `tool_stdout`, `tool_stderr`

### 6. History Directives
- `history_link`

### 7. Generation/Metadata Directives (2 total)
- `generate_time`, `generate_galaxy_version`

## Mode-Aware Design Pattern

Directives support two contextual modes:

- **`page` mode**: Static documentation pages with workflow/history references
- **`report` mode**: Dynamic workflow execution reports with runtime data

**Example mode differentiation:**
```yaml
workflow_display:
  side_panel_name:
    report: "Current Workflow"      # This workflow being reported
    page: "Display a Workflow"      # Referenced workflow
  help:
    report: "Embed this workflow's steps..."
    page: "Embed a workflow's steps..."
```

## Integration with TypeScript

**Consumer Module:** `client/src/components/Markdown/directives.ts`

Provides `directiveEntry()` function:
1. Loads raw YAML as `DirectivesMetadata` object
2. Resolves mode-specific values based on context
3. Substitutes `%MODE%` placeholder in help text
4. Returns normalized `SidePanelEntry`

**Type definitions:**
```typescript
interface DirectiveMetadata {
    side_panel_name: string | {page: string, report: string}
    side_panel_description?: string | {page: string, report: string}
    help?: string | {page: string, report: string}
}
```

## Design Decisions

### Declarative Configuration
Metadata separated from implementation. Enables UI updates without code changes.

### Mode Polymorphism
Same directive ID can present different UI labels and help depending on execution context.

### Help Text Flexibility
Supports universal help (single string) or context-specific help with `%MODE%` templating.

### Paired Templates
Works alongside `templates.yml` which maps directives to editor cell templates.

### Side Panel Architecture
Metadata designed for rendering in editor's side panel:
- Directive name/title
- Optional descriptor
- Comprehensive help on hover/focus

## Relationship to Templates System

`templates.yml` cross-references these directives:
- Each directive has corresponding template entry
- Templates define default content and configuration hints
- directives.yml provides UI metadata; templates.yml provides insertion templates

## Use Cases

1. **Markdown Editor**: Dynamic sidebar with available directives and help
2. **Document Rendering**: Mode selection determines metadata (report vs page)
3. **User Guidance**: Help text surfaces best practices
4. **Workflow Integration**: Context-aware metadata for report vs standalone page

## Documentation Highlights

**For training:**
- Declarative metadata registry
- Mode-aware presentation (page vs report)
- Help text templating with %MODE% placeholder
- Integration with TypeScript for type safety
- Paired with templates.yml for insertion
