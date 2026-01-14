# lib/galaxy/files/sources/_pyfilesystem2.py

## PyFilesystem2FilesSource Base Class Summary

PyFilesystem2FilesSource is an abstract base class that integrates Galaxy's file source abstraction with the PyFilesystem2 library (fs), enabling unified access to diverse remote filesystems through a common interface. It handles FTP, SFTP, WebDAV, cloud storage (Azure, Google Cloud, Dropbox), and other fs-compatible backends.

**PyFilesystem2 Integration Approach:**
- Subclasses implement abstract method `_open_fs()` to instantiate protocol-specific FS objects (e.g., FTPFS, WebDAVFS)
- Config-driven: all connection parameters resolved before opening filesystem handle
- Context manager pattern: filesystems opened/closed with each operation
- Pagination and search supported natively via fs.filterdir() and fs.walk()

**Key Differences from fsspec:**
- **Pagination:** PyFS2 supports server-side pagination via filterdir(page=(start,end)) for efficient large directory listing; fsspec loads entire directories then slices client-side
- **Search:** PyFS2 uses glob-style patterns (*query*) natively; fsspec requires explicit glob pattern building
- **Error handling:** PyFS2 raises fs.errors.FSError hierarchy (PermissionDenied, etc.); fsspec uses standard Python exceptions
- **Recursion:** Both walk directories, but PyFS2 handles KeyError exceptions (webdav workaround) that fsspec doesn't
- **Resource metadata:** PyFS2 requires "details" namespace in fs.walk()/filterdir(); fsspec uses detail=True returning dicts

**Core Methods:**
- `_list()` - Directory enumeration with optional recursion, filtering, pagination
- `_realize_to()` - Download files via fs.download()
- `_write_from()` - Upload files via fs.upload() with automatic parent directory creation
- `_resource_info_to_dict()` - Converts PyFS2 ResourceInfo objects to RemoteFile/RemoteDirectory entries

**When to Use PyFilesystem2 vs fsspec:**
- **Use PyFilesystem2** when integrating protocols already in the fs ecosystem (FTP, WebDAV, SSH, cloud storage SDKs) and server-side pagination is beneficial
- **Use fsspec** for wider ecosystem support (S3, GCS have native fsspec implementations) and when detailed metadata (hashes, timestamps) is required
