# PR #19952: Add validation and alerts for Markdown elements

**Author:** guerler
**Merged:** 2025-04-14
**URL:** https://github.com/galaxyproject/galaxy/pull/19952

## Summary

Added comprehensive validation and user feedback for Galaxy markdown components to prevent errors when drafting reports and pages.

## Key Changes

**Component Validation:**
- Only available directives can be embedded
- Directives assigned valid Galaxy objects or appropriate labels based on context
- Input validation prevents common mistakes

**User Feedback:**
- Alert messages guide users
- Clear error messages when validation fails
- Context-aware validation (pages vs reports)

**Testing:** Automated tests ensure validation works correctly.

## Architectural Implications

**Editor UX:** Validation happens as users compose, catching errors early rather than at render time.

**Context Awareness:** Different validation rules for pages vs reports (different available directives, different reference schemes).

**Quality Assurance:** Reduces broken reports/pages by preventing invalid directive usage upfront.

## Documentation Focus

- Show examples of validation in action
- Explain context-specific rules (pages vs reports)
- Demonstrate error messages and how to fix
- List which directives available in which contexts
