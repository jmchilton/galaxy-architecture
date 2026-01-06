# File Sources Slide Plan - Code Architecture Perspective

## Overview

This slide deck presents Galaxy File Sources architecture through a bottom-up code perspective, tracing from base abstractions through plugin implementations to API integration. The architecture demonstrates a sophisticated plugin system built on composition, template-driven configuration, and standardized filesystem abstractions (fsspec/PyFilesystem2).

**Target Audience:** Developers familiar with Galaxy seeking deep architectural understanding
**Duration:** 20 minutes
**Approach:** Code-driven analysis with 16 focused slides across 5 themes

---

## THEME 1: Core Abstractions & Plugin Interface

### Slide 1: File Sources Plugin Architecture Overview

- Three-tier architecture: Base abstractions → Adapter layers → Concrete plugins
- Plugin discovery via `plugin_type` class variable introspection
- URI-based routing with scoring algorithm for multi-plugin resolution
- Composition over inheritance: `ConfiguredFileSources` orchestrates plugin collection

**Proposed Diagram:** Component diagram showing ConfiguredFileSources → FileSourcePluginLoader → BaseFilesSource hierarchy with example plugins

**Code References:**
- lib/galaxy/files/__init__.py:123-303 (ConfiguredFileSources)
- lib/galaxy/files/plugins.py:1-50 (FileSourcePluginLoader)

---

### Slide 2: FilesSource Interface - Core Contracts

- `SingleFileSource`: realize_to(), write_from(), score_url_match()
- `SupportsBrowsing`: list() with pagination, recursion, search, sorting
- `FilesSource`: Combined interface (both single file ops + browsing)
- `BaseFilesSource`: Reference implementation with template resolution

**Proposed Diagram:** UML interface diagram showing three interfaces and their method signatures

**Code References:**
- lib/galaxy/files/sources/__init__.py:83-237 (Interface definitions)
- lib/galaxy/files/sources/__init__.py:244-591 (BaseFilesSource)

---

### Slide 3: URI Resolution & Plugin Scoring

- `score_url_match()` returns 0 (unsupported) to URI length (exact match)
- `find_best_match()` evaluates all plugins + user-defined sources
- Prefix-based matching with security validation (bucket name boundaries)
- URI schemes: `gxfiles://`, `gxftp://`, `gximport://`, `s3://`, `zenodo://`

**Proposed Diagram:** Sequence diagram showing URI resolution flow from ConfiguredFileSources through scoring to best match selection

**Code References:**
- lib/galaxy/files/__init__.py:242-268 (get_file_source_path)
- lib/galaxy/files/__init__.py:199-207 (find_best_match)
- lib/galaxy/files/sources/s3fs.py:95-106 (score_url_match security)

---

### Slide 4: User Context & Access Control

- `FileSourcesUserContext` protocol: email, roles, groups, vaults
- `ProvidesFileSourcesUserContext` adapts Galaxy trans object
- Role/group filtering via boolean expressions
- User vault + app vault for credential injection

**Proposed Diagram:** Class diagram showing context protocols and their relationships to ConfiguredFileSources

**Code References:**
- lib/galaxy/files/__init__.py:63-121 (Context protocols)
- lib/galaxy/files/sources/__init__.py:565-590 (Access control evaluation)

---

## THEME 2: Filesystem Abstraction Layers

### Slide 5: FsspecFilesSource - Unified Storage Interface

- fsspec provides AbstractFileSystem API for 40+ backends
- Subclasses implement only `_open_fs()` method
- Built-in operations: _list(), _realize_to(), _write_from()
- Pagination, metadata extraction, path transformation hooks

**Proposed Diagram:** Class hierarchy showing FsspecFilesSource → S3FsFilesSource, HuggingFaceFilesSource with _open_fs() as sole requirement

**Code References:**
- lib/galaxy/files/sources/_fsspec.py:1-120 (FsspecFilesSource base)
- lib/galaxy/files/sources/s3fs.py:67-94 (_open_fs implementation)

---

### Slide 6: PyFilesystem2FilesSource - Alternative Abstraction

- PyFilesystem2 (fs) library for FTP, WebDAV, cloud SDKs
- Server-side pagination via filterdir(page=(start,end))
- Context manager pattern: filesystems opened/closed per operation
- Error handling for protocol-specific quirks (WebDAV KeyError workaround)

**Proposed Diagram:** Comparison table: fsspec vs PyFilesystem2 features (pagination, search, error handling, ecosystem)

**Code References:**
- lib/galaxy/files/sources/_pyfilesystem2.py:1-95 (PyFilesystem2FilesSource)
- lib/galaxy/files/sources/_pyfilesystem2.py:57-82 (_list pagination logic)

---

