# PR #16672: Add workflow image and license to Galaxy markdown

**Author:** jmchilton
**Merged:** 2023-11-03
**URL:** https://github.com/galaxyproject/galaxy/pull/16672

## Summary

Added directives for embedding workflow diagram previews and license information in markdown.

## Key Changes

**Workflow Image Directive:** Three sizes supported:
- `sm` - 300px width, auto height
- `md` - 550px width, auto height
- `lg` (default) - 100% width, auto height

**SVG Rendering:** Workflow diagrams embedded as SVG for quality and scalability.

**PDF Support:** WIP for embedding SVGs in PDF exports - WeasyPrint compatibility being explored.

**License Directive:** Display workflow license information.

## Architectural Implications

**Visual Context:** Embedding workflow diagrams helps readers understand the workflow structure without leaving the report.

**Responsive Sizing:** Multiple size options allow reports to balance detail vs layout.

**Format Challenges:** SVG embedding works great for HTML, but PDF conversion presents technical challenges (discussed in PR).

## Documentation Focus

- Show examples of each size option with use cases
- Explain when to use workflow images vs full workflow displays
- Note current PDF limitations with SVG content
