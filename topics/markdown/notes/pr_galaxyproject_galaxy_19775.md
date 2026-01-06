# PR #19775: Add visualization framework interface to cell-based markdown editor

**Author:** guerler
**Merged:** 2025-03-24
**URL:** https://github.com/galaxyproject/galaxy/pull/19775

## Summary

Integrated new visualization framework into cell-based markdown editor, enabling embedding of standalone visualizations in pages and workflow reports.

## Key Changes

**Visualization Support:** Only standalone visualizations published as npm packages can be used:
- Ensures stability across Galaxy updates
- Prevents build system issues
- Packaged visualizations don't break

**Framework:** Uses new [galaxy-charts framework](https://galaxyproject.github.io/galaxy-charts).

**Workflow Reports:** Enabled cell-based editor for workflow reports (lays groundwork for workflow-specific visualizations).

**Block Types:** Integrated Vega and Vitessce as supported cell/block types.

**Preview Behavior:**
- Pages: visualizations have preview in editor
- Workflow reports: no preview (yet)

## Architectural Implications

**Stability Through Packaging:** Requiring npm-packaged visualizations prevents the common issue of visualizations breaking with Galaxy updates.

**Framework Standardization:** Adoption of galaxy-charts framework provides consistent visualization API.

**Reports Get Interactive:** Workflow reports can now include rich, interactive visualizations, not just static content.

## Documentation Focus

- Explain visualization packaging requirements
- Reference galaxy-charts framework documentation
- Show examples of Vega and Vitessce in reports
- Discuss stability benefits of packaged approach
- Note differences between page and report visualization preview
