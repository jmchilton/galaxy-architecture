# File Sources Slide Plan - Evolution Perspective

## Overview

This slide deck traces Galaxy File Sources evolution from basic URI handling to a sophisticated user-defined storage framework. The narrative follows 11 major PRs (2020-2025) showing architectural decisions, problems solved, and design patterns that emerged.

**Target Audience:** Galaxy admins and developers
**Duration:** 20 minutes
**Structure:** 6 thematic sections, 16 slides total

---

## THEME 1: Foundation - The Plugin Architecture (2020)

### Slide 1: The Problem - Before File Sources
- Upload dialog hardcoded for FTP and library imports only
- No extensibility for new storage backends
- Each storage type required modifying core upload code
- Users wanted: Dropbox, WebDAV, cloud storage, etc.

**Proposed Diagram:** Before/After comparison showing hardcoded upload paths vs pluggable architecture
```plantuml
@startuml
!theme plain

package "Before (2020)" {
  [Upload Dialog] --> [FTP Handler]
  [Upload Dialog] --> [Library Import]
  note right: Each backend\nrequires core\ncode changes
}

package "After (PR #9888)" {
  [Upload Dialog] --> [ConfiguredFileSources]
  [ConfiguredFileSources] --> [Plugin: FTP]
  [ConfiguredFileSources] --> [Plugin: WebDAV]
  [ConfiguredFileSources] --> [Plugin: Dropbox]
  [ConfiguredFileSources] --> [Plugin: ...]
  note right: New backends\nadded via\nplugins
}
@enduml
```

**PR References:** #9888

---

### Slide 2: Core Architecture - FilesSource Plugin Interface
- `FilesSource` interface: abstract contract for all plugins
- Two core operations: `index()` (browse) and `realize()` (download)
- `ConfiguredFileSources` manager: routes URIs to appropriate plugins
- Custom URI scheme: `gxfiles://<plugin-id>/path/to/file`

**Proposed Diagram:** Plugin interface and core operations
```plantuml
@startuml
!theme plain

interface FilesSource {
  +index(path, recursive): List[Entry]
  +realize(path, dest): File
  +score_url_match(url): int
}

class BaseFilesSource implements FilesSource
class PyFilesystem2FilesSource extends BaseFilesSource

class PosixPlugin extends BaseFilesSource
class WebDAVPlugin extends PyFilesystem2FilesSource
class DropboxPlugin extends PyFilesystem2FilesSource

class ConfiguredFileSources {
  +plugins: List[FilesSource]
  +find_plugin(uri): FilesSource
}

ConfiguredFileSources o-- FilesSource

note right of FilesSource
  Core operations:
  - index: browse directories
  - realize: download files
  - score_url_match: URI routing
end note
@enduml
```

**PR References:** #9888

---

### Slide 3: Base Classes and Initial Plugins
- `BaseFilesSource`: general-purpose helper (e.g., POSIX)
- `PyFilesystem2FilesSource`: assumes PyFilesystem2 backend
- Initial plugins: posix (FTP, library imports), webdav (OwnCloud), dropbox
- Configuration templating: access user preferences, env vars

**Proposed Diagram:** Base class hierarchy
```plantuml
@startuml
!theme plain

abstract class FilesSource {
  {abstract} +index()
  {abstract} +realize()
}

abstract class BaseFilesSource {
  +template_engine
  +user_context
  +parse_config()
}

abstract class PyFilesystem2FilesSource {
  +fs: PyFilesystem2
  +index() uses fs.walk()
  +realize() uses fs.download()
}

FilesSource <|-- BaseFilesSource
BaseFilesSource <|-- PyFilesystem2FilesSource

note right of BaseFilesSource
  Provides:
  - Config templating
  - User context injection
  - URI scheme handling
end note

note right of PyFilesystem2FilesSource
  Simplifies plugins:
  - Delegate to PyFilesystem2
  - Auto-implement index/realize
  - ~90% less code
end note
@enduml
```

**PR References:** #9888

---

## THEME 2: Enhanced Capabilities (2020-2021)

### Slide 4: Write Support - Export Your Data
- PR #10152: Added write operations to plugin interface
- Enables export to remote destinations (not just import)
- Use cases: collection archives, history exports, tool outputs
- Complements read-only indexing/realize operations

