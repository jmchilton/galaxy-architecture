# lib/galaxy/managers/remote_files.py

## Galaxy Remote Files API Manager Summary

The **RemoteFilesManager** orchestrates file source operations for remote file browsing and listing in Galaxy. It serves as the primary interface between REST API endpoints and the underlying file source infrastructure.

**Orchestration & URI Resolution:**
The manager delegates URI handling to `ConfiguredFileSources`, which maintains a registry of file source plugins (FTP, import directories, HTTP, DRS, etc.). When given a target parameter, the manager maps standard Galaxy targets (`userdir`, `importdir`, `ftpdir`) to their corresponding URI schemes (`gxuserimport://`, `gximport://`, `gxftp://`). The `get_file_source_path()` method resolves URIs by finding the highest-scoring matching file source plugin, extracting the target path relative to that source's base.

**Directory Listing & Browsing:**
The `index()` method retrieves directory contents with optional filtering and formatting. It validates user access before delegating to the resolved file source's `list()` method, which returns a tuple of (entries, total_count) supporting pagination, search, and sorting. The manager applies post-processing based on the requested format: **flat** (files only, sorted by path), **uri** (raw entries), or **jstree** (hierarchical tree with disable modes for folders/files).

**User Context & Access Control:**
Access is mediated through `ProvidesFileSourcesUserContext`, which encapsulates user identity (email, username), role/group memberships, FTP directory paths, and admin status. This context is passed to both URI validation and file source operations, ensuring operations respect user permissions and Galaxy configuration constraints.

**Entry Creation:**
The `create_entry()` method mirrors listing logic: validates the URI root, resolves the file source, and delegates creation while preserving user context and error handling patterns.

**Integration Points:**
ConfiguredFileSources manages plugin lifecycle, validates URIs against Galaxy configuration (checking for enabled directories, user permissions), and applies role-based filtering for available sources.
