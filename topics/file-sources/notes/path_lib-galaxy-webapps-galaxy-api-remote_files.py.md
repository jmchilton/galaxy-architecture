# lib/galaxy/webapps/galaxy/api/remote_files.py

## Galaxy Remote Files Browsing API Summary

The remote files API provides three primary endpoints for file source interaction:

**1. Directory Browsing & File Listing (`GET /api/remote_files`)**
Lists available files/directories from configured sources (ftpdir, userdir, importdir). Supports multiple response formats: `uri` (default, returns file/directory objects with metadata), `flat` (simple file list), and `jstree` (deprecated tree structure). Recursive directory traversal is configurable. Pagination via `limit`/`offset` parameters; total match count returned in `total_matches` response header. Optional search and sort_by parameters for source-specific filtering. The `disable` parameter (jstree format only) can exclude folders or files from results.

**2. File Source Plugins (`GET /api/remote_files/plugins`)**
Enumerates available gxfiles:// URI targets with plugin metadata (id, type, label, documentation, capabilities). Returns only browsable sources by default, excluding non-listable sources like `http` and `base64`. Filters by `include_kind` and `exclude_kind` parameters to narrow plugin results. Each plugin reports support capabilities (pagination, search, sorting) and access restrictions (roles/groups).

**3. Entry Creation (`POST /api/remote_files`)**
Creates new directories/records on writable file sources. Accepts target (source identifier) and name parameters. Returns created entry details including URI and optional external link. Write intent can be specified via `write_intent` query parameter to filter only writable sources during browsing.

URI-based access uses standardized entry objects distinguishing files (with size, creation time, optional hashes) from directories. Integration with pluggable file sources enables extensible backend support across FTP, user directories, import locations, and custom protocols.
