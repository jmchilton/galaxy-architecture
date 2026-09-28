Perform a code review on the provided Galaxy code. Accept input in any of following forms:
* A working directory path (analyze git diff in that directory)
* A Git commit reference (analyze changes in that commit)
* A PR reference (analyze changes in that pull request)
* A list of Python file paths (analyze those files)
* A planning document (analyze the Python files in the plan)

This Claude command should orchestrate a review of the supplied code. There are preconditions
and other target commands in the same directory as this command for each precondition. This agent
should evaluate each precondition and if it is met, launch a subagent to perform the review
of the supplied changes to this agent.

- Precondition: These changes contain Python code.
  Command: py-review-code-structure.md
- Precondition: These changes contain Python code.
  Command: gx-review-di.md
- Precondition: These changes contain Python code that touches async code, ASGI/FastAPI request handling, or code called from the event loop.
  Command: gx-review-async-sync.md
- Precondition: These changes contain Python code that adds or modifies an API endpoint.
  Command: gx-fastapi-review.md
- Precondition: These changes contain Python code that adds or modifies an API endpoint.
  Command: gx-review-business-logic-organization.md
- Precondition: These changes add or modify tests (under `lib/galaxy_test/`, `test/`, or `client/src/`).
  Command: gx-review-test-types.md
- Precondition: These changes contain Python tests.
  Command: py-challenge-patches.md
- Precondition: These changes contain client unit tests (`client/src/**/*.test.js` or `client/src/**/*.test.ts`).
  Command: gx-vitest-review.md
- Precondition: These changes contain E2E tests (`lib/galaxy_test/selenium/` or `test/integration_selenium/`).
  Command: gx-e2e-review.md
- Precondition: These changes contain client Vue components (`client/src/**/*.vue`).
  Command: gx-review-ui-components.md
- Precondition: These changes contain an Alembic database migration.
  Command: gx-review-migration.md
