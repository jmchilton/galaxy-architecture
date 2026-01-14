# PR #8893: PDF Export of Galaxy Markdown

**Author:** jmchilton
**Merged:** 2019-12-19
**URL:** https://github.com/galaxyproject/galaxy/pull/8893

## Summary

Added PDF export capability for Galaxy Markdown documents (workflow reports and pages).

## Key Changes

**Export Pipeline:**
1. Generate internal Galaxy markdown (integer IDs)
2. Convert to basic markdown via `to_basic_markdown` (removes Galaxy extensions, replaces dynamic content with static)
3. Generate HTML using Python-Markdown library
4. Sanitize HTML with `galaxy.util.sanitize_html` (security)
5. Convert to PDF using WeasyPrint

**Configuration:**
- Custom stylesheet support for branding PDFs per Galaxy instance
- WeasyPrint pinned to older Python 2-compatible version

**Security:**
- All HTML bleached through sanitization before PDF generation

## Architectural Implications

**Pure Python Solution:** Avoids requiring pandoc or other external dependencies. WeasyPrint may not scale for all use cases, but provides fallback when pandoc unavailable.

**Static Content Conversion:** `to_basic_markdown` step is critical - converts Galaxy-specific directives into plain markdown/HTML that can be safely rendered offline. This is what makes exports truly portable.

**Future Extensibility:** Architecture allows for adding pandoc support later for Word docs or other formats while keeping WeasyPrint as fallback.

## Documentation Focus

- Explain the transformation pipeline from Galaxy markdown → PDF
- Highlight `to_basic_markdown` role in making content portable
- Discuss security considerations (sanitization)
- Show how instance branding works via custom stylesheets
