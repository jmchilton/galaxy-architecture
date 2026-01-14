# PR #18127: User-Defined File Sources (Template Framework)

**Author:** John Chilton (@jmchilton)
**Merged:** May 2024
**URL:** https://github.com/galaxyproject/galaxy/pull/18127
**Foundation PRs:** #14073 (object store selection), #12940 (vault), #18117 (object store overhaul), #15875 (object store templates)
**Implements Issues:** #13816, Fixes #8790

## Overview

**Major architectural addition** enabling users to create their own file sources and object stores from admin-provided templates. Users can now instantiate multiple personal storage connections for different projects, with credentials stored securely in Galaxy's Vault.

This represents a paradigm shift from admin-only global configuration to user-driven storage management.

## Core Concepts

### Datasets vs Files, Object Stores vs File Sources

**File Sources:**
- Provide access to raw files organized hierarchically
- Used for importing data into Galaxy
- Browsable folders and files
- Configured via `file_sources_config_file` (defaults to `file_sources_conf.yml`)

**Object Stores:**
- Store Galaxy datasets (files + metadata + ownership)
- User selects storage location for histories/workflows
- Configured via `object_store_config_file` (defaults to `object_store_conf.xml/yml`)
- Quotas managed separately from Galaxy's default quota

### Global vs User-Defined

**Global Sources** (traditional):
- Admin-configured, available to all users
- Single instance shared across users
- Some templating via user preferences possible
- High education burden for users

**User-Defined Sources** (this PR):
- Users instantiate from admin templates
- Multiple instances per user (different projects)
- Unified UI with clear configuration
- Applies to both file sources AND object stores

## Template Catalog System

### Configuration Files

**file_source_templates.yml:**
```yaml
- id: template_id
  name: Human Readable Name
  description: Markdown description shown in UI
  variables:
    var_name:
      type: string
      help: Description for users
  secrets:
    secret_name:
      help: Description for secure credential
  configuration:
    # File source configuration with Jinja templating
```

**object_store_templates.yml:**
```yaml
- id: template_id
  name: Human Readable Name
  description: Markdown description
  variables: {...}
  secrets: {...}
  configuration:
    # Object store configuration with Jinja templating
```

### Template Versioning

- Templates can be versioned (v0, v1, ...)
- Old versions automatically hidden when new version added
- Users can upgrade instances to newer template versions
- UI supports re-running with newer versions (like tool versioning)
- Old template definitions preserved for existing instances

### Production-Ready Templates Included

**File Sources:**
- `production_azure.yml` - Azure Blob Storage
- `production_ftp.yml` - FTP servers
- `production_s3fs.yml` - S3FS-based buckets
- `production_aws_private_bucket.yml` - Private AWS S3
- `production_aws_public_bucket.yml` - Public AWS S3

**Object Stores:**
- `production_azure_blob.yml` - Azure Blob
- `production_aws_s3.yml` - AWS S3 (modern)
- `production_aws_s3_legacy.yml` - AWS S3 (legacy)
- `production_generic_s3.yml` - Generic S3 (modern)
- `production_generic_s3_legacy.yml` - Generic S3 (legacy)
- `production_gcp_s3.yml` - Google Cloud Storage (S3 interop)

All templates tested, documented, with screenshots.

## Jinja Templating Engine

### Why Jinja over Python/Mako

- **Preserves type information** (critical for structured configs)
- Consistent with Galaxy's direction toward typed configurations
- Well-documented, widely used
- Allows template composition (admins can template templates with Ansible)

### Jinja Environment

Templates have access to:
- `user` - User object with username, email, preferences
- `secrets` - Secure credentials from Vault
- `variables` - User-provided configuration values
- `environ` - Server environment variables (for admin injection)

### Admin Injection

Admins can inject:
- Global Vault values
- Environment variables
- Computed values

Example:
```yaml
configuration:
  bucket: '{{ user.username }}-data'
  access_key: '{{ environ.get("S3_ACCESS_KEY") }}'
  secret_key: '{{ secrets.user_secret }}'
```

## Database Models

### UserFileSource
```python
class UserFileSource(Base, HasConfigTemplate):
    id: Mapped[int]
    user_id: Mapped[Optional[int]]  # Could support groups/roles
    uuid: Mapped[Union[UUID, str]]
    create_time: Mapped[datetime]
    update_time: Mapped[datetime]
    name: Mapped[str]  # User-specified instance name
    description: Mapped[Optional[str]]
    hidden: Mapped[bool]  # Active but not in selection UI
    active: Mapped[bool]  # Deactivate without deleting
    purged: Mapped[bool]  # Cannot reactivate (secrets purged)
    template_id: Mapped[str]
    template_version: Mapped[int]
    template_definition: Mapped[CONFIGURATION_TEMPLATE_DEFINITION_TYPE]  # JSON
    template_variables: Mapped[CONFIGURATION_TEMPLATE_CONFIGURATION_VARIABLES_TYPE]  # JSON
    template_secrets: Mapped[CONFIGURATION_TEMPLATE_CONFIGURATION_SECRET_NAMES_TYPE]  # JSON (names only)
```

