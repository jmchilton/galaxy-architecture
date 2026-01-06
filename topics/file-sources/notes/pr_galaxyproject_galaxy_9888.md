# PR #9888: Pluggable URI handling across upload components (File Sources)

**Author:** John Chilton (@jmchilton)
**Merged:** July 27, 2020
**URL:** https://github.com/galaxyproject/galaxy/pull/9888

## Overview

This PR introduces the foundational **File Sources** architecture - a pluggable framework for accessing filesystem-like entities during upload. It generalizes and formalizes existing file sources (FTP, library imports) and enables new remote file source integrations (Dropbox, WebDAV, etc.).

## Key Architectural Components

### FilesSource Plugin Interface

- **Purpose**: Abstract interface for sources of directories and files during upload
- **Core Operations**:
  - **Indexing**: List directory hierarchies for client navigation
  - **Realize**: Download files to local POSIX directories for dataset ingestion
- **Base Classes**:
  - `BaseFilesSource`: General-purpose helper implementation
  - `PyFilesystem2FilesSource`: Assumes PyFilesystem2 backend (simplifies plugin development)

### ConfiguredFileSources Manager

- **Responsibility**: Manages all FilesSource plugin instances
- **Key Features**:
  - Maps URIs to appropriate plugin instances
  - Uses `galaxy.util.plugin_config` for YAML/XML plugin definitions
  - **Serializable**: Can persist to JSON for job execution (where web transaction unavailable)
  - **Adapter Pattern**: Extracts user-level info from `trans` object in Galaxy app context

### URI Scheme

File sources use custom URI schemes:
- `gxfiles://<plugin-id>/path/to/file` - User-configured plugins
- `gxftp://` - User's FTP directory (auto-populated if `ftp_upload_dir` configured)
- `gximport://` - Library import directory (auto-populated if `library_import_dir` configured)
- `gxuserimport://` - User library import directory (auto-populated if `user_library_import_dir` configured)

## Plugin Implementations Included

### 1. posix Plugin
- Direct implementation extending `BaseFilesSource`
- Preserves Galaxy's security checks for symlinks
- Respects `user_library_import_symlink_allowlist` semantics

### 2. webdav Plugin
- Extends `PyFilesystem2FilesSource`
- Enables OwnCloud integration (building on prior work)
- Supports templating for user preferences or environment variables

Example configurations:
```yaml
# User-configured OwnCloud
- type: webdav
  id: owncloud1
  label: OwnCloud
  url: ${user.preferences['owncloud|url']}
  login: ${user.preferences['owncloud|username']}
  password: ${user.preferences['webdav|password']}

# Centralized lab server
- type: webdav
  id: lab
  label: Lab WebDAV server
  url: http://ourlab.org:7083
  login: ${environ.get('WEBDAV_LOGIN')}
  password: ${environ.get('WEBDAV_PASSWORD')}
```

### 3. dropbox Plugin
- Extends `PyFilesystem2FilesSource`
- Requires Dropbox access token (can be app-folder scoped for security)

```yaml
- type: dropbox
  id: dropbox1
  label: Dropbox Files
  accessToken: ${user.preferences['dropbox|access_token']}
```

## Configuration Templating

YAML configs support Cheetah templates with access to:
- `user` - User object and preferences
- `config` - Galaxy configuration
- `environ` - Server environment variables

## Integration Points

### Upload Dialog
- Modified to support "select remote files" (generalizing FTP-specific UI)
- Navigates hierarchical file sources
- Preserves all advanced upload options (format detection, dbkey, collections, rules, etc.)

### Data Fetch Tool (`__DATA_FETCH__`)
- Uses FilesSource.realize() to download files during upload
- Works with serialized ConfiguredFileSources in job context

### Remote Files API
- Provides directory hierarchies to client
- Builds URIs for file selection

## Design Decisions

### Why Not a Tool?
Upload dialog has many advanced options (format conversion, dbkey selection, collection organization, rules) that would be difficult to replicate in a tool. File Sources integrate seamlessly with existing upload UX.

### FilesSource vs ObjectStore
- **ObjectStore**: Manages datasets with flat logical organization, includes extra files
- **FilesSource**: Manages files/directories in hierarchical fashion, meant for browsing

## Documentation Implications

### Key Concepts to Cover
1. Plugin architecture and base classes
2. URI scheme design (`gxfiles://`, `gxftp://`, etc.)
3. ConfiguredFileSources manager and serialization
4. Templating system for user preferences
5. Security model (symlink checks, allowlists)

### Code Examples to Highlight
- Implementing a custom FilesSource plugin
- Configuring built-in plugins (posix, webdav, dropbox)
- Using templating for user preferences
- How realize() and indexing work

### Visual Aids
- Architecture diagram showing FilesSource → ConfiguredFileSources → Upload components
- URI scheme mapping
- Plugin configuration examples
- Upload dialog workflow

## Future Directions Mentioned

- Terra integration via FISS library
- Additional PyFilesystem2 backends (S3, Basespace, Google Drive, OneDrive)
- Tool form support for file selection and directory export
- Writable file sources for collection archives, history exports
- Generalized data export tools (cloud send)

## Technical Details

**Diff size:** 3016 lines
**Test coverage:** Unit tests ensure serialization/deserialization works correctly across Galaxy app and job contexts
