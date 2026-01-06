# PR #15497: Unify URL handling with filesources

**Author:** Nuwan Goonasekera (@nuwang)
**Merged:** February 22, 2023
**URL:** https://github.com/galaxyproject/galaxy/pull/15497
**Closes Issue:** #14658

## Overview

Major architectural convergence that **unifies URL handling with the File Sources framework**. URLs (http, ftp, s3, drs, base64) are now routed through file sources, enabling consistent authentication, credential injection, and access control for all remote data access.

## Key Features

### 1. URLs as File Sources

All URL protocols now handled through file source plugins:
- **Preconfigured**: http(s), base64, ftp, drs
- **Admin-configurable**: s3 and custom URL handlers
- **Transparent**: No client changes required

### 2. Injectable User Context for URLs

Admins can inject credentials for protected URLs using file source configuration:

**DRS Server with Basic Auth:**
```yaml
- type: drs
  id: mydrsserver
  doc: Test drs repository filesource
  http_headers:
    Authorization: |-
      #import base64
      Basic ${base64.b64encode(str.encode(user.preferences['mydrsserver|username'] + ":" + user.preferences['mydrsserver|password'])).decode()}
```

### 3. URL Pattern Matching

File sources can specify `url_regex` for fine-grained URL routing:

**Site-specific HTTP Handler:**
```yaml
- type: http
  id: test1
  doc: A specific http url handler
  url_regex: "^https?://www.usegalaxy.org/"
  http_headers:
    Authorization: "Bearer ${user.preferences['oidc|bearer_token']}"
```

This enables:
- Different credentials for different sites
- Site-specific authentication methods
- Passwordless access to protected resources

### 4. DRS Access Method Routing

DRS access methods now routed to appropriate file sources:
- HTTP access methods → HTTP file source
- S3 access methods → S3 file source
- Enables chained DRS resolution

### 5. Future OIDC Integration

Lays groundwork for injecting OIDC single-sign-on tokens (building on PR #15300)

## Architectural Changes

### New FileSource Interface Methods

**score_url_match(url)**
- Returns numeric score indicating plugin's ability to handle a URL
- Higher scores = better match
- Enables URL routing to most appropriate file source

**get_browsable()**
- Indicates if file source supports browsing (implements `SupportsBrowsing` interface)

**to_relative_path(gxfile_url)**
- Converts `gxfiles://` URL to relative path

### Removed Interface Methods

**get_scheme()** - No longer essential in unified model (remains in `BaseFileSource` for compatibility)

### Plugin Removals

**s3.py file source removed** - Replaced by s3fs.py which has:
- Better maintained dependencies (s3.py last updated 2019)
- Better configuration documentation
- Same functionality

## Backward Compatibility

### No Client Changes Required
URL-based data access continues to work transparently

### BaseFileSource Compatibility
Most plugins inheriting from `BaseFileSource` require no changes

### Interface Updates
Plugins directly implementing `FileSource` interface must implement new methods:
- `score_url_match()`
- `get_browsable()`
- `to_relative_path()`

### Kwargs Parameter
Additional `**kwargs` parameter added to some method signatures for:
- Future expansion
- Supporting chained DRS resolution

## Documentation Implications

### Key Architectural Concepts

1. **URL Routing**: How URLs are matched to file sources via `score_url_match()`
2. **Credential Injection**: Using templating for authentication headers
3. **Pattern-based Routing**: Using `url_regex` for site-specific handlers
4. **DRS Integration**: Access method routing and chained resolution
5. **Unified Model**: Single abstraction for browsable sources and URL protocols

### Configuration Patterns to Cover

**Protected HTTP Resources:**
```yaml
- type: http
  id: protected-api
  url_regex: "^https://api.example.org/"
  http_headers:
    Authorization: "Bearer ${user.preferences['api_token']}"
```

**DRS with Credentials:**
```yaml
- type: drs
  id: protected-drs
  http_headers:
    Authorization: "Basic ${base64.b64encode(...)}"
```

**S3 with Custom Credentials:**
```yaml
- type: s3fs
  id: private-bucket
  # ... s3 configuration
```

### Visual Aids

- URL routing decision tree (url_regex matching, score_url_match)
- Before/after architecture diagrams showing convergence
- DRS access method routing flow
- Authentication credential flow (user preferences → templating → headers)

### Migration Guide

- s3.py → s3fs.py migration for admins
- Updating custom plugins to implement new interface methods
- Configuring URL handlers for existing deployments

## Use Cases Enabled

1. **Passwordless Access**: Site-specific credentials injected automatically
2. **Protected DRS Servers**: Admin-configured credentials for institutional repositories
3. **OIDC Integration**: Bearer token injection for federated access
4. **Flexible S3 Access**: Multiple S3 file sources with different credentials
5. **Chained DRS Resolution**: Follow DRS references across multiple servers

## Technical Details

**Diff size:** 2626 lines
**Breaking Changes:** Minimal - primarily affects custom FileSource implementations
**Testing:** Includes automated tests and refactoring of existing test coverage
