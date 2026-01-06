# lib/galaxy/schema/remote_files.py

## Galaxy Remote Files API Schemas Summary

**Core Models:**

The `remote_files.py` schema defines request/response models for Galaxy's file sources API. The architecture supports three primary file source types (ftpdir, userdir, importdir) and two response formats (flat URI-based and deprecated Jstree).

**File Source Plugins:**
- `FilesSourcePlugin` - Base metadata for plugins (id, type, label, writability, browsability, role/group restrictions)
- `BrowsableFilesSourcePlugin` - Extends plugin with URI root for file listing operations
- `FilesSourceSupports` - Capability flags: pagination, server-side search, and sorting support

**File/Directory Schemas:**
- `RemoteEntry` - Base model with name, URI, and path
- `RemoteFile` - Extends entry with size, creation time, optional hash list (MD5/SHA256)
- `RemoteDirectory` - Extends entry with class literal for type discrimination
- `RemoteFileHash` - Hash function + computed hash value pairs

**API Responses:**
- `ListUriResponse` - Modern response: list of RemoteFile or RemoteDirectory entries using discriminated union on "class_" field
- `ListJstreeResponse` - Legacy response format (deprecated)
- `AnyRemoteFilesListResponse` - Union supporting both formats

**Request Models:**
- `CreateEntryPayload` - Creates files: requires target plugin ID and entry name
- `CreatedEntryResponse` - Returns created entry name, URI, and optional external link

**Design Features:**
Discriminated unions enable type-safe polymorphic responses. The schema supports flexible pagination/search capabilities per plugin while maintaining consistent URI-based file identification across diverse remote backends (FTP, local directories, import systems).
