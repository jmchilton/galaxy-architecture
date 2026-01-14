# lib/galaxy/files/templates/models.py

## Galaxy File Sources Architecture: Pydantic Models Summary

### Template Catalog Structure
Galaxy's file sources use a **template-based configuration system** that decouples admin-defined templates from user configurations. The system maintains a `FileSourceTemplateCatalog` (list of `FileSourceTemplate` objects) enabling admins to define reusable, parameterized file source blueprints. Each template supports versioning and deprecation (via `version` and `hidden` fields) for backward compatibility with existing user configurations.

### Variable and Secret Definitions
Templates support two types of user-provided parameters:
- **Variables**: Typed parameters (string, integer, path_component, boolean) with labels, help text, and defaults. Used for configuration values users can safely customize.
- **Secrets**: Sensitive credentials stored in a vault, referenced by name but not exposed in API responses to non-admins. Both variables and secrets support Jinja2 template expansion.

### Template Configuration Models
The architecture defines 14 file source types (POSIX, S3, FTP, Azure, Onedata, WebDAV, Dropbox, Google Drive, eLabFTW, Inveniordm, Zenodo, RSpace, Dataverse, HuggingFace). Each type has two Pydantic models:
- **TemplateConfiguration**: Accepts `Union[str, TemplateExpansion]` for dynamic field values (variables/secrets)
- **FileSourceConfiguration**: Runtime instances with concrete string values after template expansion

OAuth2 sources (Dropbox, Google Drive) inherit from `OAuth2TemplateConfiguration`, encapsulating client credentials. Template expansion uses Jinja2 with custom filters for path validation (`ensure_path_component`) and boolean coercion.

### User-Defined File Sources
The `template_to_configuration()` function orchestrates transformation: it populates variable defaults, expands template expressions using variables/secrets/environment/user details, validates against implicit parameters, and instantiates the final `FileSourceConfiguration`. This design allows admins to define secure, parameterized file source templates once, enabling users to instantiate multiple configurations through simple variable binding.