### Slide 7: POSIX Plugin - Foundation for Stock Sources

- Three stock sources: FTP (`gxftp://`), library imports, user imports
- Template-expandable root paths: `${user.ftp_dir}`, `${config.library_import_dir}`
- Security: symlink traversal prevention, atomic writes via .part files
- Move vs copy semantics: `delete_on_realize` flag

**Proposed Diagram:** Deployment diagram showing three POSIX-based sources with their configuration templates

**Code References:**
- lib/galaxy/files/sources/posix.py:1-150 (PosixFilesSource implementation)
- lib/galaxy/files/sources/posix.py:95-115 (_write_from atomic writes)

---

## THEME 3: Concrete Plugin Implementations

### Slide 8: S3-Compatible Storage Plugin

- S3FsFilesSource extends FsspecFilesSource
- Configuration: bucket, endpoint_url, key/secret, anonymous flag
- Custom endpoint support: MinIO, DigitalOcean Spaces, Wasabi
- Bucket path normalization: handles both config bucket + s3:// URIs

**Proposed Diagram:** Sequence diagram showing S3 file listing flow: _open_fs() → S3FileSystem → fsspec operations → RemoteFile objects

**Code References:**
- lib/galaxy/files/sources/s3fs.py:1-150 (S3FsFilesSource)
- lib/galaxy/files/sources/s3fs.py:67-94 (_open_fs with client_kwargs)

---

### Slide 9: Research Data Management - Zenodo Integration

- InvenioRDM protocol implementation (draft → publish workflow)
- DOI minting for published records
- File management: metadata-first with commit operations
- Pagination, search, draft vs published record distinction

**Proposed Diagram:** State diagram showing Zenodo record lifecycle: draft creation → file upload → metadata commit → publish → DOI assignment

**Code References:**
- lib/galaxy/files/sources/zenodo.py:1-80 (ZenodoRDMFilesSource)
- lib/galaxy/files/sources/zenodo.py:35-60 (InvenioRDM API integration)

---

### Slide 10: Hugging Face Hub - AI/ML Model Access

- HfFileSystem (fsspec) + HfApi for repository operations
- Two-tier structure: repositories → files
- Authentication: optional token for private repos
- Repository discovery: search and sort by downloads, likes, trending

**Proposed Diagram:** Component interaction showing HfApi (root listing) + HfFileSystem (file operations) + Git LFS (metadata)

**Code References:**
- lib/galaxy/files/sources/huggingface.py:1-120 (HuggingFaceFilesSource)
- lib/galaxy/files/sources/huggingface.py:80-105 (Repository vs file path handling)

---

## THEME 4: Template System & User-Defined Sources

### Slide 11: Template Catalog Architecture

- `FileSourceTemplateCatalog`: Admin-defined reusable blueprints
- Two model types: TemplateConfiguration (variables) → FileSourceConfiguration (concrete)
- Variables: typed parameters (string, integer, path_component, boolean)
- Secrets: vault-stored credentials, not exposed in API responses

**Proposed Diagram:** Class diagram showing template catalog → 14 file source type models → template/resolved config pairs

**Code References:**
- lib/galaxy/files/templates/models.py:1-200 (Pydantic models)
- lib/galaxy/files/templates/models.py:150-180 (template_to_configuration)

---

### Slide 12: Template Expansion & Variable Substitution

- Jinja2 templating with four contexts: variables, secrets, user, environment
- Custom filters: `ensure_path_component`, `asbool`
- Syntactic sugar: inline includes, shorthand dict notation
- Template metadata stripping after expansion

**Proposed Diagram:** Data flow showing template YAML → syntactic sugar → Jinja2 expansion → validation → FileSourceConfiguration

**Code References:**
- lib/galaxy/files/templates/manager.py:1-150 (FileSourceTemplatesManager)
- lib/galaxy/files/templates/manager.py:80-120 (expand_raw_config)

---

### Slide 13: User Instance Lifecycle

- CRUD via FileSourceInstancesManager (create, list, show, purge)
- UUID-based identification, stored in user_file_source table
- Template validation → variable defaults → expansion → connection test
- OAuth2 workflow: pre-generate UUID for token storage before instance creation

**Proposed Diagram:** Sequence diagram showing user instance creation flow with validation checkpoints

**Code References:**
- lib/galaxy/managers/file_source_instances.py:1-200 (FileSourceInstancesManager)
- lib/galaxy/managers/file_source_instances.py:120-160 (Instance creation workflow)

---

### Slide 14: OAuth2 Integration Pattern

- OAuth2TemplateConfiguration base class for Dropbox, Google Drive
- Client credentials in template, refresh tokens in vault
- Authorization URL generation → callback handler → token storage
- Pre-generated UUID links authorization session to instance

