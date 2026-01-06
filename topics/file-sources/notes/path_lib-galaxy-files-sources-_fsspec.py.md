# lib/galaxy/files/sources/_fsspec.py

## FsspecFilesSource Base Class Summary

**FsspecFilesSource** is an abstraction layer that enables Galaxy file sources to leverage fsspec (filesystem specification), a unified Python interface for various remote storage systems (S3, GCS, Azure, SFTP, FTP, etc.).

### Key Design

The class acts as a bridge between Galaxy's file source plugin system and fsspec's AbstractFileSystem API. Subclasses need only implement `_open_fs()` to instantiate an fsspec filesystem handle—FsspecFilesSource handles all common operations.

### Core Methods Provided

- **`_list()`** – Directory listing with pagination, recursive traversal, and glob-based filtering. Results returned with total count for pagination support.
- **`_realize_to()` / `_write_from()`** – Download/upload operations delegated to fsspec's `get_file()` and `put_file()` methods.
- **`_info_to_entry()`** – Converts fsspec file metadata into Galaxy RemoteFile/RemoteDirectory objects.
- **`_extract_timestamp()` / `_get_file_hashes()`** – Customizable metadata extraction for timestamps and checksums.
- **`_adapt_entry_path() / _to_filesystem_path()`** – Path translation hooks for virtual-to-filesystem mapping.

### What Subclasses Must Implement

Only one abstract method:
- **`_open_fs()`** – Instantiate and return an fsspec AbstractFileSystem configured with credentials and connection parameters.

Optional customization points for specialized behavior (metadata extraction, path transformation).

### Benefits of fsspec Abstraction

1. **Unified Interface** – Write once, support 40+ storage backends (S3, Azure, GCS, SSH, FTP, etc.)
2. **Credential Management** – Galaxy's configuration system injects credentials; fsspec handles auth.
3. **Common Features** – Pagination, searching, caching, permission handling built-in.
4. **Scalability Safeguards** – MAX_ITEMS_LIMIT prevents browser/memory exhaustion with large directories.
5. **Minimal Plugin Code** – Subclasses focus on fsspec instantiation, not filesystem operations.

FsspecFilesSource democratizes adding new remote storage backends to Galaxy—contributors implement only connection logic, not file operations.
