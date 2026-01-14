# PR #8543: Implement workflow invocation reports (🎉 syntax)

**Author:** jmchilton
**Merged:** 2019-08-30
**URL:** https://github.com/galaxyproject/galaxy/pull/8543

## Summary

Initial implementation of workflow invocation reports using "Galaxy Flavored Markdown" with ```galaxy code blocks.

## Key Changes

**Markdown Syntax:** Community voted on using fenced code blocks with `galaxy` language identifier:
```
```galaxy
job_metrics(step=image_cat)
```
```

**Two-stage Architecture:**
1. **Workflow Markdown** - Uses workflow-relative references (step labels, input/output labels)
2. **Galaxy Markdown** - Translated to object IDs for rendering

**Core Directives Implemented:**
- `invocation_inputs()` / `invocation_outputs()` - Auto-generate input/output sections
- `history_dataset_display()` - Embed dataset display
- `history_dataset_as_image()` - Embed images directly
- `history_dataset_peek()` / `history_dataset_info()` - Show dataset metadata
- `history_dataset_collection_display()` - Display collections
- `workflow_display()` - Embed workflow diagram
- `job_parameters()` / `job_metrics()` - Show job details
- `tool_stdout()` / `tool_stderr()` - Display tool output

## Architectural Implications

**Separation of Concerns:** Workflow markdown is workflow-portable (uses labels), while Galaxy markdown is instance-specific (uses IDs). This enables:
- Workflow definitions with embedded reports that travel with the workflow
- Same markdown components potentially reusable for pages, history annotations, library descriptions

**Client-side Rendering:** Backend generates neutral Galaxy markdown format; client Vue component handles rendering. Keeps rendering logic general and reusable.

## Documentation Focus

- Explain the two markdown "flavors" and when each is used
- Show how workflow labels get translated to object IDs
- Demonstrate basic directives with examples
- Highlight reusability across Galaxy features