### UserObjectStore
Similar structure to UserFileSource but for object stores.

### Design Decision: Store Full Template Definition

Templates stored in each instance (not just id/version reference):
- **Pros**: Stable across template catalog changes
- **Cons**: Duplication, harder to update globally
- Chosen for stability and version independence

## Backend Architecture

### Decoupling Layers

**lib/galaxy/managers/file_source_instances.py:**
- Ties together: database, vault, templates, factory methods
- CRUD operations for file source instances
- Create, update, upgrade operations
- Isolated from rest of Galaxy

**lib/galaxy/managers/object_store_instances.py:**
- Similar role for object stores
- Connects user instances to object store framework

### Strict Pydantic Validation

- All templates validated with Pydantic v2
- All generated configurations validated
- JSON blobs in database strictly typed
- Backward compatibility guaranteed through versioning
- Documentation auto-generated from models

## API Endpoints

### File Source Instance API
- `GET /api/file_source_templates` - List available templates
- `POST /api/file_source_instances` - Create instance from template
- `PUT /api/file_source_instances/{id}` - Update variables
- `PUT /api/file_source_instances/{id}/secret/{secret_name}` - Update secret
- `POST /api/file_source_instances/{id}/upgrade` - Upgrade to new template version

### Object Store Instance API
Parallel endpoints for object stores.

## User Interface

### User Preferences Menu
New options:
- "Manage Your File Sources"
- "Manage Your Object Stores"

### Template Selection
- Card-based selection UI
- Hover shows Markdown description
- Template version displayed
- Badges indicate storage properties

### Instance Creation Forms
Dynamic forms generated from template definition:
- Variables as form fields (typed: string, integer, boolean, etc.)
- Secrets as password fields (stored in Vault)
- Help text from template
- Real-time validation

### Instance Management
- List all instances
- Show status (active, hidden, purged)
- Edit variables
- Update secrets (masked in UI)
- Upgrade to new versions
- Activate/deactivate
- Delete (with purge option)

## Use Cases

### 1. Multi-Project S3 Buckets
User creates separate S3 file sources for different research projects, each with different buckets and credentials.

### 2. Personal Cloud Storage
Users connect their personal Dropbox, Google Drive, Azure accounts without admin involvement.

### 3. Grant-Specific Storage
Researchers use grant-funded cloud storage by instantiating object stores with project-specific credentials.

### 4. Bring Your Own Storage
Users pay for their own cloud storage instead of consuming Galaxy quota.

## Documentation Implications

### Extensive Admin Documentation

Included in PR:
- Template syntax reference
- Variable types and validation
- Secret management with Vault
- Jinja templating guide
- Ansible composition patterns
- Badge system for storage properties
- Screenshots of all production templates

### Key Concepts to Cover

1. **Template Catalog Architecture**: How templates → instances works
2. **Jinja Templating**: Variable/secret interpolation patterns
3. **Vault Integration**: Secure credential storage
4. **Template Versioning**: Upgrading user instances
5. **Admin vs User Responsibilities**: Who configures what
6. **Quota Management**: User-defined object stores bypass default quotas

### Configuration Examples

**Simple Posix Template:**
```yaml
- id: user_posix
  name: Personal Folder
  variables:
    folder_name:
      type: string
      help: Folder name in shared area
  configuration:
    type: posix
    root: '/shared/{{ user.username }}/{{ variables.folder_name }}'
```

**AWS S3 with Secrets:**
```yaml
- id: aws_s3
  name: AWS S3 Bucket
  variables:
    bucket:
      type: string
    access_key:
      type: string
  secrets:
    secret_key:
      help: AWS secret access key
  configuration:
    type: aws_s3
    bucket:
      name: '{{ variables.bucket }}'
    auth:
      access_key: '{{ variables.access_key }}'
      secret_key: '{{ secrets.secret_key }}'
```

### Visual Aids from PR

Screenshots included for:
- Template selection UI
- Form generation for each production template
- Instance management interface
- Status indicators for OAuth2 services
- Badge display for storage properties

## Requirements

**For User-Defined Object Stores:**
- Distributed object store configured
- Vault setup recommended for secrets

**For User-Defined File Sources:**
- Vault recommended for credentials

## Technical Details

**Diff size:** 14,826 lines (massive)
**Testing:** Selenium tests for all production templates
**Database Migrations:** New tables for UserFileSource, UserObjectStore
**Backward Compatibility:** Global sources continue working unchanged