**Proposed Diagram:** Read vs Write operations flow
```plantuml
@startuml
!theme plain

actor User

package "Read Operations (Import)" {
  User --> [Upload Dialog]: browse
  [Upload Dialog] --> [FilesSource.index()]: list files
  [FilesSource.index()] --> User: show tree
  User --> [Upload Dialog]: select
  [Upload Dialog] --> [FilesSource.realize()]: download
  [FilesSource.realize()] --> [Galaxy Dataset]
}

package "Write Operations (Export)" {
  [Galaxy Dataset] --> [Export Tool]
  [Export Tool] --> [FilesSource.write_from()]: upload
  [FilesSource.write_from()] --> [Remote Storage]
}

note bottom of "Read Operations (Import)"
  Original functionality (PR #9888)
end note

note bottom of "Write Operations (Export)"
  Added in PR #10152 (Sept 2020)
end note
@enduml
```

**PR References:** #10152

---

### Slide 5: Security - Role and Group Permissions
- PR #11769: Added `requires_roles` and `requires_groups` config options
- Boolean expression parser for complex access rules (AND/OR logic)
- Access checks before file operations
- File sources without restrictions remain public

**Proposed Diagram:** Access control decision tree
```plantuml
@startuml
!theme plain

start
:User requests file source;

if (File source has\nrequires_roles or\nrequires_groups?) then (yes)
  :Evaluate boolean expression;
  if (User has required\nroles/groups?) then (yes)
    :Grant access;
    stop
  else (no)
    :Deny access\n(source hidden);
    stop
  endif
else (no)
  :Grant access\n(public source);
  stop
endif

note right
  Example config:
  requires_roles: "data_access"
  requires_groups: "engineering OR research"
end note
@enduml
```

**PR References:** #11769

---

## THEME 3: Convergence - URLs as File Sources (2023)

### Slide 6: The Big Unification - URLs Through File Sources
- PR #15497: All URL protocols routed through file sources
- Protocols: http(s), ftp, s3, drs, base64
- Previously: separate code paths for URLs vs file sources
- Now: unified authentication, credential injection, access control

**Proposed Diagram:** Before/After URL handling architecture
```plantuml
@startuml
!theme plain

package "Before PR #15497" {
  [Upload Tool] --> [URL Handler]: http, ftp
  [Upload Tool] --> [S3 Handler]: s3://
  [Upload Tool] --> [DRS Handler]: drs://
  [Upload Tool] --> [File Sources]: gxfiles://
  note bottom: Separate code paths,\nduplicated auth logic
}

package "After PR #15497" {
  [Upload Tool] --> [ConfiguredFileSources]
  [ConfiguredFileSources] --> [HTTP Plugin]: http://
  [ConfiguredFileSources] --> [S3FS Plugin]: s3://
  [ConfiguredFileSources] --> [DRS Plugin]: drs://
  [ConfiguredFileSources] --> [Posix Plugin]: gxfiles://
  note bottom: Single code path,\nunified auth
}
@enduml
```

**PR References:** #15497

---

### Slide 7: URL Pattern Matching and Credential Injection
- `url_regex` config: route specific URLs to specific plugins
- `http_headers` config: inject authentication (Basic Auth, Bearer tokens)
- Site-specific handlers with different credentials
- DRS access method routing (HTTP, S3)

**Proposed Diagram:** URL routing with credential injection
```plantuml
@startuml
!theme plain

participant "Upload Tool" as Upload
participant "ConfiguredFileSources" as Manager
participant "HTTP Plugin A" as PluginA
participant "HTTP Plugin B" as PluginB
participant "HTTP Plugin (default)" as Default

Upload -> Manager: upload("https://api.example.org/data.txt")

Manager -> PluginA: score_url_match(url)
note right: url_regex: "^https://api.example.org/"\nScore: 100

Manager -> PluginB: score_url_match(url)
note right: url_regex: "^https://other.org/"\nScore: 0

Manager -> Default: score_url_match(url)
note right: url_regex: "^https://.*"\nScore: 1

Manager -> PluginA: realize(url)
note right: Uses injected credentials:\nAuthorization: Bearer ${user.token}

PluginA --> Upload: file data
@enduml
```

