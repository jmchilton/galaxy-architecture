# lib/galaxy/managers/file_source_instances.py

## Summary: File Source Instances Manager

The `FileSourceInstancesManager` provides comprehensive CRUD operations and lifecycle management for user-defined file source instances in Galaxy.

**CRUD Operations:**
Instances are retrieved via UUID with ownership validation ensuring users access only their own sources. The manager supports create, list, show, and purge operations, storing instances in the `user_file_source` table with UUID as the primary identifier.

**Template Instantiation Workflow:**
When creating instances, the manager validates payloads against the file source template catalog, retrieves the target template, assigns UUIDs, and persists both template definition and variables. The workflow handles OAuth2 callbacks by pre-generating UUIDs during authorization to store refresh tokens before instance creation.

**Persistence & Retrieval:**
Instances are persisted via SQLAlchemy ORM with user context enforcement. The manager stores template snapshots (definition, ID, version) alongside user-provided variables and secrets. Secret values are stored in a separate Vault rather than inline, with recovery handled through the UserDefinedFileSourcesImpl resolver when instantiating file sources from URIs.

**Validation & Security:**
Multi-layered validation occurs during creation and modification: payload schema validation against templates, template variable/secret validation, and connection testing. Instance modifications support upgrading to newer templates with variable mapping. The manager tests configurations by constructing file sources and attempting root-level listing to verify connectivity and permissions before persistence.
