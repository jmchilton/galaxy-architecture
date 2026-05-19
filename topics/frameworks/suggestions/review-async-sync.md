# Content Suggestions: review-async-sync

Ideas to make the generated `review-async-sync` command more effective by
enriching `topics/frameworks/content.yaml`.

## Strong additions

- **A worked "good" controller slide** showing a sync `def` endpoint that calls
  a manager doing DB work, side by side with the offload variant. The command
  currently describes the fixes; a canonical positive example from Galaxy would
  let the reviewer pattern-match instead of reason from rules.
- **Lazy-load trap example** — a slide showing an `async def` that returns fast
  but triggers a blocking query via lazy relationship access
  (`hdca.collection.elements`). This is the subtlest red flag and deserves its
  own concrete example; it overlaps with the PR #22361 memory comments.
- **aiocop output sample** — show an actual `X-Aiocop-Violations` header / log
  line so the command can teach the agent to recognize guard output in test
  logs and CI, not just reason about source.

## Medium additions

- **WSGI vs ASGI contrast** — a note that legacy WSGI controllers do not have
  this hazard (each request is its own thread), so the rule is specific to the
  FastAPI/ASGI path. Prevents false positives on legacy code.
- **`run_in_threadpool` vs `anyio.to_thread.run_sync`** — a one-line note on
  when each is idiomatic in Galaxy, so recommendations are consistent.

## Content gaps observed while generating

- `content.yaml` has no positive/"good" full example for this section — only the
  anti-pattern and the diff. The command had to synthesize the good path from
  `roles.py` and `chat.py` references rather than from topic content.
- No coverage of how to *test* an async path under aiocop locally (the env var
  and the integration test exist but the invocation recipe is not in content).
  A short prose block with the local repro command would let the command give
  actionable test guidance.
