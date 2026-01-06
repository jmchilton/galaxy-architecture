# lib/galaxy/files/__init__.py

## Galaxy File Sources Architecture Summary

**Core Abstractions:**

The Galaxy File Sources system defines a plugin-based architecture for handling remote file access through URIs. The main entry point is `ConfiguredFileSources` (lines 123-303), which manages a collection of `BaseFilesSource` plugins and routes URIs to the appropriate handler.

**Key Components:**

1. **ConfiguredFileSources** - Central orchestrator that:
   - Loads file source plugins from configuration files or dictionaries
   - Routes URIs to the best matching file source using scoring algorithm (`score_url_match()`)
   - Validates URIs against Galaxy configuration and user permissions
   - Serializes available file sources for API responses

2. **Plugin Architecture**:
   - `FileSourcePluginLoader` - Dynamically discovers and instantiates file source plugins by type
   - `BaseFilesSource` - Abstract base class for all file source implementations (from `galaxy.files.sources`)
   - `PluginKind` enum - Categorizes plugins (rfs, drs, rdm, stock)

3. **Configuration System**:
   - `ConfiguredFileSourcesConf` - Wraps configuration (file path or inline dict)
   - `FileSourcePluginsConfig` - Global file sources config (FTP dirs, import dirs, etc.)
   - Stock plugins auto-loaded: http, base64, drs, remoteZip, and conditionally gxftp, gximport, gxuserimport

4. **User Context & Access Control**:
   - `FileSourcesUserContext` (Protocol) - Defines user properties (email, roles, groups, vaults)
   - `ProvidesFileSourcesUserContext` - Adapts Galaxy's trans object to file sources context
   - `DictFileSourcesUserContext` - Alternative dict-based implementation for testing/serialization
   - User vault and app vault support for credential injection

5. **URI Resolution**:
   - `get_file_source_path()` - Parses URI to FileSourcePath (file_source + relative path)
   - `find_best_match()` - Scores all plugins and user-defined sources, returns highest scorer
   - `validate_uri_root()` - Enforces config/auth constraints (e.g., FTP dir existence, user login requirements)

6. **Extensibility**:
   - `UserDefinedFileSources` (Protocol) - Allows injecting custom file sources at runtime
   - `NullUserDefinedFileSources` - Default no-op implementation

**Design Pattern**: Composition over inheritance - `ConfiguredFileSources` manages a list of independent file source plugins rather than subclassing, enabling flexible plugin composition.
