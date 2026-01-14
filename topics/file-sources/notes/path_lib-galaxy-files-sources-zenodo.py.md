# lib/galaxy/files/sources/zenodo.py

## Zenodo/Invenio Integration Plugin Summary

**Zenodo RDM Files Source** is a Galaxy File Sources plugin that enables integration with Zenodo, CERN's open science repository platform. The plugin provides DOI-backed archival and dataset publishing capabilities for Galaxy workflows and analyses.

### Purpose & Scope

Zenodo is built on InvenioRDM, an open-source research data management framework. This plugin implements the FilesSource interface to abstract Zenodo as a browsable file source within Galaxy, allowing users to publish and archive research datasets with persistent DOI identifiers while maintaining version control and access management.

### FilesSource Interface Implementation

The `ZenodoRDMFilesSource` class extends `InvenioRDMFilesSource`, inheriting full RDM (Research Data Management) protocol support. It exposes:

- **List containers/records**: Browse published and draft Zenodo deposits with pagination and full-text search
- **List files in containers**: View files within a specific deposit (record)
- **Download files**: Retrieve published files (authenticated access for restricted records)
- **Create new containers**: Initiate draft deposits with metadata
- **Upload files**: Add content to draft records before publication
- **URI scheme handling**: Uses `zenodo://` URI scheme to reference deposits

### InvenioRDM Compatibility

The implementation leverages InvenioRDM's standardized REST API (`/api/records`). Key integration points:

- **Record metadata**: Supports standard InvenioRDM fields (title, creators, publication date, resource type)
- **Draft lifecycle**: Creates draft records in user's workspace, supporting iterative file uploads
- **File management**: Metadata-first file approach with content upload and commit workflow
- **Access control**: Distinguishes published (public) vs. draft (writeable) records via API endpoints

### Key Features

1. **Versioning**: Deposits can be versioned; supports both draft and published states
2. **DOI Minting**: Zenodo automatically assigns DOIs to published records
3. **Deposition Workflow**: Create draft → upload files → publish flow with explicit commit operations
4. **Creator Attribution**: Captures Galaxy user metadata (public name) as deposit creator
5. **Pagination & Search**: Supports browsable discovery with limit/offset and full-text search
6. **Authentication**: Token-based access (Bearer tokens) for private/draft record access

**Plugin Type ID**: `zenodo` | **RDM Scheme**: `zenodo` | **Repository URL**: Configurable per instance
