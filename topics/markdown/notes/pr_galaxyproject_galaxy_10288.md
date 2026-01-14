# PR #10288: Add Visualizations to Pages

**Author:** guerler
**Merged:** 2020-10-13
**URL:** https://github.com/galaxyproject/galaxy/pull/10288

## Summary

Enabled embedding interactive visualizations in Galaxy pages via markdown.

## Key Changes

**Visualization Embedding:** Pages can now include visualizations, users can interactively modify them within the page view.

**Limitations:** No parameters configurable in markdown syntax initially - only dataset specification. Configuration happens interactively.

**Note:** This PR mentions it doesn't fix individual visualization issues, just enables the embedding mechanism.

## Architectural Implications

**Interactive Reports:** Moves pages beyond static content to interactive exploration. Users can adjust visualization parameters without leaving the page.

**Separation of Concerns:** Markdown provides the structure and dataset reference; visualization component handles interactivity.

## Documentation Focus

- Show basic visualization embedding syntax
- Explain interactive vs static content model
- Note limitations of configuration via markdown
