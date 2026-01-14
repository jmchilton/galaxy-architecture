# lib/galaxy/files/sources/posix.py

## POSIX FilesSource Plugin Summary

### Overview
The **PosixFilesSource** is Galaxy's concrete implementation for accessing files via the local POSIX filesystem. It serves as the foundation for three critical stock plugins: FTP directory access, library imports, and user library imports. The implementation emphasizes security while providing flexible file operations.

### Scenarios Handled
1. **User FTP Uploads** - Maps user-specific FTP directories via template expansion (`${user.ftp_dir}`)
2. **Library Imports** - Central library import directory (`${config.library_import_dir}`)
3. **User Library Imports** - Per-user import directories (`${config.user_library_import_dir}/${user.email}`)

### FilesSource Interface Implementation
The plugin implements core operations through four methods:

- **_list()** - Enumerates directory contents with optional recursion; blocks root-level access if unconfigured
- **_realize_to()** - Copies or moves files from source path to Galaxy's native path; supports delete-on-realize semantics
- **_write_from()** - Writes from Galaxy to target path with atomic writes using `.part` temporary files; optionally creates parent directories
- **_resource_info_to_dict()** - Marshals filesystem metadata (size, timestamps) into RemoteFile/RemoteDirectory objects

### Configuration Options
**PosixConfiguration** exposes four security-critical settings:

- `root` - Base directory (template-expandable); optional for read-only access
- `enforce_symlink_security` - Validates paths against allowlist (default: true)
- `delete_on_realize` - Move vs copy semantics (default: false; FTP overrides to true)
- `allow_subdir_creation` - Permit parent directory creation during writes (default: true)
- `prefer_links` - Optimization hint for internal file handling

### Security Considerations
1. **Symlink Resolution** - `safe_contains()` prevents breakout via symlink traversal when enforcement enabled
2. **Path Normalization** - All paths converted to native format and validated before filesystem operations
3. **Access Control** - Admin-only write fallback when root unconfigured; runtime context includes user data for authorization
4. **Atomic Writes** - Files written to `.part` files then renamed, preventing partial reads
5. **Allowlist Integration** - Respects Galaxy's configurable symlink allowlist for trusted paths

### Design Pattern
Demonstrates effective plugin architecture: three built-in stock sources inherit from POSIX core, customizing only the root path template and scheme identifier while reusing all security-sensitive file handling logic.
