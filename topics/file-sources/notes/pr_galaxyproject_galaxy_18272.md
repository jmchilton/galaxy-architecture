# PR #18272: Allow OAuth 2.0 user defined file sources (w/Dropbox integration)

**Author:** John Chilton (@jmchilton)
**Merged:** October 15, 2024
**URL:** https://github.com/galaxyproject/galaxy/pull/18272
**Builds on:** PR #18222

## Overview

Adds **OAuth 2.0 authentication** to user-defined file sources framework, enabling seamless integration with cloud storage services that require OAuth (Dropbox, Google Drive, etc.). Includes complete Dropbox plugin with admin and user documentation.

## Key Features

### OAuth 2.0 Client Capabilities

Framework for OAuth-based file sources:
- OAuth 2.0 authorization flow integration
- Token storage in Vault
- Refresh token handling
- Scope management
- Status tracking for OAuth services

### Initial Dropbox Integration

Complete OAuth-enabled Dropbox plugin:
- Admin documentation for configuring Dropbox app
- User documentation for granting access
- Production-ready template
- Full OAuth flow implementation

### Future Extensibility

Architecture designed for additional OAuth providers:
- Google Drive (mentioned as next target)
- OneDrive
- Any OAuth 2.0 compatible service

## OAuth Flow

### 1. Admin Configuration

Admin creates Dropbox app and configures template:
```yaml
- type: dropbox
  id: dropbox_oauth
  name: Dropbox
  description: Connect your personal Dropbox account
  oauth:
    client_id: ${environ.get('DROPBOX_CLIENT_ID')}
    client_secret: ${environ.get('DROPBOX_CLIENT_SECRET')}
    authorization_url: https://www.dropbox.com/oauth2/authorize
    token_url: https://www.dropbox.com/oauth2/token
    scopes: ['files.content.read', 'files.metadata.read']
```

### 2. User Initiates Connection

User selects Dropbox template in UI, clicks "Authorize"

### 3. OAuth Authorization

- Galaxy redirects to Dropbox authorization page
- User grants permissions
- Dropbox redirects back to Galaxy with code
- Galaxy exchanges code for access token + refresh token

### 4. Token Storage

- Access token and refresh token stored in Vault
- Tokens associated with user's file source instance
- Vault provides secure, encrypted storage

### 5. File Source Usage

- File source uses stored access token for API calls
- Refresh token used to renew expired access tokens
- All token management transparent to user

## OAuth 2.0 Callback

### Callback URL Configuration

**Production:** Must use HTTPS
```
https://galaxy.example.org/oauth2_callback
```

**Development:** HTTP allowed for localhost
```
http://localhost:8081/oauth2_callback
```

Testing with `make client-dev-server` proxy works on localhost.

### Callback Handling

Galaxy receives authorization code:
1. Validates state parameter (CSRF protection)
2. Exchanges code for tokens
3. Stores tokens in Vault
4. Associates tokens with file source instance
5. Redirects user to instance management page

## Plugin Status Framework

### Enhanced Status Tracking

For OAuth services, status includes:
- **Connection Status**: Connected, needs authorization, token expired
- **Token Expiry**: When access token expires
- **Scope Status**: Which scopes granted
- **Refresh Status**: When last refreshed

### UI Display

Status shown in instance list:
- Visual indicators for connection health
- Warnings when tokens need renewal
- Links to re-authorize if needed

Screenshot from PR shows OAuth status:
```
[✓] Connected
Last refreshed: 2 hours ago
Expires: in 3 hours
```

### Future Direction

Framework prepared for:
- Automatic token refresh
- Notifications when re-auth needed
- Scope change detection

## Dropbox Admin Documentation

Complete guide for configuring Dropbox:

### 1. Create Dropbox App

Instructions for:
- Navigating Dropbox App Console
- Choosing app type and permissions
- Configuring OAuth redirect URI
- Obtaining client ID and secret

### 2. Configure Galaxy

Set environment variables:
```bash
export DROPBOX_CLIENT_ID="your_app_key"
export DROPBOX_CLIENT_SECRET="your_app_secret"
```

