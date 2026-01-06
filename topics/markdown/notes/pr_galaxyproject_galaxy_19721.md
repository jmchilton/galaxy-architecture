# PR #19721: Preserve workflow labels in final invocation reports

**Author:** guerler
**Merged:** 2025-03-09
**URL:** https://github.com/galaxyproject/galaxy/pull/19721

## Summary

Changed invocation reports to preserve workflow labels alongside invocation IDs, enabling reports to be edited as pages while maintaining workflow context.

## Key Changes

**Previous Behavior:** Workflow labels replaced with actual IDs in final report → labels lost when editing in page editor.

**New Behavior:** Append invocation ID to workflow labels → preserve both:
- Workflow label (e.g., "input_1")
- Invocation ID

**Client-Side Resolution:** Markdown component dynamically replaces invocation ID + label pairs with actual resource IDs at render time.

**Benefits:**
- Reports remain editable without losing workflow context
- Enables interchangeability between reports and pages
- Markdown content unchanged, resolution happens at render

## Architectural Implications

**Reports ↔ Pages Interoperability:** Foundation for making reports and pages more interchangeable.

**Lazy Resolution:** IDs resolved at render time rather than baked into markdown. Keeps content portable.

**Two-Layer Addressing:** Combines workflow-relative (labels) and instance-specific (invocation IDs) addressing.

## Documentation Focus

- Explain dual addressing scheme (labels + invocation IDs)
- Show how client resolves references
- Discuss benefits for report editing
- Clarify relationship between workflow markdown, invocation markdown, and pages
