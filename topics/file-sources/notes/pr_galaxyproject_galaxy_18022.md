# PR #18022: Add Zenodo integration

**Author:** David López (@davelopez)
**Merged:** April 22, 2024
**URL:** https://github.com/galaxyproject/galaxy/pull/18022
**Requires:** PR #18028

## Overview

Adds dedicated **Zenodo file source plugin** based on Invenio framework, enabling direct export of Galaxy histories to Zenodo for DOI assignment and long-term archival. Introduces custom URI schemes (`zenodo://`, `invenio://`) for improved clarity.

## Key Features

### Zenodo File Source Plugin

Based on Invenio platform (Zenodo's underlying infrastructure):
- Upload Galaxy histories directly to Zenodo
- Automatically creates DOI for deposited records
- Supports both production Zenodo and sandbox instances
- Writable file source for data export

### Custom URI Schemes

Introduces protocol-specific schemes:
- `zenodo://` - Zenodo repositories
- `invenio://` - Generic Invenio-based repositories
- Legacy `gxfiles://` scheme still supported for backward compatibility

### Integration with User Vault

Token management using Galaxy's Vault system:
```yaml
token: ${user.user_vault.read_secret('preferences/zenodo/token')}
```

Alternative using user preferences:
```yaml
token: ${user.preferences['zenodo|token']}
```

## Configuration

### file_sources_conf.yml

```yaml
- type: zenodo
  id: zenodo
  doc: >
    Zenodo is a general-purpose open-access repository developed under
    the European OpenAIRE program and operated by CERN. It allows
    researchers to deposit data sets, research software, reports, and
    any other research-related digital artifacts. For each submission,
    a persistent digital object identifier (DOI) is minted, which makes
    the stored items easily citeable.
  label: Zenodo
  url: https://sandbox.zenodo.org  # Production: https://zenodo.org
  token: ${user.user_vault.read_secret('preferences/zenodo/token')}
  public_name: ${user.preferences['zenodo|public_name']}
  writable: true
```

### user_preferences_extra_conf.yml

```yaml
zenodo:
  description: Your Zenodo Integration Settings
  inputs:
    - name: token
      label: >
        Personal Access Token used to create draft records and to upload
        files. You can manage your tokens at
        https://zenodo.org/account/settings/applications/
      type: secret
      store: vault  # Requires vault_config_file in galaxy.yml
      required: False
    - name: public_name
      label: >
        Creator name to associate with new records (formatted as
        "Last name, First name"). If left blank "Anonymous Galaxy User"
        will be used. You can always change this by editing your record
        directly.
      type: text
      required: False
```

### galaxy.yml Requirements

```yaml
enable_celery_tasks: true
vault_config_file: vault_conf.yml  # If using Vault for token storage
```

## Workflow

1. **User Configuration**:
   - User creates Zenodo Personal Access Token
   - Stores token in Galaxy Vault or preferences
   - Optionally configures public name for attribution

2. **History Export**:
   - User selects "Export History" in Galaxy UI
   - Chooses Zenodo as destination
   - Galaxy creates draft Zenodo record
   - Uploads history files to Zenodo
   - User finalizes record to receive DOI

3. **DOI Assignment**:
   - Zenodo assigns persistent DOI
   - Record becomes citable and discoverable
   - Long-term preservation guaranteed by CERN

## Use Cases

### 1. Publishing Research Data
Researchers export Galaxy histories containing analysis results directly to Zenodo for publication alongside papers.

### 2. Long-term Archival
Institutions use Zenodo integration to preserve computational workflows and datasets beyond Galaxy server lifecycle.

### 3. Reproducibility
Published Zenodo records with DOIs enable exact citation and retrieval of computational analyses.

## Documentation Implications

### Key Concepts to Cover

1. **Zenodo Overview**: What Zenodo is, why use it for Galaxy data
2. **DOI Benefits**: Persistent identifiers, citability, discoverability
3. **Token Management**: Creating tokens, Vault vs preferences storage
4. **Export Workflow**: Step-by-step guide for exporting histories
5. **Invenio Architecture**: How Zenodo plugin relates to generic Invenio support

### Configuration Guide

- Setting up Zenodo file source
- User preferences configuration
- Vault setup for secure token storage
- Sandbox vs production instances

### User Documentation

- Creating Zenodo Personal Access Tokens
- Configuring Galaxy preferences
- Exporting histories to Zenodo
- Finalizing draft records
- Citing published Zenodo records

### Security Considerations

- Token storage best practices (Vault preferred)
- Token permissions and scoping
- Public name privacy considerations

## Related Work

**Invenio Platform**: Generic open-access repository framework
- Zenodo is an Invenio instance operated by CERN
- Plugin supports any Invenio-based repository
- Custom `invenio://` scheme for generic instances

## Technical Details

**Diff size:** 812 lines
**Dependencies:** Requires Celery tasks enabled
**Testing:** Manual testing instructions provided (no automated tests initially)
**Backward Compatibility:** Legacy `gxfiles://` scheme still supported
