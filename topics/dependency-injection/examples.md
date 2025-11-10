# Dependency Injection Examples

## Old Pattern: Direct `app` Dependency

### Before Type-based DI

```python
class DatasetCollectionManager:

     def __init__(self, app):
        self.type_registry = DATASET_COLLECTION_TYPES_REGISTRY
        self.collection_type_descriptions = COLLECTION_TYPE_DESCRIPTION_FACTORY
        self.model = app.model
        self.security = app.security

        self.hda_manager = hdas.HDAManager(app)
        self.history_manager = histories.HistoryManager(app)
        self.tag_handler = tags.GalaxyTagHandler(app.model.context)
        self.ldda_manager = lddas.LDDAManager(app)
```

**Problems:**
- Depends on entire `app` object
- Creates circular dependencies
- Hard to test
- Manager must know how to construct dependencies

---

## New Pattern: Type-based Dependency Injection

### After Type-based DI

```python
class DatasetCollectionManager:
    def __init__(
        self,
        model: GalaxyModelMapping,
        security: IdEncodingHelper,
        hda_manager: HDAManager,
        history_manager: HistoryManager,
        tag_handler: GalaxyTagHandler,
        ldda_manager: LDDAManager,
    ):
        self.type_registry = DATASET_COLLECTION_TYPES_REGISTRY
        self.collection_type_descriptions = COLLECTION_TYPE_DESCRIPTION_FACTORY
        self.model = model
        self.security = security

        self.hda_manager = hda_manager
        self.history_manager = history_manager
        self.tag_handler = tag_handler
        self.ldda_manager = ldda_manager
```

**Benefits:**
- No dependency on `app`
- Clear type signature shows all dependencies
- Easy to test with mocks
- Container handles construction

---

## Using Interfaces to Break Circular Dependencies

### With Interface (StructuredApp)

```python
class DatasetCollectionManager:

     def __init__(self, app: StructuredApp):
        self.type_registry = DATASET_COLLECTION_TYPES_REGISTRY
        self.collection_type_descriptions = COLLECTION_TYPE_DESCRIPTION_FACTORY
        self.model = app.model
        self.security = app.security

        self.hda_manager = hdas.HDAManager(app)
        self.history_manager = histories.HistoryManager(app)
        self.tag_handler = tags.GalaxyTagHandler(app.model.context)
        self.ldda_manager = lddas.LDDAManager(app)
```

Using `StructuredApp` interface instead of `UniverseApplication` breaks the circular dependency and makes dependencies closer to a DAG.

---

## DI Container Usage

### Simple Construction

**Before:**
```python
dcm = DatasetCollectionManager(
    self.model,
    self.security,
    HDAManager(self),
    HistoryManager(self),
    GalaxyTagHandler(self.model.context),
    LDDAManager(self)
)
```

**After:**
```python
dcm = container[DatasetCollectionManager]
```

The container automatically resolves all dependencies based on type annotations.

---

## DI in FastAPI Controllers

### Old FastAPI Pattern

```python
def get_tags_manager() -> TagsManager:
    return TagsManager()


@cbv(router)
class FastAPITags:
    manager: TagsManager = Depends(get_tags_manager)
    ...
```

Dependency injection allows for type checking but doesn't use type inference (requires factory functions, etc.)

---

## DI in FastAPI Controllers - Unified Approach

### New Unified Pattern

```python
@cbv(router)
class FastAPITags:
    manager: TagsManager = depends(TagsManager)

    @router.put(
        '/api/tags',
        ...
    )
    def update(
        self,
        trans: ProvidesUserContext,
        payload: TagUpdatePayload,
    ):
        self.manager.update(trans, payload)
```

Building dependency injection into our application and not relying on FastAPI allows for dependency injection that is:
- **Less verbose**
- Available uniformly across the application
- **Works for the legacy controllers identically**

---

## DI in Legacy WSGI Controllers

### Old Pattern

```python
class TagsController(BaseAPIController):

    def __init__(self, app):
        super().__init__(app)
        self.manager = TagsManager()
```

### New Pattern

```python
class TagsController(BaseGalaxyAPIController):
    manager: TagsManager = depends(TagsManager)
```

Same pattern works for both FastAPI and legacy WSGI controllers!

---

## DI in Celery Tasks

### Framework Setup

From `lib/galaxy/celery/tasks.py`:

```python
from lagom import magic_bind_to_container
...

def galaxy_task(func):
    CELERY_TASKS.append(func.__name__)
    app = get_galaxy_app()
    if app:
        return magic_bind_to_container(app)(func)
    return func
```

`magic_bind_to_container` binds function parameters to a specified Lagom DI container automatically.

---

## DI in Celery Tasks - Examples

### Simple Task

```python
@celery_app.task(ignore_result=True)
@galaxy_task
def purge_hda(hda_manager: HDAManager, hda_id):
    hda = hda_manager.by_id(hda_id)
    hda_manager._purge(hda)
```

### Task with Multiple Dependencies

```python
@celery_app.task
@galaxy_task
def set_metadata(
    hda_manager: HDAManager,
    ldda_manager: LDDAManager,
    dataset_id,
    model_class='HistoryDatasetAssociation'
):
    if model_class == 'HistoryDatasetAssociation':
        dataset = hda_manager.by_id(dataset_id)
    elif model_class == 'LibraryDatasetDatasetAssociation':
        dataset = ldda_manager.by_id(dataset_id)
    dataset.datatype.set_meta(dataset)
```

Dependencies are automatically injected based on type annotations!

---

![Decomposed App](../../images/app_decomposed.plantuml.svg)

---

## Key Takeaways

1. **Type annotations** enable automatic dependency resolution
2. **Interfaces** (like `StructuredApp`) break circular dependencies
3. **Container-based construction** simplifies object creation
4. **Uniform pattern** works across FastAPI, WSGI controllers, and Celery tasks
5. **Dependencies form a DAG** - no circular dependencies