Add template to `file_source_templates.yml`:
```yaml
- include: ./lib/galaxy/files/templates/examples/dropbox_oauth.yml
```

### 3. Test Configuration

Verify OAuth flow works before announcing to users.

## User Documentation

### Granting Access

Step-by-step:
1. Navigate to User Preferences → Manage File Sources
2. Click "Create" and select Dropbox
3. Click "Authorize with Dropbox"
4. Log in to Dropbox (if needed)
5. Review permissions
6. Click "Allow"
7. Redirected back to Galaxy - connection complete

### Using Dropbox Files

Once connected:
- Browse Dropbox in upload dialog
- Select files for import
- Export workflows/histories to Dropbox (if writable)

### Revoking Access

Users can:
- Deactivate file source in Galaxy
- Revoke app access in Dropbox settings

## Implementation Details

### Token Management

**Access Tokens:**
- Short-lived (typically 4 hours)
- Used for API requests
- Automatically refreshed when expired

**Refresh Tokens:**
- Long-lived (no expiry for Dropbox)
- Used to obtain new access tokens
- Stored securely in Vault

### Scope Requesting

OAuth configuration supports scope requests:
```yaml
oauth:
  scopes: ['files.content.read', 'files.metadata.read', 'files.content.write']
```

Galaxy requests minimum necessary scopes.

### Security Considerations

**CSRF Protection:**
- State parameter in OAuth flow
- Validates callback matches initiated request

**Secure Storage:**
- All tokens in Vault
- Never exposed in logs or UI
- Encrypted at rest

**HTTPS Enforcement:**
- Production deployments require HTTPS callback
- Protects authorization codes in transit

## Integration with Object Stores

Architecture supports OAuth for object stores:
- Same OAuth framework
- Minor work needed to integrate
- Shared client/server abstractions
- Documentation applicable to both

## Documentation Screenshots

From PR description:

**1. Dropbox App Configuration Guide**
- Step-by-step app creation
- Permission setup
- Redirect URI configuration

**2. Template Configuration Example**
- YAML syntax
- Environment variable injection
- OAuth parameters

**3. User Authorization Flow**
- Before authorization
- During OAuth flow
- After successful connection

**4. Status Display**
- Connection indicators
- Token expiry warnings
- Refresh information

## Testing

**Automated Tests:** Included
**Manual Testing:** Instructions provided
- Creating Dropbox app
- Configuring template
- User authorization flow
- File browsing and import

## Use Cases

### 1. Personal Cloud Storage Access
Users connect personal Dropbox without admin managing individual credentials.

### 2. Collaborative Project Folders
Team members each authorize Galaxy to access shared Dropbox folder for project data.

### 3. Cross-Platform Workflows
Analyze data in Galaxy, export results to Dropbox, share with collaborators who don't use Galaxy.

## Documentation Implications

### Admin Documentation

1. **OAuth App Setup**: Creating apps in various services (Dropbox, Google, etc.)
2. **Security Configuration**: HTTPS requirements, callback URLs
3. **Environment Variables**: Managing client credentials securely
4. **Testing OAuth Flows**: Verifying configuration before user rollout

### User Documentation

1. **Authorizing Services**: Step-by-step OAuth grant flow
2. **Permission Understanding**: What Galaxy can/cannot access
3. **Revoking Access**: How to disconnect services
4. **Troubleshooting**: Common OAuth errors and solutions

### Developer Documentation

1. **Adding OAuth Plugins**: Creating new OAuth-enabled file sources
2. **Token Lifecycle**: Management of access/refresh tokens
3. **Scope Design**: Requesting minimum necessary permissions
4. **Status Framework**: Displaying connection health to users

## Future Work

**Mentioned in PR:**
- Google Drive integration (in progress when PR written)
- Additional scope-requesting clients
- Testing on second service to validate framework generality

## Technical Details

**Diff size:** 5,800 lines
**Dependencies:** Requires Vault for token storage
**OAuth Callback:** `/oauth2_callback` endpoint
**Supported Services:** Dropbox (initial), extensible to any OAuth 2.0 provider
