# Galaxy Application Components: Models, Managers, and Services

> 📊 <a href="slides.html">View as training slides</a>

## Learning Questions
- How is business logic organized in Galaxy?
- What are models, managers, and services?
- How does the database layer work?

## Learning Objectives
- Understand the three-layer architecture
- Learn about SQLAlchemy and the ORM
- Understand database migrations with Alembic
- Navigate the Galaxy data model

![This section will talk about that manager layer and what lies below](../_images/asgi_app.plantuml.svg)

There are many ways to describe and visualize the Galaxy server architecture,
one is to imagine the Galaxy database as the ultimate source for Galaxy "stuff"
and the API controllers as the ultimate sink.

In this architecture imagining of Galaxy, managers are the layer meant to
mediate all controller interactions (and isolate the backend from the web
framework) while the model layer is meant to mediate all database interactions
(and isolate the backend from database internals).

![Models and Managers](../_images/core_models_managers.plantuml.svg)

## Services

Handle API and web processing details of requests and responses at a high-level.

Thin layer below the controllers to shield applciation logic from FastAPI internals.

In practice, it is totally fine to skip this layer and have FastAPI controllers talk directly
to managers. Also in practice, there are many places where the controller or service layers
are thicker than they should be - and these are anti-patterns that shouldn't be followed.

## Managers

High-level business logic that ties all of these components together.

Controllers should ideally be thin wrappers around actions defined in managers.

Whenever a model requires more than just the database, the operation should be defined
in a manager instead of in the model.

## Managers - Some Key Files

![Key Managers](../_images/core_files_managers.mindmap.plantuml.svg)

## Managers - Some Helpers

![Manager Helpers](../_images/core_files_managers_helpers.mindmap.plantuml.svg)

## Galaxy Models

- Database interactions powered by SQLAlchemy - [https://www.sqlalchemy.org/.](https://www.sqlalchemy.org/.)
- Galaxy doesn't think in terms of "rows" but "objects".
- Classes for Galaxy model objects defined in `lib/galaxy/model/__init__.py`.
- Classes mapped to database objects in same module via "declarative mapping".
  - Classes/attributes mapped to tables/columns
  - Associations between classes mapped to relationships between tables

![SQLAlchemy Architecture](../_images/sqla_arch_small.png)

## Galaxy Database Schema Migrations

- Automated execution of incremental, reversible changes to the database schema.
- Performed to update or revert the database schema to a newer or older version.
- Powered by Alembic - [https://alembic.sqlalchemy.org/.](https://alembic.sqlalchemy.org/.)
  - (as of 22.05; prior to that by SQLAlchemy Migrate)
- Each file in `lib/galaxy/model/migrations/alembic/versions_gxy` represents a migration description
  - `e7b6dcb09efd_create_gxy_branch.py`
  - `6a67bf27e6a6_deferred_data_tables.py`
  - `b182f655505f_add_workflow_source_metadata_column.py`

## More on Schema Migrations

- Great documentation in code README - `lib/galaxy/model/migrations/README.md`
  - Admin perspective on how to migrate databases forward and revert on problems.
  - Developer persepctive on how to add new revisions.
- Galaxy's data model is split into the galaxy model and the legacy install model:
  - Persisted in one combined database or two separate databases
  - Represented by 2 migration branches: "gxy" and "tsi"
- Schema changes defined in revision modules:
  - `lib/galaxy/model/migrations/alembic/versions_gxy` (gxy branch: galaxy model)
  - `lib/galaxy/model/migrations/alembic/versions_tsi` (tsi branch: legacy install model)

## Database Diagram

![Galaxy Schema](../_images/galaxy_schema.png)

[https://galaxyproject.org/admin/internals/data-model/](https://galaxyproject.org/admin/internals/data-model/)

![HDA foor bar...](../_images/hda.svg)

![HDA Dataset](../_images/hda_dataset.plantuml.svg)

## Dataset Metadata

- Typed key-value pairs attached to HDA.
- Keys and types defined at the datatype level.
- Can be used by tools to dynamically control the tool form.

![HDAs and HDCAs](../_images/hda_hdca.plantuml.svg)

![Workflows](../_images/workflow_definition.svg)

![Workflow Running](../_images/workflow_run.svg)

![Libraries](../_images/libraries.svg)

![Library Permissions](../_images/library_permissions.svg)

## Key Takeaways
- Services handle high-level API processing
- Managers contain business logic
- Models mediate database interactions
- SQLAlchemy provides ORM
- Alembic handles schema migrations
