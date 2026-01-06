# lib/galaxy/files/plugins.py

## Galaxy File Sources Plugin Architecture Summary

**Plugin Discovery & Loading:**
The `FileSourcePluginLoader` class orchestrates plugin discovery using a two-step process. First, `plugins_dict()` introspects the `galaxy.files.sources` module via `import_submodules()`, collecting all subclasses marked with a `plugin_type` class variable. These are registered in a dictionary keyed by plugin type identifier. Second, `load_plugins()` instantiates configured plugins from either YAML/XML config files or Python dictionaries, with special support for template-aware plugins via `build_template_config()`.

**ConfiguredFileSources Catalog:**
The `ConfiguredFileSources` class acts as the central catalog manager, maintaining a list of loaded `BaseFilesSource` instances. It supports flexible initialization via file paths or config dicts, stock plugin auto-loading, and URI-to-plugin resolution. The catalog validates URI roots against configured constraints (FTP directories, library import paths, etc.) and scores plugins via `score_url_match()` to find the best handler for arbitrary URIs.

**Template System:**
Configuration supports templating through `FileSourcePluginsConfig` and `FilesSourceTemplateContext`, enabling dynamic value resolution using environment variables, user context (email, username, roles, groups), and system settings. Template expansion occurs during plugin instantiation, using pattern `${ }` syntax within configuration values.

**Plugin Interface:**
Each plugin subclasses `BaseFilesSource` and declares a unique `plugin_type` string. Plugins optionally define `template_config_class` and `resolved_config_class` for template-aware configurations, inheriting from `BaseFileSourceTemplateConfiguration` and `BaseFileSourceConfiguration` respectively. The framework automatically handles template resolution before plugin initialization.
