# PR #19054: Implement tool markdown reports

**Author:** jmchilton
**Merged:** 2025-05-06
**URL:** https://github.com/galaxyproject/galaxy/pull/19054

## Summary

Enabled tools to generate Galaxy Markdown reports as outputs, providing safer and more reproducible alternative to HTML tool outputs.

## Key Changes

**Tool Reports:** Tools can now output Galaxy Markdown instead of HTML:
- Reports reference tool outputs using directives
- Can use "extra files" for report-specific data (not formal tool outputs)
- Safer than HTML (sandboxed directives vs arbitrary HTML)
- More reproducible (can be re-rendered after export/import)

**Two Test Tools:**
1. Tool that links to/displays tool outputs
2. Tool that uses extra files for report-specific content

**Directive Subset:** Not all directives available to tools (e.g., workflow_license doesn't make sense).

**Error Handling:** Still WIP - better reporting when directives fail needed.

**Future Work:**
- Document which directives available to tools
- Embed tool reports into workflow/page reports
- Better error messages

## Architectural Implications

**HTML Replacement:** Addresses long-standing issue that HTML tool outputs can't be trusted after import. Galaxy Markdown provides safe, re-renderable alternative.

**Composability:** Tool reports can be embedded into workflow reports, enabling richer report composition.

**Extra Files Pattern:** Demonstrates using Galaxy's extra files mechanism for report-specific data that shouldn't be formal outputs.

## Documentation Focus

- Explain why Galaxy Markdown is better than HTML for tool reports
- Show examples of both patterns (output references + extra files)
- List available directives for tool context
- Demonstrate embedding tool reports in workflow reports
- Explain security/reproducibility benefits