**PR References:** #15497

---

## THEME 4: User-Driven Storage (2024)

### Slide 8: Paradigm Shift - User-Defined File Sources
- PR #18127: Users create their own file source instances
- Admin provides templates, users instantiate with their credentials
- Multiple instances per user (different projects, buckets)
- Credentials stored securely in Vault

**Proposed Diagram:** Template catalog architecture
```plantuml
@startuml
!theme plain

package "Admin Configuration" {
  [file_source_templates.yml] --> [Template: AWS S3]
  [file_source_templates.yml] --> [Template: Azure Blob]
  [file_source_templates.yml] --> [Template: Dropbox OAuth]
  
  note right of [Template: AWS S3]
    Template defines:
    - Variables (bucket, region)
    - Secrets (access_key, secret_key)
    - Jinja config template
  end note
}

package "User Actions" {
  actor User
  User --> [User Preferences]: create instance
  [User Preferences] --> [Template: AWS S3]: select
  [Template: AWS S3] --> [Fill Form]: bucket="my-project-1"
  [Fill Form] --> [Vault]: store secret_key
  [Vault] --> [UserFileSource DB]: instance saved
}

package "Runtime" {
  [ConfiguredFileSources] --> [UserFileSource DB]: load instances
  [UserFileSource DB] --> [Jinja Engine]: resolve template
  [Jinja Engine] --> [S3 Plugin]: instantiate with config
}
@enduml
```

**PR References:** #18127

---

### Slide 9: Template Anatomy and Jinja Templating
- Templates define: variables (user input), secrets (Vault), configuration
- Jinja templating (not Mako): preserves types, widely known
- Template versioning: users can upgrade instances
- Context: `user`, `secrets`, `variables`, `environ`

**Proposed Diagram:** Template resolution flow
```plantuml
@startuml
!theme plain

card "Template Definition" as Template {
  **variables:**
  - bucket: string
  - region: string
  
  **secrets:**
  - access_key
  - secret_key
  
  **configuration:**
  type: s3fs
  bucket: {{ variables.bucket }}
  region: {{ variables.region }}
  access_key: {{ secrets.access_key }}
}

card "User Input" as Input {
  bucket: "my-data-2024"
  region: "us-west-2"
  access_key: (from Vault)
  secret_key: (from Vault)
}

card "Resolved Config" as Resolved {
  type: s3fs
  bucket: "my-data-2024"
  region: "us-west-2"
  access_key: "AKIAIOSFODNN7EXAMPLE"
  secret_key: "wJalr..."
}

Template --> Input: User fills form
Input --> Resolved: Jinja resolution
Resolved --> [S3FS Plugin]: Instantiate

note bottom of Resolved
  Pydantic validation at each stage:
  1. Template structure
  2. User input types
  3. Resolved config correctness
end note
@enduml
```

**PR References:** #18127

---

### Slide 10: OAuth 2.0 Integration - Seamless Cloud Access
- PR #18272: OAuth authentication for user-defined sources
- Initial: Dropbox plugin with full OAuth flow
- Token storage in Vault (access + refresh tokens)
- Status tracking: connection health, token expiry

**Proposed Diagram:** OAuth flow sequence
```plantuml
@startuml
!theme plain

actor User
participant "Galaxy UI" as UI
participant "Galaxy Server" as Server
participant "Vault" as Vault
participant "Dropbox" as Dropbox

User -> UI: Create Dropbox instance
UI -> UI: Click "Authorize"
UI -> Server: Initiate OAuth
Server -> Dropbox: Redirect to authorization
Dropbox -> User: Request permissions
User -> Dropbox: Grant access
Dropbox -> Server: Callback with code
Server -> Dropbox: Exchange code for tokens
Dropbox -> Server: access_token + refresh_token
Server -> Vault: Store tokens securely
Vault --> Server: Stored
Server -> UI: Instance ready
UI -> User: Connected!

note right of Vault
  Tokens stored encrypted:
  - access_token (4hr expiry)
  - refresh_token (no expiry)
  - scopes granted
end note
@enduml
```

