# lib/galaxy/files/sources/__init__.py

## Galaxy FilesSource Architecture Summary

**FilesSource** is Galaxy's abstraction layer for remote file system access, implementing a plugin-based architecture with three core base classes:

### Core Base Classes

1. **SingleFileSource** (lines 83-196): Abstract base for handling individual remote files. Implementations must define:
   - `get_writable()` → bool: Write capability indicator
   - `user_has_access(user_context)` → bool: Authorization check
   - `realize_to(source_path, native_path, opts)`: Copy remote file to local filesystem
   - `write_from(target_path, native_path, opts)` → str: Upload local file to remote location
   - `score_url_match(url)` → int: Scoring logic for URI matching (0 = unsupported, max = URI length)
   - `to_relative_path(url)` → str: Normalize URLs to relative paths
   - `to_dict(for_serialization, user_context)` → dict: Serialization interface
   - `prefer_links()` → bool: Link preference flag

2. **SupportsBrowsing** (lines 198-223): Mixin interface for browsable sources:
   - `get_uri_root()` → str: Returns URI prefix (e.g., `gxfiles://bucket/`)
   - `list(path, recursive, user_context, opts, limit, offset, query, sort_by)` → tuple: Directory listing with pagination/search support

3. **FilesSource** (lines 226-237): Combined interface inheriting both above classes, adding:
   - `get_browsable()` → bool: Indicates SupportsBrowsing implementation

### BaseFilesSource Implementation (lines 244-591)

Generic base class providing concrete implementations with **template configuration resolution**:

**Configuration System:**
- `template_config_class`: Template config with variable placeholders
- `resolved_config_class`: Final config after template resolution
- `_evaluate_template_config(user_data)`: Resolves placeholders using user context/environment

**Key Methods:**
- `get_uri_root()`: Constructs URIs from scheme + prefix (e.g., `scheme://id/`)
- `score_url_match(url)`: Prefix-based matching
- `user_has_access()`: Validates roles/groups using boolean expressions
- `list()`: Wrapper validating pagination/search/sort capabilities
- `_list()`, `_realize_to()`, `_write_from()`: Abstract methods for subclass implementation
- `to_dict()`: Serializes source metadata + optional runtime configuration

**URI Handling:**
- `uri_join(*args)`: Non-standard scheme-aware path joining
- Default scheme: `gxfiles://` (overridable per source)

**Security:** Role/group-based access control via boolean expression evaluation (lines 565-590).
