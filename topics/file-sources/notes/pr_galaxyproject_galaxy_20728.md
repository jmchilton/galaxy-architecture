# PR #20728: Refactor Files Sources Framework for stronger typing using Pydantic models

**Author:** David López (@davelopez)
**Merged:** August 19, 2025
**URL:** https://github.com/galaxyproject/galaxy/pull/20728
**Followup to:** PR #20698 review comments

## Overview

Major refactoring introducing **Pydantic-based configuration management** for File Sources framework. Implements two-tier architecture separating template configuration from resolved configuration, enabling dynamic user-specific customization with strong type safety.

## Two-Tier Configuration System

### Architecture

Similar to User-defined FileSources approach:

**1. Template Configuration** (`BaseFileSourceTemplateConfiguration`)
- Contains raw values with template variables
- Supports `${variable}` syntax for templating
- Pre-resolution state
- Example: `root: /data/${user.username}/files`

**2. Resolved Configuration** (`BaseFileSourceConfiguration`)
- Contains final evaluated values
- Used during actual operations
- Post-template-processing
- Example: `root: /data/john_doe/files`

### Benefits

- **Type Safety**: Pydantic validates both template and resolved configs
- **Template Flexibility**: Dynamic user/environment interpolation
- **Runtime Safety**: Errors caught during validation, not runtime
- **Documentation**: Auto-generated from Pydantic models

## Updated Base Classes

### Generic Typing

All file sources now:
```python
class MyFilesSource(BaseFilesSource[MyTemplateConfig, MyResolvedConfig]):
    plugin_type = "my_plugin"
    template_config_class = MyTemplateConfig
    resolved_config_class = MyResolvedConfig
```

### Automatic Template Resolution

Framework handles:
- Template variable expansion
- User context injection
- Environment variable substitution
- Validation at each stage

### Runtime Context

New `FilesSourceRuntimeContext` (replaces `user_context`):
```python
context: FilesSourceRuntimeContext[PosixConfiguration]
# Contains:
#  - resolved_config: validated resolved configuration
#  - user: user data (if operation run by user)
```

## Example: Posix File Source

### Template Configuration
```python
class PosixTemplateConfiguration(BaseFileSourceTemplateConfiguration):
    """Template with potential variables"""
    root: Union[str, TemplateExpansion, None] = None
    writable: Union[bool, TemplateExpansion] = Field(default=False)
    # ... other fields
```

### Resolved Configuration
```python
class PosixConfiguration(BaseFileSourceConfiguration):
    """Resolved with concrete values"""
    root: Optional[str] = None
    writable: bool = False
    # ... other fields (typed, no templates)
```

### File Source Implementation
```python
class PosixFilesSource(BaseFilesSource[PosixTemplateConfiguration, PosixConfiguration]):
    plugin_type = "posix"
    template_config_class = PosixTemplateConfiguration
    resolved_config_class = PosixConfiguration

    def _list(self, path: str, context: FilesSourceRuntimeContext[PosixConfiguration]):
        # context.resolved_config has typed, resolved values
        root = context.resolved_config.root
        # ... use resolved config for operations
```

## Template Variable Types

### TemplateExpansion

Union type supporting:
- `str` - Literal value
- Template expressions - `${user.username}`, `${environ.VAR}`
- Complex expressions - `${user.preferences['key']}`

### Validation

Pydantic ensures:
- Template syntax correctness
- Type compatibility after resolution
- Required fields present
- Custom validators enforced

## Plugin Loader Integration

### Configuration Flow

1. **Load YAML**: Read file_sources_conf.yml
2. **Parse Template**: Validate against `template_config_class`
3. **Resolve Templates**: Expand variables for user/environment
4. **Validate Resolved**: Validate against `resolved_config_class`
5. **Instantiate Plugin**: Pass resolved config to file source

### Error Handling

Errors caught at each stage:
- YAML parsing errors
- Template validation errors
- Resolution errors (missing variables)
- Resolved config validation errors

All before file source operations.

## File Sources Configuration Linter

**Bonus feature** from PR - validates file source configs.

### Usage

```bash
# Default validation
make files-sources-lint

# Verbose output
make files-sources-lint-verbose

# Specific file
python scripts/lint_file_sources_config.py -f path/to/file_sources_conf.yml

# Custom Galaxy config
python scripts/lint_file_sources_config.py -c path/to/galaxy.yml --verbose
```

### Features

- **Colorized Output**: Visual success/error feedback
- **Configuration Validation**: Instantiates each file source
- **Verbose Mode**: Shows detailed config being validated
- **Fail-Fast**: Stop on first error for debugging
- **Auto-Discovery**: Finds Galaxy and file sources configs automatically

### Example Output

```
Galaxy File Sources Configuration Validator
=============================================
Using Galaxy config: ../config/galaxy.yml
Using file sources config: ../config/file_sources_conf.yml

Found 4 file source(s) to validate

[1/4] Validating file source configuration...
  Validating file source 'test-posix-source' of type 'posix'...
    Using configuration:
        type: posix
        root: /home/dlopez/sandbox/file_source_data/
        id: test-posix-source
        label: TestSource
        writable: true
    ✓ Valid: File source 'test-posix-source' (posix) configured successfully

[2/4] Validating file source configuration...
  Validating file source 'test-s3-source' of type 's3fs'...
    Using configuration:
        type: s3fs
        bucket: ${user.preferences['test-s3-source|bucket']}
        key: ${user.user_vault.read_secret('preferences/test-s3-source/access_key')}
        ...
    ✓ Valid: File source 'test-s3-source' (s3fs) configured successfully

Validation Summary:
  Total file sources: 4
  Valid: 4
  Errors: 0

✓ All file sources validated successfully!
```

## Migration Impact

### Plugin Developers

Must update plugins to:
1. Define `TemplateConfiguration` class extending `BaseFileSourceTemplateConfiguration`
2. Define `ResolvedConfiguration` class extending `BaseFileSourceConfiguration`
3. Update class signature: `BaseFilesSource[TemplateConfig, ResolvedConfig]`
4. Set `template_config_class` and `resolved_config_class`
5. Update methods to accept `FilesSourceRuntimeContext[ResolvedConfig]`

### Configuration Files

No changes needed - existing YAML configs continue working.

### Testing

Existing tests continue working - framework handles migration internally.

## Documentation Implications

### Key Concepts to Cover

1. **Two-Tier Architecture**: Template vs resolved configuration
2. **Pydantic Models**: Type safety and validation
3. **Template Variables**: Syntax and available context
4. **Runtime Context**: How plugins access resolved config and user data
5. **Configuration Linter**: Validating configs before deployment

### Plugin Development Guide

- Defining template and resolved configuration classes
- Using TemplateExpansion for dynamic fields
- Accessing resolved config in plugin operations
- Testing plugins with linter

### Admin Guide

- Understanding template variable syntax
- Using linter to validate configs
- Debugging configuration errors
- Common validation issues

## Benefits for Galaxy

**Type Safety:**
- Catch config errors at startup, not runtime
- IDE autocomplete for configuration
- Clear error messages for users

**Flexibility:**
- Dynamic user-specific configuration
- Environment-based customization
- Template reuse across deployments

**Maintainability:**
- Self-documenting via Pydantic
- Easier to add new configuration options
- Validation logic centralized

**Developer Experience:**
- Linter for rapid feedback
- Clear plugin development patterns
- Reduced boilerplate

## Technical Details

**Diff size:** 6,248 lines (significant refactoring)
**Testing:** Refactoring of existing test coverage
**Breaking Changes:** Plugin interface updated (internal)
**Configuration Compatibility:** Existing YAML configs unchanged