**PR References:** #18272

---

## THEME 5: Advanced Features (2024)

### Slide 11: Specialized Integrations - Zenodo and Pagination
- PR #18022: Zenodo plugin for DOI-backed archival
- Custom URI schemes: `zenodo://`, `invenio://`
- PR #18059: Server-side pagination for large repositories
- Performance: fast navigation of millions of files

**Proposed Diagram:** Pagination architecture
```plantuml
@startuml
!theme plain

participant "Client" as Client
participant "API" as API
participant "Plugin" as Plugin
participant "Remote Storage" as Storage

Client -> API: list(path, limit=100, offset=0)

alt Plugin supports pagination (e.g., Invenio, PyFilesystem2)
  API -> Plugin: list with limit/offset
  Plugin -> Storage: paginated query
  Storage --> Plugin: 100 items + total_count=1500
  Plugin --> API: {items: [...], total_matches: 1500}
  API --> Client: Page 1 of 15
else Plugin doesn't support pagination
  API -> Plugin: list(path)
  Plugin -> Storage: full listing
  Storage --> Plugin: ALL 1500 items
  Plugin --> API: 1500 items
  API -> API: Client-side pagination
  API --> Client: Page 1 of 15 (slow!)
end

note right of Client
  Pagination properties:
  - supports_pagination: bool
  - supports_search: bool  
  - supports_sorting: bool
end note
@enduml
```

**PR References:** #18022, #18059

---

## THEME 6: Modern Foundation (2025)

### Slide 12: Pydantic Revolution - Strong Typing
- PR #20728: Two-tier configuration system (template vs resolved)
- Pydantic v2 models for all configs
- Configuration linter: `make files-sources-lint`
- Runtime safety: errors caught at validation, not operation

**Proposed Diagram:** Two-tier configuration with validation
```plantuml
@startuml
!theme plain

class TemplateConfiguration {
  +root: Union[str, TemplateExpansion]
  +writable: Union[bool, TemplateExpansion]
  +bucket: TemplateExpansion
}

class ResolvedConfiguration {
  +root: str
  +writable: bool
  +bucket: str
}

class FilesSourceRuntimeContext {
  +resolved_config: ResolvedConfiguration
  +user: Optional[User]
}

card "YAML Config" as YAML {
  type: posix
  root: /data/${user.username}
  writable: ${environ.get('WRITABLE')}
}

YAML --> TemplateConfiguration: Parse & validate
TemplateConfiguration --> ResolvedConfiguration: Resolve variables
ResolvedConfiguration --> FilesSourceRuntimeContext: Runtime
FilesSourceRuntimeContext --> [Plugin Operations]: Use typed config

note bottom of TemplateConfiguration
  Pydantic validation stage 1:
  - Template syntax correct
  - Types match schema
end note

note bottom of ResolvedConfiguration
  Pydantic validation stage 2:
  - Variables resolved
  - Final types correct
end note
@enduml
```

**PR References:** #20728

---

### Slide 13: fsspec Integration - 40+ Backends
- PR #20698: `FsspecFilesSource` base class
- Simplifies plugins: 10x code reduction (500+ lines → 50 lines)
- Implements `_get_fs()`, framework handles rest
- Available backends: S3, Azure, GCS, HTTP, FTP, SSH, ZIP, Git, Zarr, etc.

**Proposed Diagram:** Plugin complexity comparison
```plantuml
@startuml
!theme plain

card "Before fsspec (Custom Implementation)" as Before {
  class MyFilesSource {
    +index(path, recursive)
    +realize(path, dest)
    +write_from(src, path)
    +exists(path)
    +delete(path)
    +mkdir(path)
    +rmdir(path)
    +size(path)
    +ctime(path)
    +permissions(path)
    --
    ~500+ lines of code
    --
    Handle:
    - Connection management
    - Error handling
    - Path normalization
    - Recursive listing
    - Streaming I/O
    - Retries
  }
}

card "After fsspec (Adapter)" as After {
  class MyFilesSource {
    +_get_fs(context): fsspec.AbstractFileSystem
    --
    ~10-50 lines of code
    --
    Example:
    return fsspec.filesystem(
      "s3",
      bucket=context.config.bucket,
      key=context.config.key
    )
  }
  
  note bottom
    Framework provides:
    - All FilesSource methods
    - Error handling
    - Path operations
    - Streaming
    - Pagination
  end note
}

Before -right-> After: PR #20698
@enduml
```