**Proposed Diagram:** Sequence diagram showing OAuth2 flow: template → auth URL → user consent → callback → token vault → instance creation

**Code References:**
- lib/galaxy/files/templates/models.py:80-110 (OAuth2TemplateConfiguration)
- lib/galaxy/webapps/galaxy/api/file_sources.py:30-50 (oauth2 endpoint)

---

## THEME 5: API Integration & Data Flow

### Slide 15: Remote Files API - Browsing & Listing

- Three endpoints: directory listing, plugin enumeration, entry creation
- Response formats: uri (metadata-rich), flat (file list), jstree (deprecated tree)
- Pagination: limit/offset with total_matches header
- Search and sort delegation to plugin capabilities

**Proposed Diagram:** API request flow showing endpoint → RemoteFilesManager → ConfiguredFileSources → plugin selection → response serialization

**Code References:**
- lib/galaxy/webapps/galaxy/api/remote_files.py:1-150 (Remote files endpoints)
- lib/galaxy/managers/remote_files.py:1-180 (RemoteFilesManager)

---

### Slide 16: File Sources API - Template Management

- Template browsing: GET /api/file_source_templates
- Instance CRUD: POST/GET/PUT/DELETE /api/file_source_instances/{uuid}
- Testing endpoints: validate configuration before persistence
- OAuth2 endpoint: template-based authorization URL generation

**Proposed Diagram:** REST API hierarchy showing template endpoints + instance endpoints with HTTP methods and status codes

**Code References:**
- lib/galaxy/webapps/galaxy/api/file_sources.py:1-180 (File sources API)
- lib/galaxy/schema/remote_files.py:1-120 (API schemas)

---

## Diagram TODO List

1. **File Sources Component Architecture** - PlantUML Component Diagram - Shows ConfiguredFileSources, FileSourcePluginLoader, BaseFilesSource, and plugin instances
2. **FilesSource Interface Hierarchy** - PlantUML Class Diagram - Shows SingleFileSource, SupportsBrowsing, FilesSource interfaces with method signatures
3. **URI Resolution Scoring Flow** - PlantUML Sequence Diagram - Shows URI → ConfiguredFileSources → score evaluation → best match selection
4. **User Context Protocol Relationships** - PlantUML Class Diagram - Shows context protocols and their integration with file sources
5. **fsspec Plugin Hierarchy** - PlantUML Class Diagram - Shows FsspecFilesSource → concrete implementations (S3, HuggingFace) with _open_fs()
6. **fsspec vs PyFilesystem2 Comparison** - Markdown Table - Feature comparison (pagination, search, errors, ecosystem)
7. **POSIX Stock Sources Deployment** - PlantUML Deployment Diagram - Shows FTP, library import, user import configurations
8. **S3 File Listing Sequence** - PlantUML Sequence Diagram - Shows S3 operations from _open_fs through fsspec to response
9. **Zenodo Record Lifecycle** - PlantUML State Diagram - Shows draft → upload → commit → publish → DOI flow
10. **HuggingFace Component Integration** - PlantUML Component Diagram - Shows HfApi + HfFileSystem + Git LFS interaction
11. **Template Catalog Model Structure** - PlantUML Class Diagram - Shows template catalog → 14 source types → template/resolved pairs
12. **Template Expansion Data Flow** - PlantUML Activity Diagram - Shows YAML → syntactic sugar → Jinja2 → validation flow
13. **User Instance Creation Sequence** - PlantUML Sequence Diagram - Shows validation checkpoints during instance creation
14. **OAuth2 Authorization Flow** - PlantUML Sequence Diagram - Shows template → auth → callback → vault → instance
15. **Remote Files API Request Flow** - PlantUML Sequence Diagram - Shows endpoint → manager → plugin → serialization
16. **File Sources REST API Hierarchy** - PlantUML Component Diagram - Shows template + instance endpoints with HTTP methods

---

## Implementation Notes

**Diagram Priority:**
- High: Diagrams 1, 2, 5, 11, 15 (core architecture understanding)
- Medium: Diagrams 3, 7, 12, 13, 16 (workflow and API patterns)
- Low: Diagrams 4, 6, 8, 9, 10, 14 (supplementary detail)

**Code Snippet Candidates:**
- Slide 2: BaseFilesSource interface methods
- Slide 3: score_url_match() implementation
- Slide 5: _open_fs() example from S3FsFilesSource
- Slide 7: Atomic write pattern with .part files
- Slide 12: Jinja2 template expansion snippet

**Recommended Diagram Format:**
- Use PlantUML for all UML diagrams (class, sequence, component, state, deployment)
- Use Markdown tables for feature comparisons
- Inline simple examples directly in slides
- Complex diagrams rendered as separate image files

