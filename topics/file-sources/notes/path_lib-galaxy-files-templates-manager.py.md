# lib/galaxy/files/templates/manager.py

## Galaxy File Sources Template Manager Summary

**Template Catalog Loading**
Templates are loaded via two paths: directly from app config or from a YAML file specified in `file_source_templates_config_file`. The `from_app_config` method uses `raw_config_to_catalog` to convert raw configuration to a validated `FileSourceTemplateCatalog` using Pydantic models. The catalog undergoes syntactic sugar processing (`apply_syntactic_sugar`) that expands inline includes, converts shorthand dict notation for variables/secrets into lists, and recursively loads referenced YAML files.

**Template Expansion & Variable Substitution**
Templates use Jinja2 templating (default delimiters `{{` `}}`) with configurable start/end markers. The `expand_raw_config` function injects four contexts into templates: `variables`, `secrets`, `user` (user details), and `environment`. String values containing template delimiters are rendered through Jinja2's NativeEnvironment, which preserves Python types. Custom filters include `ensure_path_component` (prevents directory traversal) and `asbool` for type coercion. Template metadata (`template_start`, `template_end`) is stripped after expansion.

**User Instance Creation Workflow**
Instance creation follows strict validation: `template_to_configuration` applies variable defaults, expands template expressions with user-provided values, merges implicit OAuth2 parameters when applicable, and finally instantiates the appropriate `FileSourceConfiguration` class via `to_configuration_object`. The configuration object enforces type correctness and structural requirements.

**Secret & Credential Handling**
Secrets are validated separately from variables—all required secrets must be defined and must be strings. OAuth2 secrets (client_id, client_secret, scope) are handled specially, being replaced with tokens during implicit parameter merging. Vault integration is enforced: if any template declares secrets, Galaxy vault must be configured, raising an exception otherwise. Validation occurs at template lookup and instance creation stages.
