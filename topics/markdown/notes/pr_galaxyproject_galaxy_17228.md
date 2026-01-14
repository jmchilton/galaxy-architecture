# PR #17228: Overhaul Galaxy Markdown Help

**Author:** jmchilton
**Merged:** 2024-01-18
**URL:** https://github.com/galaxyproject/galaxy/pull/17228

## Summary

Fixed and improved help documentation for Galaxy Markdown directives in both pages and invocation reports.

## Key Changes

**Context-Aware Help:** Component now dispatches on document type ('mode' prop):
- Pages show page-appropriate examples and directives
- Invocation reports show workflow-appropriate examples and directives

**Unified Documentation Source:** Help text pulled from YAML document introduced in #16979:
- Same descriptions used for inline help tooltips
- Same descriptions used for help panel
- Ensures consistency and completeness

**Fixed Invocation Help:** Before this PR, invocation report help was showing incorrect/unuseful content for many directives.

## Architectural Implications

**Single Source of Truth:** YAML document defines directive metadata used across UI (help panel, tooltips, validation).

**Mode-Based Rendering:** Recognition that pages and reports have different available directives and different use patterns.

## Documentation Focus

- Explain how help system works (YAML → UI)
- Show differences between page and report directive availability
- Reference the YAML schema for directive metadata
