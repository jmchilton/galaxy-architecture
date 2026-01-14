# PR #10152: Infrastructure for writing to pluggable Galaxy file sources (Writable File Sources)

**Author:** John Chilton (@jmchilton)
**Merged:** September 17, 2020
**URL:** https://github.com/galaxyproject/galaxy/pull/10152
**Foundation:** Built on PR #9888 (initial plugin implementation in 20.09)

## Overview

Extends the File Sources architecture to support **write operations**, enabling Galaxy to export data to remote file sources (Dropbox, WebDAV, etc.) in addition to importing from them.

## Key Changes

### Write Operation Support

- Adds write capabilities to FilesSource plugin interface
- Enables data export to remote destinations
- Complements the read-only indexing/realize operations from PR #9888

## Architectural Impact

### Plugin Interface Extensions

File sources can now be marked as **writable**, supporting:
- Exporting datasets to remote locations
- Writing collection archives
- History exports to external storage

### Use Cases Enabled

1. **Data Export Tools**: Generalization of existing "cloud send" tools
2. **Collection Archives**: Export collection data to remote file sources
3. **History Export**: Write entire histories to external storage
4. **Tool Form Integration**: Future support for "export_directory" input type

## Design Considerations

### Enhanced UX for Data Export

This infrastructure improves the user experience for getting large datasets out of Galaxy by:
- Providing consistent interface across multiple storage backends
- Leveraging the same plugin system as uploads
- Enabling direct export without intermediate downloads

## Documentation Implications

### Key Concepts to Cover

1. **Writable vs Read-only File Sources**: Configuration and behavior differences
2. **Export Workflows**: How write operations integrate with Galaxy tools
3. **Plugin Configuration**: Marking plugins as writable
4. **Security Considerations**: Permission checks for write access

### Code Examples to Highlight

- Configuring a writable file source
- Implementing write operations in custom plugins
- Export tool examples using writable file sources

### Future Tool Form Feature

The PR mentions future direction for a new tool form input type `export_directory` that would:
- Allow tools to specify export destinations
- Integrate with file sources for flexible output locations
- Generalize existing data export patterns

## Technical Details

**Diff size:** 833 lines
**Dependencies:** Requires PR #9888 foundation
