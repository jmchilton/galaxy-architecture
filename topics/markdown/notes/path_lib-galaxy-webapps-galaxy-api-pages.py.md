# Code Path: lib/galaxy/webapps/galaxy/api/pages.py

## Role in Architecture

FastAPI-based API layer for Galaxy Pages. Enables users to create, manage, and share rich markdown/HTML documents that embed Galaxy objects (datasets, workflows).

## API Endpoints

### Index & CRUD Operations
- **GET `/api/pages`** - List pages with filtering, sorting, pagination
- **POST `/api/pages`** - Create new page
- **GET `/api/pages/{id}`** - Retrieve page summary + latest revision
- **PUT `/api/pages/{id}`** - Update page metadata
- **DELETE `/api/pages/{id}`** - Soft-delete page
- **PUT `/api/pages/{id}/undelete`** - Restore deleted page

### Sharing & Access Control
- **GET `/api/pages/{id}/sharing`** - Get sharing status
- **PUT `/api/pages/{id}/publish`** - Make public
- **PUT `/api/pages/{id}/unpublish`** - Remove from published
- **PUT `/api/pages/{id}/enable_link_access`** - Enable public URL
- **PUT `/api/pages/{id}/disable_link_access`** - Disable public URL
- **PUT `/api/pages/{id}/share_with_users`** - Share with specific users
- **PUT `/api/pages/{id}/slug`** - Set unique URL slug

### PDF Export
- **GET `/api/pages/{id}.pdf`** - Stream PDF of latest revision
- **POST `/api/pages/{id}/prepare_download`** - Async PDF generation

## Request/Response Models

### CreatePagePayload
- `title` (str, required) - Page name
- `slug` (str, required) - URL identifier, pattern: `^[a-z0-9-]+$`
- `content_format` (enum: "html" | "markdown")
- `content` (str, optional) - Page body
- `annotation` (str, optional) - Documentation
- `invocation_id` (str, optional) - Auto-populate from workflow report

### PageDetails (Response)
- All summary fields: `id`, `title`, `slug`, `username`, etc.
- `content` (str) - Full page body
- `content_format` (enum)
- `content_editor` (str) - For markdown: original Galaxy markdown for editing
- `annotation` (str)
- Metadata: `generate_version`, `generate_time`

## Markdown Content Handling

### HTML Format
- Processed via `PageContentProcessor` (HTMLParser subclass)
- Sanitized before storage (XSS prevention)
- Embedded objects converted to placeholder tokens
- On export: placeholders re-expanded with current state

### Markdown Format (Primary)
- Uses Galaxy's internal markdown dialect
- Import: `ready_galaxy_markdown_for_import()` converts external → internal
- Export: `ready_galaxy_markdown_for_export()` expands embeds, returns:
  - `content_embed_expanded` - Full rendered HTML
  - `content_editor` - Original markdown for editing
- PDF export: Converts to basic markdown, then PDF via Celery

## Content Processing Pipeline

**On Create/Update:**
```
Raw Payload
    ↓
rewrite_content_for_import(trans, content, content_format)
    ├─ HTML: sanitize_html() → PageContentProcessor
    └─ Markdown: ready_galaxy_markdown_for_import()
    ↓
Store in PageRevision.content
```

**On Retrieval:**
```
Database (PageRevision.content)
    ↓
rewrite_content_for_export(trans, as_dict)
    ├─ HTML: PageContentProcessor (re-expand placeholders)
    └─ Markdown: ready_galaxy_markdown_for_export()
    ↓
Response (PageDetails)
```

**PDF Export:**
```
internal_galaxy_markdown
    ↓
to_basic_markdown() → Celery task
    ↓
internal_galaxy_markdown_to_pdf()
```

## Service Architecture

**FastAPIPages (API Controller)**
- FastAPI class-based view
- Depends on `PagesService` (injected)
- Maps HTTP requests to service methods
- Handles response serialization

**PagesService (Business Logic)**
- Orchestrates manager + serializer
- Methods: `index()`, `create()`, `show()`, `show_pdf()`, `update()`, `delete()`
- Delegates to PageManager for data access
- Handles markdown transformations
- Integrates ShareableService for sharing
- Manages async PDF tasks via Celery

**PageManager (Persistence)**
- Extends `SharableModelManager`
- Core methods: `index_query()`, `create_page()`, `update_page()`, `save_new_revision()`
- Content transformation: `rewrite_content_for_import/export()`
- Uses associations: `PageTagAssociation`, `PageUserShareAssociation`

## Query/Search Features

**Parameters:**
- `limit` (1-999, default 100)
- `offset` (default 0)
- `sort_by` (enum: "update_time" default)
- `deleted`, `show_own`, `show_published`, `show_shared`
- `search` - Free-text/filter query

**Search Syntax:**
- `title:` - Page title
- `slug:` (or `s:`) - Page slug
- `tag:` (or `t:`) - Tags
- `user:` (or `u:`) - Owner username
- `is:deleted`, `is:published`, `is:shared_with_me` - Status filters

## Design Patterns

### Dual Content Format Support
HTML for legacy; Markdown as primary. Separate transformations per format.

### Content Embedding Architecture
Objects stored as placeholders internally. Rendered on-demand on export.

### Revision History
Every page has `latest_revision` + `revision_ids`. Update doesn't create revision; `save_new_revision()` does.

### Soft Deletion
Pages marked `deleted=true`, not hard-deleted. Preserves history.

### Async PDF Export
Synchronous streaming for small pages. Async Celery tasks for large/complex pages with polling.

### Type Safety
Pydantic v2 models define all contracts. `DecodedDatabaseIdField` for URL IDs.

## Documentation Highlights

**For training:**
- Dual content format (HTML/Markdown)
- Embedded object strategy (placeholders)
- Revision-based history
- Soft deletion pattern
- ShareableService integration
- Async PDF generation with Celery
