# Dependency Injection in Galaxy - Claude Context

You are an expert on dependency injection patterns in Galaxy, specifically type-based dependency injection using Lagom.

## Core Concepts

- Galaxy uses **type-based dependency injection** with the **Lagom** library
- The old `app` object was a **god object** that knew/did too much
- **Interfaces** (like `StructuredApp`) break circular dependencies
- Dependencies should form a **DAG (directed acyclic graph)**
- DI works uniformly across **FastAPI controllers**, **WSGI controllers**, and **Celery tasks**

## Key Files to Reference

- `lib/galaxy/di/` - Dependency injection container setup
- `lib/galaxy/structured_app.py` - `StructuredApp` interface definition
- `lib/galaxy/app.py` - `UniverseApplication` implementation
- `lib/galaxy/managers/` - Manager implementations using DI
- `lib/galaxy/webapps/galaxy/api/` - FastAPI controllers using DI
- `lib/galaxy/celery/tasks.py` - Celery tasks using DI

## Architecture Pattern

```
Lagom Container
    ├── Resolves dependencies by type
    ├── Manages singletons
    └── Constructs objects automatically

Components declare dependencies via type annotations:
    def __init__(self, manager: SomeManager, service: SomeService):
        ...

Container automatically resolves:
    instance = container[MyComponent]
```

## Common Patterns

### Manager Pattern
```python
class MyManager:
    def __init__(
        self,
        model: GalaxyModelMapping,
        hda_manager: HDAManager,
        history_manager: HistoryManager,
    ):
        self.model = model
        self.hda_manager = hda_manager
        self.history_manager = history_manager
```

### FastAPI Controller Pattern
```python
@cbv(router)
class FastAPITags:
    manager: TagsManager = depends(TagsManager)
    
    @router.put('/api/tags')
    def update(self, trans: ProvidesUserContext, payload: TagUpdatePayload):
        self.manager.update(trans, payload)
```

### Legacy WSGI Controller Pattern
```python
class TagsController(BaseGalaxyAPIController):
    manager: TagsManager = depends(TagsManager)
```

### Celery Task Pattern
```python
@celery_app.task
@galaxy_task
def my_task(hda_manager: HDAManager, dataset_id):
    hda = hda_manager.by_id(dataset_id)
    # ... use manager
```

## Key Libraries

- **Lagom**: Type-based dependency injection library
  - https://lagom-di.readthedocs.io/en/latest/
  - Automatically resolves dependencies based on type annotations
  - Supports singletons and factory functions

## When Updating This Topic

1. **Verify examples** against current Galaxy codebase
2. **Check** if Lagom usage patterns have changed
3. **Update** `related_code_paths` in metadata.yaml if new files are relevant
4. **Regenerate** all outputs: `/sync-slides dependency-injection`
5. **Run validation**: `/validate-topic dependency-injection`

## Related Topics

- **frameworks** - Background on Galaxy's framework choices
- **tasks** - How Celery tasks use DI
- **application-components** - What components use DI

## Key Points for Developers

### Do's

- ✅ Use **type annotations** for all dependencies
- ✅ Use **interface types** (like `StructuredApp`) to break circular dependencies
- ✅ Let the **container** construct objects: `container[MyClass]`
- ✅ Use `depends()` for controllers: `manager: Manager = depends(Manager)`
- ✅ Use `@galaxy_task` decorator for Celery tasks

### Don'ts

- ❌ Don't depend on the entire `app` object when you only need specific parts
- ❌ Don't create circular dependencies - use interfaces
- ❌ Don't manually construct dependencies - let the container do it
- ❌ Don't use `Depends()` from FastAPI - use Galaxy's `depends()`

## Common Questions

**Q: Why use Lagom instead of FastAPI's Depends?**
A: Lagom provides type-based inference, works uniformly across FastAPI and WSGI controllers, and is less verbose.

**Q: How do I add a new manager with DI?**
A: Add type annotations to `__init__`, register with container, and use `container[MyManager]` to get instances.

**Q: Can I still use `app`?**
A: Avoid when possible. Use specific managers/services via DI. Use `StructuredApp` interface if you need app-like object.

**Q: How do I test code using DI?**
A: Mock each dependency individually based on type annotations. Much easier than mocking entire `app` object.

**Q: What's the difference between `StructuredApp` and `UniverseApplication`?**
A: `StructuredApp` is an interface that breaks circular dependencies. `UniverseApplication` is the concrete implementation.

## Migration Notes

- Old code used `app` object directly
- New code uses type-based DI with Lagom
- Controllers can use `depends()` for uniform DI
- Tasks use `@galaxy_task` decorator for automatic DI
- Interfaces like `StructuredApp` prevent circular dependencies

## Benefits Summary

1. **Type Safety**: Type annotations enable mypy checking and IDE hints
2. **Testability**: Easy to mock individual dependencies
3. **Clarity**: Type signatures show exactly what's needed
4. **Uniformity**: Same pattern works everywhere (FastAPI, WSGI, tasks)
5. **Simplicity**: Container handles construction automatically