**PR References:** #20698

---

### Slide 14: Real-World Example - Hugging Face Integration
- PR #20805: Hugging Face Hub file source (AI/ML models)
- Built on fsspec: minimal code, full functionality
- User-defined template: configure repo, optional token
- 415 lines total (including tests, config, docs)

**Proposed Diagram:** Hugging Face integration simplicity
```plantuml
@startuml
!theme plain

class HuggingFaceFilesSource {
  plugin_type = "huggingface"
  
  +_get_fs(context):
    return fsspec.filesystem(
      "hf",
      repo_id=context.config.repo_id,
      token=context.config.token,
      repo_type=context.config.repo_type
    )
}

FsspecFilesSource <|-- HuggingFaceFilesSource

card "Template" as Template {
  **variables:**
  - repo_id: "google/flan-t5-small"
  - repo_type: "model"
  - revision: "main"
  
  **secrets:**
  - token (optional)
  
  **Example Usage:**
  Browse and import:
  - Pre-trained models
  - ML datasets  
  - Model checkpoints
  - Config files
}

HuggingFaceFilesSource --> Template: User configures

note bottom of HuggingFaceFilesSource
  Total implementation:
  ~50 lines of plugin code
  + Pydantic configs
  + User template
  = Full HF integration!
end note
@enduml
```

**PR References:** #20805

---

## THEME 7: Summary and Architecture

### Slide 15: Evolution Timeline - 5 Years of Innovation
- 2020: Foundation (plugins, templating)
- 2020-2021: Enhanced capabilities (write, security)
- 2023: Convergence (URLs unified)
- 2024: User-driven storage (templates, OAuth)
- 2025: Modern foundation (Pydantic, fsspec)

**Proposed Diagram:** Timeline with key milestones
```mermaid
gantt
    title Galaxy File Sources Evolution (2020-2025)
    dateFormat YYYY-MM
    section Foundation
    Plugin Architecture (PR #9888)           :milestone, 2020-07, 0d
    Write Support (PR #10152)                :milestone, 2020-09, 0d
    section Security
    Role/Group Permissions (PR #11769)       :milestone, 2021-04, 0d
    section Convergence
    URL Unification (PR #15497)              :milestone, 2023-02, 0d
    section User-Driven
    Zenodo Integration (PR #18022)           :milestone, 2024-04, 0d
    Pagination (PR #18059)                   :milestone, 2024-05, 0d
    User-Defined Sources (PR #18127)         :milestone, 2024-05, 0d
    OAuth 2.0 (PR #18272)                    :milestone, 2024-10, 0d
    section Modern
    Pydantic Typing (PR #20728)              :milestone, 2025-08, 0d
    fsspec Integration (PR #20698)           :milestone, 2025-08, 0d
    Hugging Face (PR #20805)                 :milestone, 2025-08, 0d
```

**PR References:** All

---

### Slide 16: Current Architecture - The Complete Picture
- Three tiers: Core framework → Base classes → Plugins
- Two paradigms: Global (admin) vs User-defined (template catalog)
- Two backend helpers: PyFilesystem2 (legacy) vs fsspec (modern)
- Key abstractions: ConfiguredFileSources, RuntimeContext, Template System

