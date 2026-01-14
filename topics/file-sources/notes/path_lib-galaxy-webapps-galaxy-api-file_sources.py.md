# lib/galaxy/webapps/galaxy/api/file_sources.py

## File Sources API Summary

The File Sources API provides endpoints for managing file source templates and user-defined file source instances in Galaxy.

### Template Browsing Endpoints

- **GET `/api/file_source_templates`** - Lists available file source templates with summaries
- **GET `/api/file_source_templates/{template_id}/{template_version}/oauth2`** - Retrieves OAuth2 authorization URL for template-based authentication

### User Instance CRUD Endpoints

- **POST `/api/file_source_instances`** - Create new user-bound file source instance
- **GET `/api/file_source_instances`** - List all user's file source instances
- **GET `/api/file_source_instances/{uuid}`** - Retrieve specific instance
- **PUT `/api/file_source_instances/{uuid}`** - Update/upgrade existing instance
- **DELETE `/api/file_source_instances/{uuid}`** - Purge instance (returns 204 No Content)

### Testing Endpoints

- **POST `/api/file_source_instances/test`** - Validate configuration before creating instance
- **GET `/api/file_source_instances/{uuid}/test`** - Test existing instance connectivity
- **POST `/api/file_source_instances/{uuid}/test`** - Validate update payload before applying

### Auth & Patterns

**Authentication:** All endpoints require `ProvidesUserContext` or `SessionRequestContext` dependency injection.

**Request/Response:** Uses Pydantic models (`CreateInstancePayload`, `ModifyInstancePayload`, `UserFileSourceModel`) for typed validation. Responses include `PluginStatus` for test operations and `OAuth2Info` for OAuth flows.

**Instance Identification:** Uses UUID4 path parameters for instance operations, ensuring user-bound isolation and secure access.
