# PR #20698: Add fsspec base implementation for File Source plugins

**Author:** David López (@davelopez)
**Merged:** August 20, 2025
**URL:** https://github.com/galaxyproject/galaxy/pull/20698
**Requires:** PR #20728 (Pydantic refactoring)
**Related Issue:** #20415

## Overview

Adds **fsspec adapter base class** enabling integration of any [fsspec-compatible](https://filesystem-spec.readthedocs.io/en/latest/index.html) filesystem backend into Galaxy's File Sources framework. Dramatically simplifies adding new file source types.

## fsspec Background

### What is fsspec?

**Filesystem Spec** (fsspec) is a Python specification for filesystem interfaces:
- Unified API across diverse storage backends
- Large ecosystem of implementations
- Well-maintained, widely adopted
- Used by pandas, dask, zarr, etc.

### Available Backends

fsspec supports 40+ backends including:
- **Cloud**: S3, Azure Blob, GCS, Dropbox, OneDrive
- **Network**: HTTP, FTP, SFTP, WebDAV
- **Archives**: ZIP, TAR, 7z
- **Special**: Git, GitHub, Hugging Face, DVC
- **Local**: OSFS, Memory, Temp

## FsspecFilesSource Base Class

### Purpose

Adapter that wraps any fsspec filesystem for Galaxy:
- Implements Galaxy FilesSource interface
- Delegates operations to fsspec backend
- Handles Galaxy-specific concerns (quotas, permissions, etc.)
- Simplifies plugin development

### Architecture

```python
class FsspecFilesSource(BaseFilesSource[TTemplateConfig, TResolvedConfig]):
    """Base class for fsspec-backed file sources"""

    def _get_fs(self, context: FilesSourceRuntimeContext) -> AbstractFileSystem:
        """Return fsspec filesystem for this backend"""
        raise NotImplementedError

    # Galaxy operations delegated to fsspec:
    # - _list() → fs.ls()
    # - _realize() → fs.get()
    # - _write_from() → fs.put()
    # - _exists() → fs.exists()
    # ...
```

### Plugin Implementation

Plugins only need to:
1. Define configuration models
2. Implement `_get_fs()` to return configured fsspec filesystem

Example:
```python
class MemoryFilesSource(FsspecFilesSource[MemoryTemplateConfig, MemoryConfig]):
    plugin_type = "memory"

    def _get_fs(self, context: FilesSourceRuntimeContext[MemoryConfig]):
        return fsspec.filesystem("memory")
```

## Implementations Included

### 1. TempFilesSource (Migrated)

**Before:** Custom implementation
**After:** Extends FsspecFilesSource using OSFS backend

Benefits:
- Less code
- Better tested (fsspec)
- More features (free from fsspec)

### 2. MemoryFilesSource (New, Non-Production)

In-memory filesystem for testing:
- No disk I/O
- Fast test execution
- Verifies FsspecFilesSource integration

```python
class MemoryFilesSource(FsspecFilesSource[MemoryTemplateConfig, MemoryConfig]):
    plugin_type = "memory"
    template_config_class = MemoryTemplateConfiguration
    resolved_config_class = MemoryConfiguration

    def _get_fs(self, context):
        return fsspec.filesystem("memory")
```

## BaseFileSourceTestSuite

Generic test suite for file sources:
- Tests basic functionality
- Requires writable and browsable file source
- Reusable across implementations

```python
class TestMyFileSource(BaseFileSourceTestSuite):
    def _get_file_source(self):
        return MyFilesSource(config)

    # Inherits:
    # - test_list()
    # - test_write()
    # - test_read()
    # - test_delete()
    # - test_exists()
    # ...
```

## Developer Benefits

### Before fsspec Base

To add new file source type:
1. Implement full FilesSource interface (~15 methods)
2. Handle edge cases (permissions, errors, etc.)
3. Write comprehensive tests
4. Maintain backend-specific code

~500+ lines of code per plugin

### After fsspec Base

To add new file source type:
1. Define Pydantic configs
2. Implement `_get_fs()` method (~10 lines)
3. Use BaseFileSourceTestSuite

~50-100 lines of code per plugin

**10x reduction in code!**

## Use Cases Enabled

### Easy Cloud Integration

Adding GCS file source:
```python
class GCSFilesSource(FsspecFilesSource[GCSTemplateConfig, GCSConfig]):
    plugin_type = "gcs"

    def _get_fs(self, context: FilesSourceRuntimeContext[GCSConfig]):
        return fsspec.filesystem(
            "gcs",
            token=context.resolved_config.credentials
        )
```

### Archive File Sources

Browse ZIP files as folders:
```python
class ZipFilesSource(FsspecFilesSource[ZipTemplateConfig, ZipConfig]):
    plugin_type = "zip"

    def _get_fs(self, context):
        return fsspec.filesystem(
            "zip",
            fo=context.resolved_config.zip_path
        )
```

### Version Control Systems

Access GitHub repos:
```python
class GitHubFilesSource(FsspecFilesSource[GitHubTemplateConfig, GitHubConfig]):
    plugin_type = "github"

    def _get_fs(self, context):
        return fsspec.filesystem(
            "github",
            org=context.resolved_config.org,
            repo=context.resolved_config.repo
        )
```

## Testing Strategy

### BaseFileSourceTestSuite

Verifies:
- Directory listing
- File reading/writing
- Existence checks
- Deletion operations
- Error handling
- Permission enforcement

### Per-Backend Tests

Additional tests for:
- Backend-specific features
- Configuration validation
- Edge cases

### Mock Backends

MemoryFilesSource enables:
- Fast unit tests
- No external dependencies
- Predictable state

## Future File Sources

With fsspec base, adding these becomes trivial:
- **OneDrive**: `fsspec.filesystem("onedrive")`
- **Git**: `fsspec.filesystem("git")`
- **HDFS**: `fsspec.filesystem("hdfs")`
- **IPFS**: `fsspec.filesystem("ipfs")`
- **SSH**: `fsspec.filesystem("ssh")`
- **WebDAV**: `fsspec.filesystem("webdav")` (replace PyFilesystem2)
- **Zarr**: `fsspec.filesystem("zarr")`

All with minimal code!

## Documentation Implications

### Key Concepts to Cover

1. **fsspec Ecosystem**: What it is, why we use it
2. **FsspecFilesSource Base**: How adapter pattern works
3. **Plugin Development**: Creating fsspec-backed file sources
4. **Testing**: Using BaseFileSourceTestSuite

### Plugin Development Guide

**Creating fsspec File Source:**
```
1. Choose fsspec backend from registry
2. Define Pydantic configs (template + resolved)
3. Implement _get_fs() to return configured filesystem
4. Use BaseFileSourceTestSuite for testing
5. Document configuration options
```

### Admin Guide

- Understanding which file sources use fsspec
- Configuration for fsspec backends
- Performance characteristics
- Troubleshooting fsspec issues

### Benefits Documentation

**For Plugin Developers:**
- Minimal code required
- Leverage well-tested fsspec backends
- Focus on configuration, not implementation

**For Galaxy:**
- Rapidly expand file source ecosystem
- Consistent behavior across backends
- Reduced maintenance burden

## Migration Path

### Existing PyFilesystem2 Plugins

Can migrate to fsspec:
- WebDAV: PyFilesystem2 → fsspec webdav
- Dropbox: PyFilesystem2 → fsspec dropbox

Benefits:
- Better maintained backends
- More features
- Less code

### Compatibility

FsspecFilesSource coexists with:
- PyFilesystem2-based sources
- Custom implementations
- No forced migration

## Technical Details

**Diff size:** 1,304 lines
**Dependencies:** Adds fsspec as dependency
**Testing:** Includes BaseFileSourceTestSuite and MemoryFilesSource tests
**Refactoring:** Migrates TempFilesSource to fsspec
**Breaking Changes:** None (new base class, existing plugins unchanged)

## Related Work

**Issue #20415:** Request for broader filesystem backend support
**PR #20728:** Pydantic refactoring enables typed fsspec integration
