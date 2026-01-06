# File Sources Final Slide Plan - Flow C (Hybrid/Thematic)

## Configuration

**Flow:** Hybrid/Thematic (Concept-driven with evolution context)
**Duration:** 25 minutes
**Slides:** 19 total
**Diagrams:** 9 high-priority, 7 medium/low-priority (iterative)
**Code Snippets:** Yes, inline YAML and Python examples
**Audience:** Galaxy developers and advanced admins

---

## THEME 1: Plugin Architecture & Extensibility (4 slides) ✅ COMPLETE

### Slide 1: The Problem & Solution ✅ GENERATED
**Type:** Historical context + architecture introduction
**Duration:** ~2 minutes

**Content:**
- **Before 2020:** Upload dialog hardcoded for FTP and library imports
- **Problem:** No extensibility, each backend required core code changes
- **Solution (PR #9888):** Plugin architecture with `FilesSource` interface
- **Result:** New backends added without modifying Galaxy core

**Diagram:** None (text-driven slide)

**Code Snippet:** None

**Code References:**
- lib/galaxy/files/__init__.py:123-303 (ConfiguredFileSources)
- lib/galaxy/files/plugins.py:1-50 (FileSourcePluginLoader)

**PR References:** #9888

---

### Slide 2: Core Abstractions ✅ GENERATED
**Type:** Technical deep-dive (interface contracts)
**Duration:** ~2 minutes

**Content:**
- **Three interfaces:** `SingleFileSource`, `SupportsBrowsing`, `FilesSource`
- **Key operations:**
  - `realize_to()` / `write_from()` - Single file download/upload
  - `list()` - Directory browsing with pagination, search, sorting
  - `score_url_match()` - URI routing
- **BaseFilesSource:** Reference implementation with template resolution
- **ConfiguredFileSources:** Orchestrates plugin collection, manages lifecycle

**Diagram:** HIGH PRIORITY - FilesSource Interface Hierarchy ✅
- Type: PlantUML Class Diagram
- File: `images/file_sources_interface_hierarchy.plantuml.txt`
- Shows: Interface methods, inheritance, BaseFilesSource implementation

**Code Snippet:** Interface method signatures
```python
class FilesSource(Protocol):
    """Combined interface for file sources."""

    # Single file operations
    def realize_to(self, source_path: str, native_path: str) -> None:
        """Download file from source to local path."""

    def write_from(self, target_path: str, native_path: str) -> None:
        """Upload file from local path to source."""

    # Browsing operations
    def list(
        self,
        path: str = "/",
        recursive: bool = False,
        user_context: Optional[FileSourcesUserContext] = None,
        opts: Optional[FilesSourceOptions] = None,
    ) -> Tuple[List[AnyRemoteEntry], int]:
        """List directory contents with optional pagination."""

    # URI routing
    def score_url_match(self, url: str) -> int:
        """Return 0 (no match) to len(url) (exact match)."""
```

**Code References:**
- lib/galaxy/files/sources/__init__.py:83-237 (Interface definitions)
- lib/galaxy/files/sources/__init__.py:244-591 (BaseFilesSource)

**PR References:** #9888

---

### Slide 3: URI Routing & Plugin Scoring ✅ GENERATED (split into 2 slides)
**Type:** Technical deep-dive (algorithm)
**Duration:** ~1.5 minutes

**Content:**
- **Scoring algorithm:** Returns 0 (unsupported) to URI length (exact match)
- **find_best_match():** Evaluates all stock + user-defined plugins
- **URI schemes:** `gxfiles://`, `gxftp://`, `gximport://`, `s3://`, `zenodo://`, `hf://`
- **Security:** Bucket name boundary validation, prefix matching

**Diagram:** HIGH PRIORITY - URI Resolution Scoring Sequence ✅
- Type: PlantUML Sequence Diagram
- File: `images/file_sources_uri_resolution.plantuml.txt`
- Shows: URI → ConfiguredFileSources → score all plugins → best match selection

**Code Snippet:** URI scoring example
```python
# Example from S3FsFilesSource
def score_url_match(self, url: str) -> int:
    """Score S3 URL match with bucket boundary validation."""
    if url.startswith("s3://"):
        bucket_name = self._get_config_bucket()
        if bucket_name:
            # Exact bucket match: score by full prefix length
            prefix = f"s3://{bucket_name}/"
            if url.startswith(prefix):
                return len(prefix)
            # Prevent matching s3://my-bucket-prod when config is s3://my-bucket
            elif url.startswith(f"s3://{bucket_name}") and url[len(f"s3://{bucket_name}")] != "/":
                return 0  # Not a boundary, reject
        return 1  # Generic S3 match
    return 0  # Not S3
```

**Code References:**
- lib/galaxy/files/__init__.py:242-268 (get_file_source_path)
- lib/galaxy/files/__init__.py:199-207 (find_best_match)
- lib/galaxy/files/sources/s3fs.py:95-106 (score_url_match security)

**PR References:** #9888, #15497

---

### Slide 4: User Context & Access Control ✅ GENERATED (split into 2 slides)
**Type:** Technical deep-dive (security)
**Duration:** ~1.5 minutes

**Content:**
- **FileSourcesUserContext protocol:** email, roles, groups, vault access
- **ProvidesFileSourcesUserContext:** Adapts Galaxy trans object to context
- **Access filtering:** `requires_roles` and `requires_groups` config options
- **Boolean expressions:** AND/OR logic for complex access rules
- **Vault integration:** User vault + app vault for credential injection

**Diagram:** MEDIUM PRIORITY - Access Control Decision Flow ✅
- Type: PlantUML Activity Diagram
- File: `images/file_sources_access_control.plantuml.txt`
- Shows: User request → role/group evaluation (with admin bypass) → grant/deny (403)

**Code Snippet:** Access control configuration
```yaml
# Role-based access control
- type: s3fs
  id: restricted_bucket
  label: Restricted Project Data
  bucket: sensitive-data
  requires_roles: "data_access"
  requires_groups: "engineering OR research"

# Vault credential injection
- type: posix
  id: user_staging
  root: /data/staging/${user.username}
  writable: true
```

**Code References:**
- lib/galaxy/files/__init__.py:63-121 (Context protocols)
- lib/galaxy/files/sources/__init__.py:565-590 (Access control evaluation)

**PR References:** #11769

---

## THEME 2: Filesystem Abstraction Layers (4 slides) ✅ COMPLETE

### Slide 5: PyFilesystem2 Foundation (2020) ✅ GENERATED
**Type:** Historical context + technical
**Duration:** ~1.5 minutes

**Content:**
- **Original abstraction:** PyFilesystem2 (fs) library for FTP, WebDAV, cloud SDKs
- **Key feature:** Server-side pagination via `filterdir(page=(start, end))`
- **Pattern:** Context manager (filesystems opened/closed per operation)
- **Use cases:** FTP, WebDAV, SSH protocols; server-side pagination beneficial
- **Limitations:** Protocol-specific quirks, smaller ecosystem vs fsspec

**Diagram:** None (comparison in next slide)

**Code Snippet:** PyFilesystem2 pagination
```python
class PyFilesystem2FilesSource(BaseFilesSource):
    """Base class using PyFilesystem2 for file operations."""

    def _list(
        self,
        path: str = "/",
        recursive: bool = False,
        user_context: Optional[FileSourcesUserContext] = None,
        opts: Optional[FilesSourceOptions] = None,
    ) -> Tuple[List[AnyRemoteEntry], int]:
        """List with server-side pagination if supported."""
        with self._open_fs(user_context) as fs:
            limit = opts.limit if opts else None
            offset = opts.offset if opts else 0

            # Server-side pagination for large directories
            if limit is not None:
                page = (offset, offset + limit)
                entries = list(fs.filterdir(path, page=page))
            else:
                entries = list(fs.scandir(path))

            return self._serialize_entries(entries), len(entries)
```

**Code References:**
- lib/galaxy/files/sources/_pyfilesystem2.py:1-95 (PyFilesystem2FilesSource)
- lib/galaxy/files/sources/_pyfilesystem2.py:57-82 (_list pagination)

**PR References:** #9888

---

### Slide 6: fsspec Revolution (2025) ✅ GENERATED (split into 2 slides)
**Type:** Technical + evolution (major improvement)
**Duration:** ~2 minutes

**Content:**
- **fsspec:** Unified AbstractFileSystem API for 40+ backends
- **Simplicity:** Subclasses implement only `_open_fs()` method
- **Code reduction:** 500+ lines → 50 lines (10x reduction)
- **Backends:** S3, Azure, GCS, HTTP, FTP, SSH, ZIP, Git, Zarr, Hugging Face, etc.
- **Built-in features:** Pagination, metadata, path transformation, caching

**Diagram:** HIGH PRIORITY - fsspec Plugin Hierarchy ✅
- Type: PlantUML Class Diagram
- File: `images/file_sources_fsspec_hierarchy.plantuml.txt`
- Shows: FsspecFilesSource → S3FsFilesSource, HuggingFaceFilesSource with _open_fs() as sole requirement

**Code Snippet:** fsspec simplicity
```python
class S3FsFilesSource(FsspecFilesSource):
    """S3-compatible storage via fsspec."""

    plugin_type = "s3fs"

    def _open_fs(self, user_context: Optional[FileSourcesUserContext] = None):
        """Single method to implement - framework handles rest."""
        config = self._get_config(user_context)

        return fsspec.filesystem(
            "s3",
            anon=config.anon,
            key=config.access_key_id,
            secret=config.secret_access_key,
            client_kwargs={
                "endpoint_url": config.endpoint_url,
                "region_name": config.region,
            },
        )

    # That's it! FsspecFilesSource provides:
    # - realize_to(), write_from()
    # - list() with pagination
    # - score_url_match()
    # - All error handling
```

**Code References:**
- lib/galaxy/files/sources/_fsspec.py:1-120 (FsspecFilesSource base)
- lib/galaxy/files/sources/s3fs.py:67-94 (_open_fs implementation)

**PR References:** #20698

---

### Slide 7: Comparison & Migration Strategy ✅ GENERATED
**Type:** Technical comparison + guidance
**Duration:** ~1.5 minutes

**Content:**
- **When to use PyFilesystem2:** Legacy plugins, server-side pagination critical, protocol-specific features
- **When to use fsspec:** New plugins, standard operations, large ecosystem
- **Migration path:** Gradual, both abstractions coexist
- **Future direction:** fsspec preferred for new development

**Diagram:** HIGH PRIORITY - fsspec vs PyFilesystem2 Comparison
- Type: Markdown Table (rendered in slide)
- File: Inline in slide content

**Code Snippet:** None (table-driven)

**Comparison Table:**
```markdown
| Feature | PyFilesystem2 | fsspec |
|---------|---------------|--------|
| **Backends** | ~20 (FTP, WebDAV, SFTP, S3, Azure) | 40+ (all PyFS2 + Zarr, Git, HTTP, etc.) |
| **Server Pagination** | Native via filterdir(page=...) | Must implement manually |
| **Code Complexity** | Medium (~200 lines) | Low (~50 lines) |
| **Error Handling** | Protocol-specific quirks | Consistent across backends |
| **Ecosystem** | Smaller, focused | Large, active (Dask, Intake, etc.) |
| **Galaxy Usage** | FTP, WebDAV, legacy plugins | S3, Azure, GCS, Hugging Face, new plugins |
| **Performance** | Good for server-side pagination | Good for caching, parallelism |
| **Documentation** | Good | Excellent |
```

**Code References:**
- lib/galaxy/files/sources/_pyfilesystem2.py:1-95
- lib/galaxy/files/sources/_fsspec.py:1-120

**PR References:** #20698

---

### Slide 8: Adding a New File Source Plugin ✅ GENERATED
**Type:** Practical guide (extensibility)
**Duration:** ~2 minutes

**Content:**
- **Step 1:** Choose base class (FsspecFilesSource for most cases)
- **Step 2:** Implement `_open_fs()` returning fsspec filesystem
- **Step 3:** Set `plugin_type` class variable for discovery
- **Step 4:** Add Pydantic configuration models (template + resolved)
- **Step 5:** Register in `lib/galaxy/files/sources/__init__.py`
- **Step 6:** (Optional) Add user-defined template to `file_source_templates.yml`

**Diagram:** HIGH PRIORITY - Plugin Implementation Checklist ✅
- Type: PlantUML Activity Diagram
- File: `images/file_sources_add_plugin.plantuml.txt`
- Shows: Decision tree for base class selection → implementation steps → registration

**Code Snippet:** Minimal plugin example
```python
from galaxy.files.sources._fsspec import FsspecFilesSource

class MyCloudFilesSource(FsspecFilesSource):
    """Minimal file source plugin - just 15 lines!"""

    plugin_type = "mycloud"

    def _open_fs(self, user_context=None):
        config = self._get_config(user_context)
        return fsspec.filesystem(
            "mycloud",
            token=config.token,
            endpoint=config.endpoint,
        )

# That's it! Framework provides all FilesSource operations.
```

**Code References:**
- lib/galaxy/files/sources/_fsspec.py:1-120 (FsspecFilesSource base)
- lib/galaxy/files/sources/huggingface.py:1-50 (Real-world example)

**PR References:** #20698, #20805

---

## THEME 3: Plugin Implementations (3 slides) ✅ COMPLETE

### Slide 9: Stock Plugins - POSIX Foundation ✅ GENERATED
**Type:** Technical implementation
**Duration:** ~1.5 minutes

**Content:**
- **Three stock sources:** FTP (`gxftp://`), library imports (`gximport://`), user imports (`gxuserimport://`)
- **Template expansion:** `${user.ftp_dir}`, `${config.library_import_dir}`, `${user.username}`
- **Security patterns:** Symlink traversal prevention, atomic writes via .part files
- **Semantics:** Move vs copy (`delete_on_realize` flag)

**Diagram:** MEDIUM PRIORITY - POSIX Stock Sources Deployment ✅
- Type: PlantUML Deployment Diagram
- File: `images/file_sources_posix_deployment.plantuml.txt`
- Shows: Three POSIX-based sources with template configurations

**Code Snippet:** POSIX template configuration
```yaml
# FTP directory (user-specific)
- type: posix
  id: ftp_dir
  label: FTP Directory
  doc: Files uploaded via FTP
  root: ${user.ftp_dir}
  writable: false
  requires_roles: user

# Library import (admin-configured)
- type: posix
  id: library_import_dir
  label: Library Import Directory
  doc: Datasets for library imports
  root: ${config.library_import_dir}
  writable: false
  requires_roles: admin

# User-specific imports
- type: posix
  id: user_library_import_dir
  label: User Library Import
  doc: User-specific import staging
  root: ${config.user_library_import_dir}/${user.username}
  writable: true
```

**Code References:**
- lib/galaxy/files/sources/posix.py:1-150 (PosixFilesSource)
- lib/galaxy/files/sources/posix.py:95-115 (_write_from atomic writes)

**PR References:** #9888

---

### Slide 10: Cloud Storage - S3 & OAuth ✅ GENERATED
**Type:** Technical implementation + evolution
**Duration:** ~2 minutes

**Content:**
- **S3-compatible storage:** AWS S3, MinIO, DigitalOcean Spaces, Wasabi
- **Configuration:** bucket, endpoint_url, access keys, anonymous flag
- **OAuth 2.0 integration (PR #18272):** Dropbox, Google Drive (future)
- **Token management:** Access tokens (4hr expiry) + refresh tokens (stored in Vault)
- **Status tracking:** Connection health, token expiry monitoring

**Diagram:** MEDIUM PRIORITY - OAuth Flow Sequence ✅ (covered by file_sources_oauth_sequence.plantuml.txt)
- Type: PlantUML Sequence Diagram
- File: `images/file_sources_oauth_sequence.plantuml.txt`
- Shows: User → Galaxy UI → OAuth provider → callback → Vault → instance creation

**Code Snippet:** S3 configuration + OAuth template
```yaml
# S3-compatible storage (admin or user-defined)
- type: s3fs
  id: my_s3_bucket
  label: Project Data (S3)
  bucket: my-project-data
  endpoint_url: https://s3.us-west-2.amazonaws.com
  access_key_id: ${secrets.aws_access_key}
  secret_access_key: ${secrets.aws_secret_key}

# Dropbox with OAuth 2.0 (user-defined template)
- type: dropbox
  id: dropbox_{{ user.username }}
  label: "{{ user.username }}'s Dropbox"
  # OAuth tokens stored in Vault, auto-refreshed
  access_token: ${secrets.dropbox_access_token}
  refresh_token: ${secrets.dropbox_refresh_token}
```

**Code References:**
- lib/galaxy/files/sources/s3fs.py:1-150 (S3FsFilesSource)
- lib/galaxy/files/sources/s3fs.py:67-94 (_open_fs with client_kwargs)
- lib/galaxy/files/templates/models.py:80-110 (OAuth2TemplateConfiguration)

**PR References:** #20698 (S3), #18272 (OAuth)

---

### Slide 11: Research Data - Zenodo & Hugging Face ✅ GENERATED
**Type:** Technical implementation (specialized plugins)
**Duration:** ~2 minutes

**Content:**
- **Zenodo/InvenioRDM:** DOI-backed archival, draft → publish workflow
  - File management: metadata-first with commit operations
  - DOI minting for published records
  - Versioning support
- **Hugging Face Hub:** AI/ML models and datasets
  - HfFileSystem (fsspec) + HfApi (repository operations)
  - Two-tier structure: repositories → files
  - Authentication for private repos

**Diagram:** MEDIUM PRIORITY - Zenodo State Diagram (skipped - not useful)
- Type: PlantUML State Diagram
- Shows: Draft creation → file upload → metadata commit → publish → DOI assignment

**Code Snippet:** Hugging Face simplicity (fsspec-based)
```python
class HuggingFaceFilesSource(FsspecFilesSource):
    """Hugging Face Hub integration via fsspec."""

    plugin_type = "huggingface"

    def _open_fs(self, user_context: Optional[FileSourcesUserContext] = None):
        """Minimal implementation - 10 lines for full HF integration!"""
        config = self._get_config(user_context)

        return fsspec.filesystem(
            "hf",
            repo_id=config.repo_id,
            repo_type=config.repo_type,  # "model", "dataset", or "space"
            revision=config.revision,     # branch/tag/commit
            token=config.token,           # optional for private repos
            endpoint=config.endpoint,     # custom HF endpoint
        )

    # Framework provides everything else:
    # - Browse repositories and files
    # - Download models/datasets
    # - Upload trained models
    # - Git LFS metadata handling
```

**Code References:**
- lib/galaxy/files/sources/zenodo.py:1-80 (ZenodoRDMFilesSource)
- lib/galaxy/files/sources/huggingface.py:1-120 (HuggingFaceFilesSource)
- lib/galaxy/files/sources/huggingface.py:80-105 (Repository vs file path handling)

**PR References:** #18022 (Zenodo), #20805 (Hugging Face)

---

## THEME 4: User-Defined Sources (5 slides) ✅ COMPLETE

### Slide 12: Paradigm Shift - User-Driven Storage ✅ GENERATED
**Type:** Evolution + architecture shift
**Duration:** ~2 minutes

**Content:**
- **Before:** Admin configures all file sources globally in `file_sources_conf.yml`
- **Problem:** Doesn't scale to diverse user needs (different buckets, projects, credentials)
- **Solution (PR #18127):** Template catalog + user instances
- **Pattern:** Admin provides templates, users instantiate with their credentials
- **Result:** Users create multiple instances per template (different projects, buckets)

**Diagram:** None (text + code snippet driven; details in slides 13-16)

**Code Snippet:** Template catalog structure
```yaml
# file_source_templates.yml (admin-configured)
- id: s3_template
  name: AWS S3 Bucket
  description: Connect to your AWS S3 bucket
  version: 1

  variables:
    bucket:
      label: Bucket Name
      type: string
      help: S3 bucket name (e.g., my-project-data)

    region:
      label: AWS Region
      type: string
      default: us-east-1
      help: AWS region (e.g., us-west-2)

  secrets:
    access_key_id:
      label: Access Key ID
      help: AWS access key (stored in Vault)

    secret_access_key:
      label: Secret Access Key
      help: AWS secret key (stored in Vault)

  configuration:
    type: s3fs
    bucket: "{{ variables.bucket }}"
    region: "{{ variables.region }}"
    access_key_id: "{{ secrets.access_key_id }}"
    secret_access_key: "{{ secrets.secret_access_key }}"
```

**Code References:**
- lib/galaxy/files/templates/models.py:1-200 (Pydantic template models)
- lib/galaxy/managers/file_source_instances.py:1-200 (FileSourceInstancesManager)

**PR References:** #18127

---

### Slide 13: Template System - Pydantic Models ✅ GENERATED
**Type:** Technical deep-dive (type safety)
**Duration:** ~1.5 minutes

**Content:**
- **Two-tier configuration (PR #20728):**
  - `TemplateConfiguration` - Variables as Jinja2 expressions
  - `FileSourceConfiguration` - Resolved concrete values
- **Pydantic validation:** Three stages (template syntax → user input → resolved config)
- **Type union pattern:** `Union[str, TemplateExpansion]` allows both literal and template values
- **Template versioning:** Users can upgrade instances to new template versions

**Diagram:** HIGH PRIORITY - Two-Tier Configuration Models ✅
- Type: PlantUML Class Diagram
- File: `images/file_sources_pydantic_models.plantuml.txt`
- Shows: TemplateConfiguration → FileSourceConfiguration with validation stages

**Code Snippet:** Two-tier Pydantic models
```python
# Two-tier configuration models (Pydantic v2)
class S3FsTemplateConfiguration(BaseModel):
    """Template-stage config with Jinja2 expressions."""
    type: Literal["s3fs"]
    bucket: Union[str, TemplateExpansion]  # Can be "{{ variables.bucket }}"
    region: Union[str, TemplateExpansion]
    access_key_id: Union[str, TemplateExpansion]

class S3FsFilesSourceConfiguration(BaseModel):
    """Resolved config with concrete values."""
    type: Literal["s3fs"]
    bucket: str  # Must be concrete string
    region: str
    access_key_id: str
```

**Code References:**
- lib/galaxy/files/templates/models.py:1-200 (Pydantic template models)

**PR References:** #20728 (Pydantic)

---

### Slide 14: Template Expansion - Jinja2 Resolution ✅ GENERATED
**Type:** Technical deep-dive (expansion)
**Duration:** ~1.5 minutes

**Content:**
- **Jinja2 contexts:** Four available contexts for variable resolution
  - `variables` - User-provided values from form
  - `secrets` - Credentials from Vault
  - `user` - Galaxy user attributes (username, email, roles)
  - `environ` - Environment variables
- **Custom filters:** `ensure_path_component`, `asbool`
- **Syntactic sugar:** Inline includes, shorthand dict notation

**Diagram:** HIGH PRIORITY - Template Expansion Data Flow ✅
- Type: PlantUML Activity Diagram
- File: `images/file_sources_template_expansion.plantuml.txt`
- Shows: YAML → syntactic sugar → Jinja2 expansion → Pydantic validation → FileSourceConfiguration

**Code Snippet:** Jinja2 expansion with contexts
```python
def resolve_template(template_config, variables, secrets, user):
    """Three-stage validation."""
    # Stage 1: Validate template syntax
    template = TemplateConfiguration.model_validate(template_config)

    # Stage 2: Expand Jinja2 with contexts
    context = {
        "variables": variables,      # User form input
        "secrets": secrets,          # From Vault
        "user": user,                # Galaxy user object
        "environ": os.environ,       # Environment vars
    }
    expanded = jinja_env.expand(template.model_dump(), context)

    # Stage 3: Validate resolved config
    return FileSourceConfiguration.model_validate(expanded)
```

**Code References:**
- lib/galaxy/files/templates/manager.py:80-120 (expand_raw_config)

**PR References:** #18127 (templates), #20728 (Pydantic)

---

### Slide 15: OAuth 2.0 Integration Pattern ✅ GENERATED
**Type:** Technical deep-dive (security)
**Duration:** ~1.5 minutes

**Content:**
- **OAuth2TemplateConfiguration:** Base class for Dropbox, Google Drive
- **Token storage:** Vault-backed, encrypted at rest
- **Authorization flow:**
  1. User clicks "Authorize" in Galaxy UI
  2. Galaxy generates authorization URL, pre-generates UUID
  3. User redirected to provider (Dropbox, Google)
  4. User grants permissions
  5. Provider redirects to Galaxy callback with code
  6. Galaxy exchanges code for tokens
  7. Tokens stored in Vault with pre-generated UUID
  8. User completes instance creation with UUID
- **Token refresh:** Automatic via refresh tokens (no user interaction)

**Diagram:** HIGH PRIORITY - OAuth2 Authorization Flow ✅
- Type: PlantUML Sequence Diagram
- File: `images/file_sources_oauth_sequence.plantuml.txt`
- Shows: Complete OAuth flow with Vault integration

**Code Snippet:** OAuth template example
```yaml
# Dropbox OAuth template (admin-configured)
- id: dropbox_oauth
  name: Dropbox
  description: Connect to your Dropbox account
  version: 1

  # OAuth configuration (admin provides client ID/secret)
  secrets:
    client_id:
      label: Client ID
      help: Dropbox OAuth app client ID

    client_secret:
      label: Client Secret
      help: Dropbox OAuth app client secret

  configuration:
    type: dropbox
    # User tokens stored in Vault during OAuth flow
    access_token: "{{ secrets.access_token }}"
    refresh_token: "{{ secrets.refresh_token }}"
    token_expiry: "{{ secrets.token_expiry }}"

# User experience:
# 1. Click "Connect Dropbox" in User Preferences
# 2. Redirect to Dropbox authorization
# 3. Grant permissions
# 4. Return to Galaxy - instance automatically created
```

**Code References:**
- lib/galaxy/files/templates/models.py:80-110 (OAuth2TemplateConfiguration)
- lib/galaxy/webapps/galaxy/api/file_sources.py:30-50 (oauth2 endpoint)
- lib/galaxy/managers/file_source_instances.py:120-160 (Instance creation workflow)

**PR References:** #18272

---

### Slide 16: User Instance Lifecycle ✅ GENERATED
**Type:** Technical (CRUD operations)
**Duration:** ~1.5 minutes

**Content:**
- **CRUD operations:** Create, Read (list/show), Update, Delete (purge)
- **Instance identification:** UUID4 path parameters
- **Persistence:** `user_file_source` table with template snapshot + variables
- **Validation workflow:**
  1. Payload schema validation against template
  2. Template variable/secret validation
  3. Connection testing (root-level listing)
  4. Persistence to database + Vault
- **Updates:** Support template upgrades with variable mapping
- **Security:** Ownership validation, user-bound isolation

**Diagram:** HIGH PRIORITY - Instance Creation Sequence ✅
- Type: PlantUML Sequence Diagram
- File: `images/file_sources_instance_creation.plantuml.txt`
- Shows: Pre-flight validation (test endpoint) → Instance creation (persist → Vault → update)

**Code Snippet:** None (diagram-driven)

**Code References:**
- lib/galaxy/managers/file_source_instances.py:1-200 (FileSourceInstancesManager)
- lib/galaxy/webapps/galaxy/api/file_sources.py:1-180 (File sources API)

**PR References:** #18127

---

## THEME 5: URL Convergence & API (2 slides) ✅ COMPLETE

### Slide 17: URL Unification - All Protocols Through File Sources ✅ GENERATED
**Type:** Evolution + architecture convergence
**Duration:** ~2 minutes

**Content:**
- **Before PR #15497:** Separate code paths for URLs vs file sources
  - HTTP/FTP: Custom URL handler
  - S3: Separate S3 handler
  - DRS: Separate DRS handler
  - File sources: `gxfiles://` only
  - Problem: Duplicated auth logic, inconsistent access control
- **After PR #15497:** All URLs routed through file sources
  - Unified authentication and credential injection
  - `url_regex` config for site-specific handlers
  - `http_headers` config for Bearer tokens, Basic Auth
  - Consistent access control across all protocols

**Diagram:** None (text-driven slide)

**Code Snippet:** URL routing with credential injection
```yaml
# Site-specific URL routing with auth
- type: http
  id: internal_api
  label: Internal Data API
  doc: Authenticated access to internal API
  url_regex: "^https://api\\.internal\\.org/"
  http_headers:
    Authorization: "Bearer ${secrets.api_token}"

- type: http
  id: public_http
  label: Public HTTP
  doc: Generic HTTP/HTTPS downloads
  url_regex: "^https?://.*"
  # No auth headers - public access

# Result: URLs automatically route to correct handler
# https://api.internal.org/data.txt → internal_api (with auth)
# https://example.com/data.txt → public_http (no auth)
```

**Code References:**
- lib/galaxy/files/__init__.py:242-268 (get_file_source_path with URL support)
- lib/galaxy/files/sources/http.py:1-100 (HTTPFilesSource with headers)

**PR References:** #15497

---

### Slide 18: API Integration - Browsing & Management ✅ GENERATED
**Type:** Technical (API layer)
**Duration:** ~1.5 minutes

**Content:**
- **Remote Files API (browsing):**
  - `GET /api/remote_files` - Directory listing with pagination
  - `GET /api/remote_files/plugins` - Plugin enumeration
  - `POST /api/remote_files` - Entry creation (writable sources)
  - Response formats: `uri` (metadata), `flat` (file list), `jstree` (deprecated)
- **File Sources API (templates/instances):**
  - `GET /api/file_source_templates` - Template catalog
  - `POST /api/file_source_instances` - Create instance
  - `GET /api/file_source_instances` - List user instances
  - `PUT /api/file_source_instances/{uuid}` - Update instance
  - `DELETE /api/file_source_instances/{uuid}` - Delete instance
  - `POST /api/file_source_instances/test` - Validate configuration

**Diagram:** HIGH PRIORITY - Remote Files API Request Flow ✅
- Type: PlantUML Sequence Diagram
- File: `images/file_sources_api_flow.plantuml.txt`
- Shows: REST endpoint → RemoteFilesManager → ConfiguredFileSources → plugin → response serialization

**Code Snippet:** API usage examples
```python
# Browse file source directory
GET /api/remote_files?target=my_s3_bucket&path=/datasets
Response:
{
  "uri_list": [
    {"class": "Directory", "name": "2024", "uri": "gxfiles://my_s3_bucket/datasets/2024", "path": "/datasets/2024"},
    {"class": "File", "name": "data.csv", "uri": "gxfiles://my_s3_bucket/datasets/data.csv", "path": "/datasets/data.csv", "size": 1024000}
  ]
}

# List available plugins
GET /api/remote_files/plugins
Response:
[
  {"id": "ftp_dir", "type": "posix", "label": "FTP Directory", "writable": false, "browsable": true},
  {"id": "my_s3_bucket", "type": "s3fs", "label": "Project Data", "writable": true, "browsable": true}
]

# Create user instance
POST /api/file_source_instances
{
  "template_id": "s3_template",
  "template_version": 1,
  "name": "My Bucket",
  "variables": {"bucket": "my-data", "region": "us-west-2"},
  "secrets": {"access_key_id": "AKIA...", "secret_access_key": "wJa..."}
}
Response: {"uuid": "550e8400-e29b-41d4-a716-446655440000", "name": "My Bucket", "status": "ok"}
```

**Code References:**
- lib/galaxy/webapps/galaxy/api/remote_files.py:1-150 (Remote files endpoints)
- lib/galaxy/webapps/galaxy/api/file_sources.py:1-180 (File sources API)
- lib/galaxy/managers/remote_files.py:1-180 (RemoteFilesManager)
- lib/galaxy/schema/remote_files.py:1-120 (API schemas)

**PR References:** #9888 (remote files), #18127 (file sources API)

---

## THEME 6: Summary (1 slide) ✅ COMPLETE

### Slide 19: Complete Architecture & Key Takeaways ✅ GENERATED
**Type:** Synthesis + summary
**Duration:** ~1 minute

**Content:**
- **Architecture layers:**
  - Core framework: ConfiguredFileSources, RuntimeContext, Template Manager, Vault
  - Base classes: BaseFilesSource, PyFilesystem2FilesSource, FsspecFilesSource
  - Plugins: Stock (POSIX, HTTP, DRS) + User-defined (S3, Azure, Dropbox, Zenodo, HF)
- **Key design patterns:**
  - Plugin architecture for extensibility
  - URI scoring for routing
  - Template catalog for user empowerment
  - Dual abstractions (PyFilesystem2 legacy, fsspec modern)
  - Pydantic for type safety
  - OAuth for seamless cloud access
- **Evolution highlights:**
  - 2020: Foundation (plugins)
  - 2023: Convergence (URL unification)
  - 2024: User-driven (templates, OAuth)
  - 2025: Modern foundation (Pydantic, fsspec)

**Diagram:** MEDIUM PRIORITY - Complete Architecture Synthesis (skipped - too busy)
- Type: PlantUML Component Diagram
- Shows: All layers, stock vs user-defined, configuration sources, Vault integration

**Code Snippet:** None (diagram + bullet summary)

**Code References:** All previous slides

**PR References:** All (#9888, #10152, #11769, #15497, #18022, #18059, #18127, #18272, #20698, #20728, #20805)

---

## High-Priority Diagram List (9 diagrams)

1. **file_sources_interface_hierarchy.plantuml** ✅ - FilesSource interface class diagram (Slide 2)
2. **file_sources_uri_resolution.plantuml** ✅ - URI resolution scoring sequence (Slide 3)
3. **file_sources_fsspec_hierarchy.plantuml** ✅ - fsspec plugin class hierarchy (Slide 6)
4. **file_sources_fsspec_vs_pyfs2.md** - Comparison table (Slide 7) - INLINE IN SLIDE
5. **file_sources_add_plugin.plantuml** ✅ - Plugin implementation checklist (Slide 8)
6. **file_sources_pydantic_models.plantuml** ✅ - Two-tier configuration models (Slide 13)
7. **file_sources_template_expansion.plantuml** ✅ - Template expansion data flow (Slide 14)
8. **file_sources_oauth_sequence.plantuml** ✅ - OAuth2 authorization flow (Slide 15)
9. **file_sources_instance_creation.plantuml** ✅ - Instance creation sequence (Slide 16)
10. **file_sources_api_flow.plantuml** ✅ - Remote Files API request flow (Slide 18)

**Note:** Item #4 is inline markdown table, not separate file. Total: 9 PlantUML diagrams. **All complete!**

---

## Implementation Order

1. ✅ **Final plan document** (this file)
2. ✅ **Generate content.yaml** with slide definitions (19/19 slides complete)
3. ✅ **Create high-priority diagram sources** (9 PlantUML files in `images/`)
4. ✅ **Write slide content fragments** in `topics/file-sources/fragments/` (if needed)
5. ✅ **Build diagrams** with `make images`
6. ✅ **Validate** with `make validate`
7. ✅ **Generate slides** with `make build-slides`
8. **Iterate on medium/low-priority diagrams** as needed

## Current Progress

- **Theme 1:** 4/4 slides ✅ (note: slides 3 & 4 each split into 2 = 7 actual slides)
- **Theme 2:** 4/4 slides ✅ (PyFilesystem2, fsspec (split into 2), comparison, adding plugin)
- **Theme 3:** 3/3 slides ✅ (POSIX Foundation, Cloud Storage S3/OAuth, Zenodo/HF)
- **Theme 4:** 5/5 slides ✅ (Paradigm Shift, Template Catalog, Pydantic, Jinja2, OAuth, Lifecycle)
- **Theme 5:** 2/2 slides ✅ (URL Unification, API Integration)
- **Theme 6:** 1/1 slides ✅ (Summary)

**Total:** 19/19 content slides generated ✅ COMPLETE

---

## Notes

**Code Snippet Guidelines:**
- YAML configs: Show real-world template examples
- Python: Focus on key methods (interfaces, scoring, _open_fs)
- Keep snippets under 30 lines for slide readability
- Include inline comments explaining non-obvious logic

**Diagram Priorities:**
- High-priority: Create first, essential for understanding
- Medium: Create if time permits, enhance specific concepts
- Low: Create iteratively based on feedback

**Timeline References:**
- Weave evolution context throughout (not just timeline slide)
- PR numbers as references, not primary narrative
- Emphasize design patterns over implementation details

**Audience Considerations:**
- Developers: Focus on interfaces, plugin implementation, code snippets
- Admins: Focus on templates, configuration, OAuth workflows
- Both: Architecture diagrams, use cases, URL unification benefits
