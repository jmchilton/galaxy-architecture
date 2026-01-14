# PR #18059: Add pagination support to Files Source plugins

**Author:** David López (@davelopez)
**Merged:** May 21, 2024
**URL:** https://github.com/galaxyproject/galaxy/pull/18059

## Overview

Adds **server-side pagination, filtering, and sorting** to File Sources plugins, addressing performance issues when browsing large repositories. Previously, all files were loaded client-side, making navigation slow for sources with many files.

## Problem Addressed

### Previous Approach Limitations
- Retrieved ALL files/directories from remote sources
- Client-side pagination and search
- Adequate for small sources
- Very slow for large repositories (thousands+ files)
- Difficult navigation for vast file collections

## Key Features

### 1. Server-Side Pagination

New plugin property: `supports_pagination`
- Signals client to delegate pagination to server
- Passes `limit` and `offset` parameters
- Only applicable in non-recursive view
- Requires server-side sorting/filtering

### 2. Server-Side Search/Filtering

New plugin property: `supports_search`
- Plugin can filter by search query
- Query syntax plugin-specific
- Minimum requirement: search by name
- Client delegates search to capable plugins

### 3. Server-Side Sorting

New plugin property: `supports_sorting`
- Most plugins won't support this
- Signals client to disable UI sorting when unsupported
- Ensures listings stay synchronized with server

### 4. Total Matches Metadata

API now returns total match count:
- Enables proper pagination UI
- Shows "X of Y results"
- Allows calculating total pages

## Implementation

### PyFilesystem2 Plugins
All PyFilesystem2-based plugins support pagination:
- Implemented in base class
- Consistent behavior across plugins

### Invenio Plugins
Invenio-based plugins (Zenodo, etc.) support pagination:
- Leverages Invenio API pagination
- Natural fit for repository browsing

### New TempFileSource Plugin

Testing utility for PyFilesystem2 plugins:
- Uses built-in OS Filesystem
- Simplifies testing
- Question: Could replace `posix` plugin? (unless specific posix functionality needed)

## Architectural Impact

### Plugin Interface Extensions

Three new serializable properties:
```python
supports_pagination: bool
supports_search: bool
supports_sorting: bool
```

### API Changes

List contents now returns:
```python
{
  "items": [...],
  "total_matches": 1234
}
```

### Client-Side Changes

UI updated to:
- Use server-side pagination when supported
- Disable client sorting when server sorting unsupported
- Display total matches
- Handle limit/offset parameters

## Trade-offs

### Challenges

**Server-Side Handling Complexity:**
- Sorting must be handled carefully
- Filtering requires plugin implementation
- Searching syntax varies by plugin

**Recursive View Limitation:**
- Pagination only works in flat (non-recursive) view
- Recursive browsing still loads all files

### Benefits

**Performance:**
- Fast navigation in large repositories
- Reduced memory usage
- Scalable to millions of files

**User Experience:**
- Responsive UI even with huge file sources
- Clear pagination controls
- Total count visible

## Bug Fixes

Fixed issue in PyFilesystem2 plugins:
- Problem when listing recursively
- Detected during TempFileSource testing

## Documentation Implications

### Key Concepts to Cover

1. **Pagination Model**: Server-side vs client-side pagination
2. **Plugin Capabilities**: How `supports_*` properties work
3. **Search Syntax**: Plugin-specific search query formats
4. **Performance Characteristics**: When pagination matters
5. **Recursive vs Flat Browsing**: Pagination limitations

### Configuration Examples

Plugins automatically expose pagination capabilities - no configuration needed. Documentation should cover:
- How to check if a plugin supports pagination
- Expected performance with/without pagination
- Search query syntax for different plugin types

### User Documentation

- Using pagination controls in file source browser
- Understanding total match counts
- Search functionality per file source type
- Performance expectations for large sources

### Developer Documentation

- Implementing pagination in custom plugins
- Server-side sorting considerations
- Search query syntax design
- Testing pagination with TempFileSource

## Visual Aids

Include screenshot from PR showing pagination UI:
- Pagination controls
- Total match display
- Search interface

## Testing

**Automated Tests:** Included for pagination functionality
**TempFileSource:** New testing plugin simplifies PyFilesystem2 plugin tests

## Technical Details

**Diff size:** 1475 lines
**Affected Plugins:** All PyFilesystem2-based and Invenio-based plugins
**Breaking Changes:** None - backward compatible API extension
