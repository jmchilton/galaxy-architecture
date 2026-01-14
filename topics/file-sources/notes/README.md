# File Sources Research Notes

Research notes for file-sources topic, generated from related pull requests.

## Overview

This directory contains detailed summaries and diffs for all major pull requests that developed Galaxy's File Sources architecture. Each PR is documented with:
- **Summary markdown** (`pr_*.md`): Analysis tailored for documentation generation
- **Diff file** (`pr_*.diff`): Complete code changes for reference

## Pull Requests by Theme

### Foundation (2020)

**PR #9888 - Pluggable URI handling (File Sources inception)**
- Initial File Sources architecture
- FilesSource plugin interface, ConfiguredFileSources manager
- URI schemes (gxfiles://, gxftp://, etc.)
- Posix, WebDAV, Dropbox plugins
- Templating with user preferences

**PR #10152 - Writable File Sources**
- Write operation support
- Export capabilities
- Data export tools foundation

### Security & Access Control (2021)

**PR #11769 - Role and Group Permissions**
- `requires_roles` and `requires_groups` configuration
- Boolean logic for access rules
- Security enforcement layer

### Unification (2023)

**PR #15497 - Converge File Sources and URI handling**
- URLs routed through file sources
- `score_url_match()` for URL routing
- Credential injection for protected URLs
- DRS integration
- Pattern-based routing with `url_regex`

### Cloud Services & Pagination (2024)

**PR #18022 - Zenodo Integration**
- Zenodo/Invenio file source plugin
- DOI-backed data archival
- Custom URI schemes (zenodo://, invenio://)
- Vault integration for tokens

**PR #18059 - Server-side Pagination**
- `supports_pagination`, `supports_search`, `supports_sorting` properties
- Total match counts in API
- Performance for large repositories
- TempFileSource testing plugin

### User-Defined Framework (2024)

**PR #18127 - User-Defined File Sources (Template Framework)**
- Template catalog system
- Jinja templating for configurations
- UserFileSource and UserObjectStore database models
- Production-ready templates (AWS, Azure, GCS, FTP, etc.)
- Template versioning and upgrades
- Extensive admin/user documentation

**PR #18272 - OAuth 2.0 Support**
- OAuth 2.0 authentication flow
- Dropbox integration with OAuth
- Token management in Vault
- Status framework for OAuth services
- Extensible to Google Drive, OneDrive, etc.

### Modern Architecture (2025)

**PR #20728 - Pydantic Modelling**
- Two-tier configuration (template vs resolved)
- Pydantic validation at all levels
- FilesSourceRuntimeContext
- Configuration linter tool

**PR #20698 - fsspec Base Implementation**
- FsspecFilesSource adapter base class
- 40+ backends available via fsspec
- BaseFileSourceTestSuite
- MemoryFilesSource for testing
- 10x code reduction for new plugins

**PR #20805 - Hugging Face Integration**
- Access AI/ML models and datasets
- Built on fsspec infrastructure
- User-defined template
- Repository versioning support

## Key Architectural Evolution

1. **2020**: Plugin framework with basic plugins (posix, webdav, dropbox)
2. **2021**: Security controls (roles/groups)
3. **2023**: URL convergence, DRS support
4. **2024**: User-defined templates, OAuth, cloud integrations
5. **2025**: Pydantic typing, fsspec backends, modern ML platform integration

## Documentation Narrative Arc

### Introduction
- What are File Sources vs Object Stores
- Use cases (import, export, storage)
- Global vs user-defined

### Core Architecture (PR #9888)
- FilesSource plugin interface
- ConfiguredFileSources manager
- URI schemes
- Plugin examples

### Security Model (PR #11769)
- Role and group restrictions
- Access control patterns

### URL Handling (PR #15497)
- URL routing through file sources
- Credential injection
- DRS integration

### User-Defined Framework (PR #18127)
- Template catalog concept
- Jinja templating
- Database models
- Admin configuration
- User workflow

### Authentication (PR #18272)
- OAuth 2.0 integration
- Token management
- Service-specific flows

### Modern Development (PR #20728, #20698)
- Pydantic models
- fsspec backends
- Plugin development guide

### Integrations
- Zenodo (PR #18022)
- Hugging Face (PR #20805)
- Cloud providers (AWS, Azure, GCS)

## File Naming Convention

- `pr_<github_org>_<github_repo>_<number>.md` - Summary document
- `pr_<github_org>_<github_repo>_<number>.diff` - Complete code diff

## Usage

These notes are designed to:
1. Understand File Sources architecture evolution
2. Generate topic content.yaml with accurate technical details
3. Create training slides with proper context
4. Write Sphinx documentation with correct examples
