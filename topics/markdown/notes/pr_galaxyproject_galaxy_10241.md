# PR #10241: Create Page from Invocation Report

**Author:** guerler
**Merged:** 2020-09-20
**URL:** https://github.com/galaxyproject/galaxy/pull/10241

## Summary

Enabled creating editable Pages from immutable Invocation Reports.

## Key Changes

**Conversion Flow:**
- Invocation reports are immutable (workflow execution artifacts)
- Edit button redirects to Page creation form
- Page creation endpoint accepts Invocation ID parameter
- Form pre-populated with invocation report markdown content

**Workflow to Page:** Users can take a workflow report and continue editing it as a standalone page.

## Architectural Implications

**Mutability Boundary:** Clear separation between immutable reports (tied to specific invocation) and mutable pages (standalone documents). This PR provides the bridge.

**Content Reuse:** Workflow markdown gets translated and can be edited further in page context. Shows flexibility of markdown format across different Galaxy document types.

## Documentation Focus

- Explain difference between reports (immutable) and pages (mutable)
- Show workflow for converting reports to pages
- Discuss when to use each document type
