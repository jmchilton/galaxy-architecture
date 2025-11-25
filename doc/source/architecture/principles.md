# Galaxy Architecture Principles

> 📊 <a href="slides.html">View as training slides</a>

## Learning Questions
- What are the guiding principles of Galaxy architecture?
- Why is the frontend opinionated but the backend plugin-driven?
- Who are the target audiences for each component?

## Learning Objectives
- Understand the contrasting philosophies of frontend vs backend
- Learn why Galaxy is designed for flexibility
- Identify the target users for each layer

## Aspirational Principles of Galaxy Architecture

Whereas the architecture of the frontend (Web UI) aims for consistency and is
highly opinionated, the backend (Python server) is guided by flexibility and is meant to be driven by plugins whenever possible.

## An Opinionated Frontend

- The target audience is a *bench scientist* - no knowledge of programming, paths, or command lines should be assumed.
- Consistent colors, fonts, themes, etc...
- Reusable components for presenting common widgets - from the generic (forms and grids) to the specific (tools and histories).
- Tied to specific technologies:
  - Implemented in TypeScript
  - Built with [webpack](https://webpack.js.org/)
  - [Vue.js](https://vuejs.org/) for component definitions

## A Plugin Driven Backend

Galaxy's backend is in many ways driven by *pluggable interfaces* and
can be adapted to many different technologies.

- SQLAlchemy allows using SQLite, PostgreSQL, or MySQL (sort of) for your database.
- Many different cluster backends or job managers are supported.
- Different frontend proxies (e.g. nginx) are supported as well as web
  application containers (e.g. uvicorn, gunicorn).
- Different storage strategies and technologies are supported (e.g. S3, iRODS).
- Tool definitions, job metrics, stat middleware, tool dependency resolution, workflow modules,
  datatype definitions are all plugin driven.

## A Plugin Driven Backend but...

Galaxy has long been guided by the principle that cloning it and calling
the `run.sh` should "just work" and should work quickly.

So by default Galaxy does not require:

 - Compilation - it fetches *binary wheels* for your platform.
 - A job manager - Galaxy can act as one.
 - An external database server - Galaxy can use an sqlite database.
 - A web proxy or external Python web server.

## In other words...

The Galaxy frontend is architected with the bench scientist in mind first and foremost,
the Galaxy backend is architected with Galaxy administrators in mind first and foremost.

## Key Takeaways
- Frontend: opinionated, consistent, for bench scientists
- Backend: plugin-driven, flexible, for administrators
- Galaxy runs out of the box with minimal dependencies
- Architecture balances simplicity and extensibility
