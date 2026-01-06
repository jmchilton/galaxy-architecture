# PR #19719: Move Markdown components to subdirectory for modularity

**Author:** guerler
**Merged:** 2025-03-03
**URL:** https://github.com/galaxyproject/galaxy/pull/19719

## Summary

Refactored markdown components for better modularity and reactivity, preparing for new element types and component preview features.

## Key Changes

**Modularization:** Moved markdown components to subdirectories:
- Separates default/markdown from galaxy components
- Prepares for supporting additional element types

**Reactivity:** Introduced reactive components necessary for upcoming component preview.

**Resource Endpoints:** Components now interact directly with resource endpoints rather than going through Pages API for dataset IDs.

**Caching:** Simple caching mechanism prevents redundant requests.

## Architectural Implications

**Component Independence:** Components no longer require Pages API mediation - they fetch data directly. More reusable across contexts.

**Preview Foundation:** Reactivity and modular structure enable live preview of markdown elements as users edit.

**Performance:** Caching reduces API load when rendering complex documents with many directives.

## Documentation Focus

- Explain component architecture (modular, reactive)
- Describe resource endpoint interactions
- Note performance benefits of caching
- Mention this as foundation for editing features
