# PR #19086: Allow several Galaxy Markdown directives to be embedded

**Author:** jmchilton
**Merged:** 2025-09-23
**URL:** https://github.com/galaxyproject/galaxy/pull/19086

## Summary

Enabled inline/embedded Galaxy Markdown directives that render within text rather than as separate blocks.

## Key Changes

**Inline Directives:** Directives can now be embedded in paragraph text:
- Dataset names, types, links
- Tool names, parameter names
- Timestamps, versions

**Syntax:** Embedded directives use same ```galaxy syntax but render inline instead of as blocks.

**Use Cases:**
- "This analysis used dataset `dataset_name(...)` which is a `dataset_type(...)` file"
- "Generated on `generate_time(...)` using Galaxy `generate_galaxy_version(...)`"
- Legends, headers, footers with dynamic content

**Designed For:** Many directives were designed years ago anticipating this feature (links, names, types, etc. don't make sense as standalone blocks).

## Architectural Implications

**Dynamic Text:** Reports can include inline references that stay synchronized with actual data (dataset names, tool names, parameter values).

**Tool Reports:** Particularly useful for tool reports (#19054) where tool name and parameters should be rendered dynamically from XML.

**Workflow Integration:** Workflow reports can embed dynamic content in explanatory text without breaking flow.

## Documentation Focus

- Show before/after examples of embedded vs block directives
- Demonstrate inline references in flowing text
- Explain which directives make sense inline vs block
- Show practical examples: report headers with metadata, tool parameter documentation
