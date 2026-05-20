# Improvement Suggestions for `review-async-sync` Operation

Suggestions for enhancing `topics/frameworks/content.yaml` to make the
`review-async-sync` code review operation more effective.

## Content Gaps Identified

### 1. Missing: Canonical "good" controller example

**Problem:** Current async/sync content shows the anti-pattern and the fix
diff, but no end-to-end positive example. The generated command had to
synthesize the good path from references to `roles.py` and `chat.py`
rather than from topic content.

**Suggestion:** Add a slide pairing a sync `def` endpoint with the manager
it calls (DB-bound), and a second showing the same flow with an
`anyio.to_thread.run_sync` offload when the caller must stay `async`.
Reviewers can then pattern-match instead of reasoning from rules.

### 2. Missing: Lazy ORM load trap

**Problem:** The subtlest red flag is an `async def` that returns fast but
triggers a blocking query via lazy relationship access
(`hdca.collection.elements`, attribute autoloads). This kind of block
doesn't look like a query in the source.

**Suggestion:** A dedicated slide showing a lazy-load chain inside `async
def` and the diff to either eager-load (`selectinload`) or sync-ify the
helper. Worth its own block because it's not visible by grep.

### 3. Missing: WSGI-vs-ASGI scope clarification

**Problem:** The rule "default to sync `def`" is specific to the ASGI/
FastAPI path. Legacy WSGI controllers do not have this hazard — each
request is its own thread. Without this scope statement the review command
risks false positives on legacy code.

**Suggestion:** Short prose block (or bullet on the convention slide)
stating that the rule applies to FastAPI/ASGI handlers and async tasks;
WSGI controllers are unaffected.

### 4. Missing: aiocop output sample

**Problem:** The aiocop slide and prose describe the `X-Aiocop-Violations`
header abstractly. Reviewing CI/test output requires recognizing the actual
log line and header format.

**Suggestion:** Add a small inline sample of the log message and the
header string so the command can teach the agent to spot guard output in
test logs, not just reason about source.

### 5. Missing: Local aiocop repro recipe

**Problem:** The env var and the integration test exist but the invocation
recipe is not in the topic content. Reviewers can't easily tell a
contributor *how* to run their new async path under the guard locally.

**Suggestion:** Short prose block with the local repro command (env var +
`pytest` invocation) so the command can give actionable test guidance.

## Specific Content Additions

### Add: `run_in_threadpool` vs `anyio.to_thread.run_sync` idiom

The convention slide shows `anyio.to_thread.run_sync` (matching
`api/chat.py`). FastAPI also offers `starlette.concurrency.run_in_threadpool`.
A one-line note on which Galaxy prefers and why would let recommendations
stay consistent across reviewers.

## Priority Ranking

1. **High:** Lazy ORM load trap — subtlest red flag; deserves an explicit example.
2. **High:** Canonical "good" controller example — command currently synthesizes from outside references.
3. **Medium:** WSGI-vs-ASGI scope clarification — prevents false positives on legacy code.
4. **Medium:** aiocop output sample — teaches log/header recognition in CI.
5. **Low:** Offload-utility idiom note — small consistency win.
6. **Low:** Local aiocop repro recipe — useful but covered elsewhere in Galaxy docs.
