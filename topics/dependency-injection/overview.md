# Dependency Injection in Galaxy

## The Problem: `app` as a God Object

### What is a God Object?

> "a God object is an object that knows too much or does too much. The God object is an example of an anti-pattern and a code smell."

https://en.wikipedia.org/wiki/God_object

Not only does `app` know and do too much, it is also used way too many places. Every interesting component, every controller, the web transaction, etc. has a reference to `app`.

---

## A Typical Usage Pattern

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

---

## Problematic Dependency Graph

When managers depend directly on `UniverseApplication`:

```python
class DatasetCollectionManager:

     def __init__(self, app: UniverseApplication):
        self.type_registry = DATASET_COLLECTION_TYPES_REGISTRY
        self.collection_type_descriptions = COLLECTION_TYPE_DESCRIPTION_FACTORY
        self.model = app.model
        self.security = app.security

        self.hda_manager = hdas.HDAManager(app)
        self.history_manager = histories.HistoryManager(app)
        self.tag_handler = tags.GalaxyTagHandler(app.model.context)
        self.ldda_manager = lddas.LDDAManager(app)
```

`UniverseApplication` creates a `DatasetCollectionManager` for the application and `DatasetCollectionManager` imports and annotates the `UniverseApplication` as a requirement. This creates an unfortunate dependency loop.

**Dependencies should form a DAG (directed acyclic graph)**.

---

## Why an Interface?

By using `StructuredApp` interface instead of `UniverseApplication`:

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

Dependencies now closer to a DAG - `DatasetCollectionManager` no longer annotated with the type `UniverseApplication`! Imports are cleaner.

---

## Benefits of Typing

- **mypy** provides robust type checking
- **IDE** can provide hints to make developing this class and usage of this class easier

---

## Design Problems with Handling Dependencies Directly

- `DatasetCollectionManager` needs to know how to construct all the other managers it is using, not just their interface
- `app` has an instance of this class and `app` is used to construct an instance of this class - this circular dependency chain results in brittleness and complexity in how to construct `app`
- `app` is very big and we're depending on a lot of it but not a large percent of it. This makes typing less than ideal

---

## Testing Problems with Handling Dependencies Directly

- Difficult to unit test properly
  - What parts of app are being used?
  - How do we construct a smaller app with just those pieces?
  - How do we stub out classes cleanly when we're creating the dependent objects internally?

---

## Design Benefits of Injecting Dependencies

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

- We're no longer depending on `app`
- The type signature very clearly delineates what dependencies are required
- Unit testing can inject precise dependencies supplying only the behavior needed

---

## What is Type-based Dependency Injection?

A dependency injection **container** keeps tracks of singletons or recipes for how to construct each type. By default when it goes to construct an object, it can just ask the container for each dependency based on the type signature of the class being constructed.

If an object declares it consumes a dependency of type `X` (e.g. `HDAManager`), just query the container recursively for an object of type `X`.

---

## Object Construction Simplification

Once all the dependencies have been type annotated properly and the needed singletons have been configured.

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

---

## Picking a Library

Many of the existing DI libraries for Python predate widespread Python 3 and don't readily infer things based on types. The benefits of typing and DI are both enhanced by the other - so it was important to pick one that could do type-based injection.

We went with **Lagom**, but we've built abstractions that would make it very easy to switch.

---

## Lagom

https://lagom-di.readthedocs.io/en/latest/

Lagom is a dependency injection library designed for Python 3.7+ with type hints.

---

## Tips for Designing New Galaxy Backend Components

- Consume only the related components you need to avoid `app` when possible
- Annotate inputs to the component with Python types
- Use interface types to shield consumers from implementation details
- Rely on Galaxy's dependency injection to construct the component and provide it to consumers
