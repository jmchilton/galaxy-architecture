# PR #19769: Add cell-based markdown editor for pages

**Author:** guerler
**Merged:** 2025-03-17
**URL:** https://github.com/galaxyproject/galaxy/pull/19769

## Summary

Introduced cell-based markdown editor for pages as alternative to text-based editor, with live preview support.

## Key Changes

**Cell-Based Editor:**
- Alternative to traditional text editor
- Live preview of markdown cells
- Users can switch between editors seamlessly

**Pages Only:** Initially only impacts Pages, not Reports.

**Limitations:** Visualizations not yet supported in this PR (added in follow-up).

**User Experience:** More interactive editing with immediate visual feedback.

## Architectural Implications

**Dual Editor Support:** Maintains backward compatibility with text editor while offering modern cell-based experience.

**Preview Architecture:** Requires reactive components (#19719) and direct resource endpoint access.

**Foundation for Rich Editing:** Cell structure enables more sophisticated editing features (drag-drop, inline controls).

## Documentation Focus

- Explain cell-based vs text-based editing models
- Show when to use each editor
- Demonstrate live preview capabilities
- Note visualization support coming in follow-up
