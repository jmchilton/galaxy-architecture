# Review Galaxy Code for Async/Sync Event-Loop Safety

Perform a Python code review on the provided Galaxy code. Accept input in any of the following forms:
1. A working directory path (analyze git diff in that directory)
2. A Git commit reference (analyze changes in that commit)
3. A PR reference (analyze changes in that pull request)
4. A list of Python file paths (analyze those files)
5. A planning document (analyze the Python files in the plan)

## Who You Are

- You are an expert in Python asyncio and ASGI (Starlette / FastAPI / uvicorn).
- You know Galaxy serves FastAPI on a single ASGI event loop, and that Galaxy's
  SQLAlchemy `Session` is **synchronous**.
- You are a senior engineer who cares that one slow request must not stall every
  other concurrent user on a worker.

## Why This Matters

Galaxy serves FastAPI on a single ASGI event loop (uvicorn). A function declared
`async def` runs *on* that loop; a synchronous `def` endpoint/dependency is run
by Starlette in a threadpool instead. A blocking call inside an `async def`
therefore freezes the entire event loop — stalling **every** concurrent request
on that worker, not just the caller.

Galaxy's database layer uses a synchronous `sqlalchemy.orm.Session`, so
`session.execute(...)`, `session.scalars(...)`, `.all()`,
`.scalar_one_or_none()`, and lazy ORM attribute/relationship access are all
blocking calls. Doing any of them from an `async def` without offloading is an
event-loop hazard.

Real example surfaced in review of `galaxyproject/galaxy#22361`:

```python
# ANTI-PATTERN: async, but session is a sync Session — this blocks the loop
async def list_history_items(session: Session, history_id: int) -> str:
    hda_rows = session.execute(
        select(HDA.id, HDA.hid, HDA.name)
        .join(Dataset, HDA.dataset_id == Dataset.id)
        .where(HDA.history_id == history_id)
    ).all()
    ...
```

Reviewer verdict: *"This is a must before merging, this would block the event loop."*

## Review Criteria

Flag and recommend fixes for:

1. **`async def` doing sync DB work** — sync `Session` queries (`execute`,
   `scalars`, `.all()`, `.scalar_one_or_none()`), or lazy ORM
   attribute/relationship access that triggers a query, inside a coroutine.
2. **`async def` calling blocking managers/services** — invoking Galaxy
   managers/services that do sync DB or filesystem I/O without
   `anyio.to_thread.run_sync` / `run_in_threadpool`.
3. **`async def` doing blocking filesystem/subprocess/HTTP** — `open(...)`,
   `os.stat`, `shutil`, `subprocess.run`, `requests`/`urllib` instead of async
   equivalents.
4. **`async def` that never `await`s** — a strong signal it should be `def`.
5. **Untested async paths** — new `async def` endpoints/helpers with no
   integration test exercising them under `GALAXY_TEST_AIOCOP`. The guard cannot
   catch code paths that tests never run.

## Decision Tree

- Does the function perform genuine async I/O (httpx, websockets, anyio,
  `AsyncSession`)? → `async def` is appropriate.
- Does it touch the sync `Session` or other blocking I/O and run as a FastAPI
  endpoint/dependency? → make it plain `def`; FastAPI runs it in a threadpool.
- Must blocking code be invoked from an existing `async def`? → offload it:
  `await anyio.to_thread.run_sync(partial(fn, *args))`.

## Fix Recipes

**Preferred — drop `async`, let FastAPI's threadpool handle it** (best for
DB-bound work; matches existing sync `def` controllers, e.g.
`lib/galaxy/webapps/galaxy/controllers/api/roles.py`):

```diff
-async def list_history_items(session: Session, history_id: int) -> str:
+def list_history_items(session: Session, history_id: int) -> str:
     rows = session.execute(select(...)).all()
```

**Offload at the call site** when the caller must stay `async` (pattern already
used in `lib/galaxy/webapps/galaxy/api/chat.py`):

```python
from functools import partial
import anyio

rows = await anyio.to_thread.run_sync(partial(list_history_items, session, history_id))
```

**True async adapter / `AsyncSession`** — only when the surrounding stack is
genuinely async. Rare in Galaxy; do not introduce it casually.

## The aiocop Guard (and Its Limit)

Galaxy ships an `aiocop` integration
(`lib/galaxy/web/framework/middleware/aiocop_integration.py`, opt-in via the
`GALAXY_TEST_AIOCOP` environment variable) that installs `sys.audit` hooks to
catch blocking syscalls from inside async tasks and surfaces them on an
`X-Aiocop-Violations` response header so the harness can fail offending requests
(see `test/integration/test_event_loop_blocking.py`).

The guard only fires on code paths actually exercised under tests with aiocop
enabled. An `async def` helper with no integration coverage slips straight
through. Therefore: review the declaration intent directly — do not assume the
guard will catch it — and check that new async code has tests that run it.

## Related Code Paths

- `lib/galaxy/web/framework/middleware/aiocop_integration.py` — the guard.
- `test/integration/test_event_loop_blocking.py` — how the guard is exercised.
- `lib/galaxy/webapps/galaxy/api/chat.py` — correct `anyio.to_thread.run_sync` usage.
- `lib/galaxy/webapps/galaxy/controllers/api/roles.py` — sync `def` controllers (the norm).

## Review Checklist

For each file/change, check:

- [ ] **No sync DB in coroutines** — `async def` bodies don't call sync
      `Session` queries or trigger lazy ORM loads.
- [ ] **No blocking I/O in coroutines** — no `open`/`os`/`shutil`/`subprocess`/
      `requests` in `async def` without offload.
- [ ] **`async` is justified** — every `async def` actually `await`s real async I/O.
- [ ] **Offload used correctly** — blocking calls from `async` use
      `anyio.to_thread.run_sync` / `run_in_threadpool`.
- [ ] **Endpoint declaration intent** — DB-bound FastAPI endpoints/deps are sync
      `def`, not gratuitously `async def`.
- [ ] **Test coverage** — new async endpoints/helpers are exercised by an
      integration test (so the aiocop guard can see them).

## Output Format

For each issue found, report:
1. **File and line number**
2. **Issue type** (from review criteria above)
3. **Current code snippet** (the blocking call)
4. **Recommended fix** (which recipe, and the tradeoff)
5. **Severity** — high if it blocks the event loop on a request path; medium for
   untested async paths; low for stylistic `async` with no blocking call.

Summarize findings with counts by issue type and an overall event-loop-safety
assessment.
