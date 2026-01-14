# Code Path: lib/galaxy/managers/pages.py

## Role in Architecture

Core component of Galaxy's content creation and sharing system. Manages complete lifecycle of Pages - rich, interactive markup-based documents that embed Galaxy objects (datasets, workflows, histories, visualizations).

## Primary Responsibilities

**Lifecycle Management:** Creation, editing, versioning, searching, and sharing pages with robust permission infrastructure.

**Key Integration Points:**
- Inherits from `SharableModelManager` - permission/sharing infrastructure
- Uses `UsesAnnotations` mixin - user metadata/annotations
- Integrates with workflow manager for auto-generated pages from invocation reports
- Processes markdown and HTML with Galaxy-specific transformations

## Core Classes

### PageManager

Four main operational areas:

#### A. Creation & Revision Management
```python
create_page(trans, payload: CreatePagePayload) → Page
```
- Validates unique slug per user
- Creates initial PageRevision with content
- Two creation paths: direct content OR auto-generation from workflow invocation
- Applies content security/transformations on import

#### B. Content Editing
```python
update_page(trans, id: int, payload: UpdatePagePayload) → Page
save_new_revision(trans, page, payload) → PageRevision
```
- Updates page metadata (title, slug, annotation)
- Creates new revision on content save (version history)
- Validates slug uniqueness
- Performs security checks (ownership/accessibility)

#### C. Content Transformation
```python
rewrite_content_for_import(trans, content, content_format: str) → str
rewrite_content_for_export(trans, as_dict) → dict
```

**Import (Save) Path:**
- HTML: Sanitizes HTML, processes embedded objects, resolves placeholder references
- Markdown: Runs Galaxy markdown pre-processor

**Export (Edit/Display) Path:**
- HTML: Renders embedded objects to displayable content
- Markdown: Expands embedded references, provides editor-friendly and display versions

#### D. Discovery & Querying
```python
index_query(trans, payload: PageIndexQueryPayload, include_total_count: bool)
```

Complex filtering supporting:
- **Visibility modes:** Own pages, published, shared, deleted (admin-only)
- **Advanced search:** `title:`, `slug:`, `tag:`, `user:`, `is:` filters
- **Raw text search** across title, slug, tags, username
- Sorting and pagination support

**Security Pattern:** Admin-only access to sensitive filter combinations.

### PageContentProcessor

Specialized HTML parser for two rendering modes.

**Design:** Extends Python's `HTMLParser` to:
- Track nested tag depth
- Identify and replace embedded Galaxy objects
- Preserve HTML structure
- Handle malformed HTML edge cases

**Core Algorithm:**
```
FOR each HTML element:
  IF element has "embedded-item" class:
    EXTRACT object type & ID
    RENDER object placeholder/content
    IGNORE original element content
  ELSE:
    RECONSTRUCT element as-is
```

**Technical Details:**
- Handles void elements with self-closing syntax
- Fixes malformed tags
- Normalizes character/entity references
- Escapes bare ampersands
- Preserves HTML comments

### PageSerializer & PageDeserializer

Standard Galaxy serialization pair for Pages ↔ JSON conversion.

Inherits from `SharableModelSerializer/Deserializer` for tagging, sharing, and annotation support.

## Important Design Patterns

### 1. Revision-Based History
- Every content change creates new `PageRevision` record
- `page.latest_revision` points to current version
- Enables rollback, version comparison, audit trails
- Schema: `Page → [PageRevision]` (1-to-many)

### 2. Embedded Object Strategy
- Objects stored as placeholders (not serialized copies)
- Rendering deferred until display time
- Supports lifecycle changes (dataset deleted, workflow modified)

**Placeholder Format:**
```html
<div class="embedded-item dataset placeholder" id="HistoryDatasetAssociation-123">
  <p class="title">Embedded Galaxy Dataset - 'expression.csv'</p>
  <p class="content">[Do not edit this block...]</p>
</div>
```

### 3. Content Format Agnosticism
- Supports both HTML and Markdown as first-class formats
- Format stored per-revision
- Unified transformation pipeline regardless of format
- Enables future format additions

### 4. Security-First Approach
- All content sanitized on import (prevents XSS)
- Slug must be unique per user
- Security checks on all object access
- Sharable objects inherit permission model

### 5. Complex Query Builder
- Structured search parser with multiple filter types
- Exact filters (`tag:genomics`) and raw text matches
- Admin-only combinations prevented at API level
- Automatic distinct() for left outer joins

## Code Examples

### Creating Page from Workflow Invocation
```python
payload = CreatePagePayload(
    title="My Analysis Results",
    slug="analysis-2025-01",
    invocation_id="abc123"  # Triggers auto-report generation
)
page = page_manager.create_page(trans, payload)
```

### Updating Page with Embedded Dataset
```python
payload = UpdatePagePayload(
    title="Updated Analysis",
    content="""
    <h2>Results</h2>
    <div class="embedded-item dataset placeholder"
         id="HistoryDatasetAssociation-42">...</div>
    """,
    content_format="html"
)
page_manager.save_new_revision(trans, page, payload)
```

### Advanced Search
```python
payload = PageIndexQueryPayload(
    search="user:emma tag:genomics is:published",
    show_published=True
)
results, total = page_manager.index_query(trans, payload, include_total_count=True)
```

## Integration Points

1. **Workflow Integration** - Pages from invocation reports
2. **Markdown Processing** - Galaxy-specific markdown features
3. **Sharing System** - `PageUserShareAssociation` permissions
4. **Tagging System** - `PageTagAssociation`
5. **Annotations** - `PageAnnotationAssociation`

## Documentation Highlights

**For training:**
- Pages bridge Galaxy objects and narrative
- Revision history is foundational
- Multiple rendering contexts (display, edit, import)
- Complex permission model
- Content security is non-negotiable