**Proposed Diagram:** Complete architecture diagram
```plantuml
@startuml
!theme plain

package "Core Framework" {
  [ConfiguredFileSources] as Manager
  [FilesSourceRuntimeContext] as Context
  [Template Manager]
  [Vault]
}

package "Base Classes" {
  [BaseFilesSource]
  [PyFilesystem2FilesSource]
  [FsspecFilesSource]
}

package "Plugins (Global)" {
  [Posix]
  [WebDAV]
  [HTTP]
  [DRS]
}

package "Plugins (User-Defined)" {
  [S3 (fsspec)]
  [Azure Blob (fsspec)]
  [Dropbox (OAuth)]
  [Zenodo (Invenio)]
  [Hugging Face (fsspec)]
}

package "Configuration" {
  database "UserFileSource DB" as DB
  [file_sources_conf.yml] as GlobalConfig
  [file_source_templates.yml] as Templates
}

' Connections
Manager --> Context
Manager --> [Template Manager]
[Template Manager] --> [Vault]
[Template Manager] --> DB

[BaseFilesSource] <|-- [PyFilesystem2FilesSource]
[BaseFilesSource] <|-- [FsspecFilesSource]

[BaseFilesSource] <|-- [Posix]
[PyFilesystem2FilesSource] <|-- [WebDAV]
[BaseFilesSource] <|-- [HTTP]
[BaseFilesSource] <|-- [DRS]

[FsspecFilesSource] <|-- [S3 (fsspec)]
[FsspecFilesSource] <|-- [Azure Blob (fsspec)]
[FsspecFilesSource] <|-- [Hugging Face (fsspec)]
[PyFilesystem2FilesSource] <|-- [Dropbox (OAuth)]
[BaseFilesSource] <|-- [Zenodo (Invenio)]

GlobalConfig --> Manager
Templates --> [Template Manager]
DB --> Manager

note right of Manager
  Routes URIs to plugins
  Manages lifecycle
  Handles serialization
end note

note bottom of [FsspecFilesSource]
  Modern approach:
  - 40+ backends
  - Minimal code
  - Well-tested
end note

note bottom of DB
  User instances:
  - Template reference
  - Resolved config
  - Vault secrets
  - Status tracking
end note
@enduml
```

**PR References:** All

---

## Diagram TODO List

1. **Before/After Plugin Architecture** - PlantUML component - Show hardcoded vs pluggable upload
2. **Plugin Interface and Operations** - PlantUML class - FilesSource interface with core methods
3. **Base Class Hierarchy** - PlantUML class - Inheritance from FilesSource to plugins
4. **Read vs Write Operations Flow** - PlantUML sequence - Import and export data flows
5. **Access Control Decision Tree** - PlantUML activity - Role/group permission checks
6. **URL Handling Convergence** - PlantUML component - Before/after URL routing
7. **URL Routing with Credentials** - PlantUML sequence - Pattern matching and auth injection
8. **Template Catalog Architecture** - PlantUML component - Admin templates to user instances
9. **Template Resolution Flow** - PlantUML activity/card - Jinja variable expansion
10. **OAuth Flow Sequence** - PlantUML sequence - Full OAuth authorization flow
11. **Pagination Architecture** - PlantUML sequence - Server-side vs client-side pagination
12. **Two-Tier Configuration** - PlantUML class/activity - Template vs resolved configs with validation
13. **Plugin Complexity Comparison** - PlantUML class/card - Before/after fsspec code reduction
14. **Hugging Face Integration** - PlantUML class - Simple plugin implementation
15. **Evolution Timeline** - Mermaid gantt - 5-year feature timeline
16. **Complete Architecture** - PlantUML component - Full system view with all layers

---

## Notes on Presentation Strategy

**Chronological Flow:**
- Start with problem (Slide 1)
- Show foundation (Slides 2-3)
- Build up capabilities (Slides 4-7)
- User empowerment (Slides 8-10)
- Advanced features (Slide 11)
- Modern refactoring (Slides 12-14)
- Synthesis (Slides 15-16)

**Key Themes to Emphasize:**
1. **Extensibility:** Plugin architecture enables unlimited backends
2. **Security:** Multi-layer access control (roles, groups, OAuth)
3. **User Empowerment:** From admin-only to user-driven storage
4. **Convergence:** Unifying URLs and file sources
5. **Developer Experience:** fsspec makes plugins trivial
6. **Type Safety:** Pydantic catches errors early

**Questions This Answers:**
- Why plugin architecture? (extensibility)
- Why unify URLs? (consistent auth, less code)
- Why user-defined? (scale to user needs)
- Why fsspec? (40+ backends, 10x less code)
- Why Pydantic? (type safety, validation)

**Code Examples to Show:**
- Template configuration (Slide 9)
- OAuth config snippet (Slide 10)
- fsspec _get_fs() implementation (Slide 13)
- Complete HF plugin (Slide 14)
