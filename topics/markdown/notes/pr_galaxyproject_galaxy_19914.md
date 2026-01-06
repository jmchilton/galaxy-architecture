# PR #19914: Replace backend page creation controller endpoint

**Author:** guerler
**Merged:** 2025-03-27
**URL:** https://github.com/galaxyproject/galaxy/pull/19914

## Summary

Modernized page creation by replacing backend controller endpoint with frontend component, improving UX and removing page reloads.

## Key Changes

**Frontend Page Creation:**
- Removed backend controller endpoint
- Specific page creation component instead of generic form
- Form input wrapper highlights required fields
- Template markdown content for new pages (not empty)

**Improved Flow:**
- Users redirected to markdown editor after creation (not back to page list)
- No page reloads during creation
- Smoother, more modern experience

## Architectural Implications

**Client-Side Logic:** Page creation logic moved to frontend, reducing server round-trips.

**Better Onboarding:** Template content gives users starting point instead of blank page.

**Modern UX:** Single-page application flow without reloads.

## Documentation Focus

- Explain new page creation flow
- Show template content structure
- Note UX improvements (no reloads, better redirects)
- Compare to old controller-based approach
