# PR #11769: Support role and group permissions in file sources plugins

**Author:** David López (@davelopez)
**Merged:** April 6, 2021
**URL:** https://github.com/galaxyproject/galaxy/pull/11769
**Related Issue:** #11768

## Overview

Adds **security controls** to File Sources by enabling role and group-based access restrictions. This allows administrators to limit which users can access specific file sources based on their Galaxy roles and group memberships.

## Key Changes

### New Security Configuration Options

File source plugins now support two new YAML configuration options:

```yaml
requires_roles: some_role
requires_groups: some_group
```

### Boolean Logic for Access Rules

Implements boolean expression parser for sophisticated access control:
- Supports AND/OR logic for combining multiple roles/groups
- Allows complex access requirements

## Architectural Impact

### Security Enforcement Layer

- Access checks performed before allowing file source operations
- Integrated into file sources security model
- Works with existing Galaxy role/group infrastructure

### API Consistency Fix

Fixed inconsistency between legacy and FastAPI `remote_files` API default responses (detected during testing)

## Use Cases

### 1. Restrict File Sources by Department
```yaml
- type: posix
  id: engineering-data
  label: Engineering Data
  root: /mnt/engineering
  requires_groups: engineering_team
```

### 2. Restrict File Sources by Permission Level
```yaml
- type: webdav
  id: sensitive-data
  label: Sensitive Research Data
  requires_roles: data_access_role
  requires_groups: approved_researchers
```

### 3. Public vs Private File Sources
- File sources without `requires_*` options remain accessible to all users
- File sources with restrictions only visible/usable by authorized users

## Documentation Implications

### Key Concepts to Cover

1. **Access Control Model**: How roles and groups restrict file source access
2. **Boolean Logic Syntax**: Combining multiple roles/groups in expressions
3. **Security Best Practices**: When and how to restrict file sources
4. **User Experience**: How restrictions affect file source visibility

### Configuration Examples to Highlight

- Simple single role/group restrictions
- Complex boolean expressions
- Combining with user preferences and templating
- Public vs restricted file sources

### Security Considerations

- File sources without restrictions are globally accessible
- Access checks happen before file operations
- Changes to user roles/groups dynamically affect access
- Integration with Galaxy's existing security model

## Technical Details

**Diff size:** 895 lines
**Testing:** Includes unit tests for boolean logic parser and integration tests using posix plugin
**API Impact:** Fixed remote_files API consistency between legacy and FastAPI implementations
