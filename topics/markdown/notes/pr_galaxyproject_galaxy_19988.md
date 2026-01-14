# PR #19988: Add KaTeX equation rendering plugin to Markdown Editor

**Author:** guerler
**Merged:** 2025-05-13
**URL:** https://github.com/galaxyproject/galaxy/pull/19988

## Summary

Added KaTeX support for rendering mathematical equations (inline and block) in markdown editor.

## Key Changes

**Math Rendering:** Support for LaTeX-style equations:
- Inline equations: `$equation$`
- Block equations: `$$equation$$`

**Plugin Architecture:** Uses markdown-it plugin interface for KaTeX integration.

**Templates:** New equation templates added to editor.

**Future Direction:** Demonstrates approach for supporting inline rendering plugins across more Galaxy markdown components.

## Architectural Implications

**Plugin Extensibility:** markdown-it plugin interface enables adding more rendering capabilities (diagrams, charts, etc.).

**Scientific Content:** Essential for scientific workflows that need to present mathematical concepts.

**Composability:** Math rendering works alongside Galaxy directives, enabling rich scientific reports.

## Documentation Focus

- Show inline vs block equation syntax
- Provide example equations for common use cases
- Explain markdown-it plugin architecture
- Demonstrate combining equations with Galaxy directives in scientific reports
