# Galaxy Testing

> 📊 <a href="tests/slides.html">View as slides</a>

## Learning Questions
- Where should I put a new test?
- How do I write an API test?
- When should I use an integration test vs an API test?
- How do I test code that requires special Galaxy configuration?
- How do I write Selenium/Playwright tests?

## Learning Objectives
- Use the decision tree to select appropriate test type
- Write Python unit tests for isolated components
- Write API tests using populators and assertions
- Write integration tests with custom Galaxy configuration
- Write Selenium tests using the smart component system
- Understand CI workflows for each test type

## Writing Tests for Galaxy

Tests are essential for Galaxy development:

- **Prevent regressions** as code evolves
- **Document behavior** through executable examples
- **Enable refactoring** with confidence
- **Run in CI** on every pull request


Galaxy has a comprehensive test suite covering everything from isolated
Python functions to full-stack browser automation. This topic guides
you through the different test types, when to use each, and how to write
effective tests for your Galaxy contributions.


## Other Resources

- `./run_tests.sh --help` - Command-line options
- [GTN Writing Tests Tutorial](https://training.galaxyproject.org/training-material/topics/dev/tutorials/writing_tests/tutorial.html) - Hands-on exercises
- `client/README.md` - Client-side testing details
- [Galaxy Architecture Slides](https://training.galaxyproject.org/training-material/topics/dev/tutorials/architecture/slides.html) - CI overview


The `run_tests.sh` script is the primary entry point for running Galaxy's
Python tests. Its help output provides the most up-to-date documentation
on available test suites and command-line flags. The GTN tutorial provides
hands-on exercises covering API tests, unit tests, and testability patterns.


## Quick Reference

| Test Type | Location | Run Command |
|-----------|----------|-------------|
| Unit (Python) | `test/unit/` | `./run_tests.sh -unit` |
| Unit (Client) | `client/src/` | `make client-test` |
| API | `lib/galaxy_test/api/` | `./run_tests.sh -api` |
| Integration | `test/integration/` | `./run_tests.sh -integration` |
| Framework | `test/functional/tools/` | `./run_tests.sh -framework` |
| Workflow Framework | `lib/galaxy_test/workflow/` | `./run_tests.sh -framework-workflows` |
| Selenium | `lib/galaxy_test/selenium/` | `./run_tests.sh -selenium` |
| Playwright | `lib/galaxy_test/selenium/` | `./run_tests.sh -playwright` |
| Selenium Integration | `test/integration_selenium/` | `./run_tests.sh -selenium` |


This table provides a quick reference for finding and running each test
type. Note that Selenium and Playwright tests share the same test files
in `lib/galaxy_test/selenium/` but use different browser automation
backends. The run commands shown are the most common invocations; see
`run_tests.sh --help` for additional options.


## Which Test Type?

![Test Type Decision Tree](../_images/tests-decision-tree.mermaid.svg)


The decision tree helps you choose the right test type for your needs.
The primary questions are: Does the test need a running Galaxy server?
Does it need a web browser? Does it need custom Galaxy configuration?
Your answers guide you to the appropriate test suite.


## Decision Tree Walkthrough

**No running server needed?** &rarr; Unit test
- Python backend &rarr; `test/unit/`
- ES6/Vue client &rarr; `client/src/`

**Server needed, no browser?**
- Standard config &rarr; API test
- Custom config &rarr; Integration test
- Tool/workflow only &rarr; Framework test

**Browser needed?** &rarr; Selenium/Playwright


Start by asking whether your test needs a running Galaxy server. If not,
it's a unit test. If yes, consider whether you need browser automation.
Most backend tests work best as API tests since they're faster and more
reliable than browser tests. Only use integration tests when you need
custom Galaxy configuration, and only use Selenium tests when testing
the actual UI.


## Python Unit Tests

**Location:** `test/unit/`

**When to use:**
- Component can be tested in isolation
- No database or web server needed
- Complex logic worth testing independently

**Run:** `./run_tests.sh -unit`


Python unit tests are located in `test/unit/` and run via pytest. They're
ideal for components that are well-architected for isolation - those that
shield complexity from consumers and have minimal external dependencies.
Unit tests are fast and reliable since they don't require Galaxy's
infrastructure.


## Doctests Guidance

[Doctests](https://docs.python.org/3/library/doctest.html) are executable examples embedded in docstrings - Python runs them to verify documentation stays accurate.

> Doctests are more brittle and more restrictive.

**Use doctests when:**
- Tests serve as documentation (definitely)
- Tests are simple and isolated (maybe)

**Use standalone tests when:**
- Tests are complex
- Tests need fixtures or mocking
- Tests verify edge cases


Doctests can be useful when the test itself serves as high-quality
documentation for the component. However, they're harder to maintain
and more restrictive than standalone test files. For most cases,
prefer writing tests in `test/unit/` where you have full access to
pytest fixtures and standard testing patterns.


## External Dependency Tests

Tests in `test/unit/tool_util/` are "slow" tests that interact with external services:

```python
from .util import external_dependency_management

@external_dependency_management
def test_conda_install(tmp_path):
    # ... test conda operations
```

**Run separately:**
```bash
tox -e mulled
# or:
pytest -m external_dependency_management test/unit/tool_util/
```


Some unit tests interact with external services like Conda, container
registries, or BioContainers. These are marked with the
`@external_dependency_management` decorator and excluded from normal
unit test runs since they're slow and depend on network access. Run
them explicitly with `tox -e mulled` when needed.


## Python Unit Test CI

**CI Platform:** GitHub Actions

**Workflow:** `.github/workflows/unit.yaml`

**Characteristics:**
- Runs on every pull request
- Tests multiple Python versions (3.9, 3.14)
- Moderately prone to flaky failures
- If tests fail unrelated to your PR, request a re-run


Python unit tests run automatically on every pull request via GitHub
Actions. The test suite can occasionally fail due to transient issues
unrelated to your changes. If you see failures that don't seem related
to your PR, ping the Galaxy committers to request a re-run.


## Frontend Unit Tests

Galaxy's client unit tests test the ES6/TypeScript/Vue frontend components.

Technologies:
- [Vitest](https://vitest.dev/) - Test framework
- [Vue Test Utils](https://vue-test-utils.vuejs.org/) - Component testing
- [MSW](https://mswjs.io/) - API mocking


New client-side code submissions should include
accompanying unit tests for the developer-facing API. Vitest provides
the test framework, Vue Test Utils enables component testing, and MSW
(Mock Service Worker) provides type-safe API mocking.


## Test File Structure

Place tests adjacent to code with `.test.ts` extension (older tests may use .test.js):

```
src/components/MyComponent/
├── MyComponent.vue
├── MyComponent.test.ts
└── test-utils.ts        # optional shared utilities
```

**Standard imports:**
```typescript
import { createTestingPinia } from "@pinia/testing";
import { getLocalVue } from "@tests/vitest/helpers";
import { shallowMount } from "@vue/test-utils";
import { useServerMock } from "@/api/client/__mocks__";
import { beforeEach, describe, expect, it, vi } from "vitest";
```


Client tests are colocated with the source code they test, following
the `*.test.ts` naming convention. This makes it easy to find tests
for a given component and keeps related code together. The standard
imports pattern shows the common utilities you'll use in most tests.


## Galaxy Testing Infrastructure

**LocalVue Setup** - configures BootstrapVue, Pinia, localization:

```typescript
const localVue = getLocalVue();
// or with localization testing:
const localVue = getLocalVue(true);
```

**Test Data Factories** - consistent test data:

```typescript
import { getFakeRegisteredUser } from "@tests/test-data";
const user = getFakeRegisteredUser({ id: "custom-id", is_admin: true });
```


Galaxy provides testing infrastructure to simplify component setup.
`getLocalVue()` returns a Vue instance configured with common plugins.
Test data factories like `getFakeRegisteredUser()` provide consistent
mock data. Helper functions suppress known console warnings from
third-party libraries that would otherwise clutter test output.


## Test Data Factories

Galaxy's `@tests/test-data` module provides factory functions for creating
consistent test fixtures:

```typescript
import {
    getFakeRegisteredUser,
    getFakeHistory,
    getFakeHistoryDataset,
} from "@tests/test-data";

// Create with defaults
const user = getFakeRegisteredUser();

// Override specific fields
const adminUser = getFakeRegisteredUser({ is_admin: true });
const history = getFakeHistory({ name: "Test History", size: 1024 });
```

**When to use factories vs inline data:**
- **Use factories** when you need realistic, complete objects with all required fields
- **Use inline data** for minimal test cases focused on specific fields
- **Extend factories** when tests need consistent variations (e.g., admin users)

Available factories include user types (`getFakeRegisteredUser`, `getFakeAnonymousUser`),
histories, datasets, and other common Galaxy objects. Check `client/tests/test-data/`
for the complete list.


## API Mocking with MSW

Galaxy uses [MSW](https://mswjs.io/) with [OpenAPI-MSW](https://github.com/christoph-fricke/openapi-msw) for type-safe API mocking:

```typescript
import { useServerMock } from "@/api/client/__mocks__";

const { server, http } = useServerMock();

beforeEach(() => {
    server.use(
        http.get("/api/histories/{history_id}", ({ response }) => {
            return response(200).json({
                id: "history-id", name: "Test History",
            });
        }),
    );
});
```


MSW intercepts API requests at the network level, providing realistic
API mocking. The `useServerMock()` helper sets up MSW with Galaxy's
OpenAPI spec, giving you type-safe request handlers. This is the
preferred approach over axios-mock-adapter for new tests.


## shallowMount vs mount

**Prefer `shallowMount`** for client unit tests.

| `shallowMount` (preferred) | `mount` |
|---------------------------|---------|
| Stubs child components | Renders full tree |
| Tests component in isolation | Tests integration |
| Faster, fewer mocks needed | Slower, more setup |

```typescript
// Preferred: isolated unit test
const wrapper = shallowMount(MyComponent, { localVue, pinia });
```

Integration testing &rarr; use Selenium/Playwright instead.


Client-side tests should be focused unit tests that verify individual
component behavior. `shallowMount` stubs all child components, keeping
tests isolated and fast. For testing parent-child interactions across
the full component tree, Galaxy's Selenium/Playwright tests are better
suited since they test the real application in a browser.


## Mount Wrapper Factories

Create reusable mount functions for complex setup:

```typescript
async function mountMyComponent(propsData = {}, options = {}) {
    const pinia = createTestingPinia({ createSpy: vi.fn });

    const wrapper = shallowMount(MyComponent, {
        localVue,
        propsData: { defaultProp: "value", ...propsData },
        pinia,
        ...options,
    });

    await flushPromises();
    return wrapper;
}
```


For components with complex setup requirements, create a factory function
that handles Pinia setup, default props, and waiting for promises. This
keeps individual tests focused on behavior rather than boilerplate setup.


## Selector Constants & Events

**Define selectors as constants:**
```typescript
const SELECTORS = {
    SUBMIT_BUTTON: "[data-description='submit button']",
    ERROR_MESSAGE: "[data-description='error message']",
};
expect(wrapper.find(SELECTORS.ERROR_MESSAGE).exists()).toBe(true);
```

**Testing emitted events:**
```typescript
await wrapper.find("input").setValue("new value");

expect(wrapper.emitted()["update:value"]).toBeTruthy();
expect(wrapper.emitted()["update:value"][0][0]).toBe("new value");
```


Define selectors as constants for maintainability - when component
structure changes, update selectors in one place. For events, use
`wrapper.emitted()` to verify components emit the right events with
correct payloads.


## Pinia Store Testing

**In component tests:**
```typescript
const pinia = createTestingPinia({ createSpy: vi.fn, stubActions: false });
setActivePinia(pinia);

const wrapper = shallowMount(MyComponent, { localVue, pinia });

const userStore = useUserStore();
userStore.currentUser = getFakeRegisteredUser();
```

**Isolated store tests:**
```typescript
beforeEach(() => setActivePinia(createPinia()));

it("updates state correctly", () => {
    const store = useMyStore();
    store.doAction();
    expect(store.someState).toBe("expected");
});
```


For component tests, use `createTestingPinia()` which provides a mock
Pinia instance with spied actions. For isolated store unit tests, use
a real Pinia instance to test store logic directly.


## Async Operations

**Use `flushPromises()` after API calls:**
```typescript
const wrapper = shallowMount(MyComponent, { localVue, pinia });
await flushPromises(); // Wait for mounted() API calls
```

**Use `nextTick()` for Vue reactivity:**
```typescript
await wrapper.setProps({ value: "new" });
await nextTick();
expect(wrapper.text()).toContain("new");
```


Many component operations are asynchronous. Use `flushPromises()` to
wait for all pending promises (API calls, async setup). Use Vue's
`nextTick()` when waiting for reactive updates to propagate to the DOM.


## Testing Best Practices

1. **Test behavior, not implementation**
2. **Avoid `wrapper.vm` directly** - test through template
3. **One behavior per test**
4. **Descriptive names**: `"displays error when API returns 500"`
5. **Clean up in `beforeEach`/`afterEach`**
6. **Mock external services, not component logic**
7. **Test edge cases**: errors, empty data, boundaries


Focus on what users see and experience, not internal implementation
details. Keep tests focused on a single behavior with clear names.
Mock at appropriate boundaries - external services yes, component
logic no. Don't forget edge cases like error states and empty data.


## Good vs Bad Test Examples

**GOOD: Test user-visible behavior**
```typescript
test('displays error message when API fails', async () => {
    server.use(http.get("/api/data", ({ response }) => response(500).json({})));
    const wrapper = shallowMount(MyComponent, { localVue, pinia });
    await flushPromises();
    expect(wrapper.text()).toContain('Error loading data');
});
```

**BAD: Test implementation details**
```typescript
test('calls fetchData method', () => {
    const fetchDataSpy = vi.spyOn(wrapper.vm, 'fetchData');
    wrapper.vm.loadData();
    expect(fetchDataSpy).toHaveBeenCalled();
});
```


## Running Client Tests

**Full test run (CI):**
```bash
make client-test
```

**Watch mode (development):**
```bash
yarn test:watch
yarn test:watch MyModule      # Filter by name
yarn test:watch workflow/run  # Filter by path
```


The `make client-test` command runs the complete client test suite,
which is what CI executes. During development, use watch mode for
fast feedback - tests rerun automatically on file changes. Filter
to specific tests by passing a pattern.


## Client Test CI

**CI Platform:** GitHub Actions

**Workflow:** `.github/workflows/client-unit.yaml`

**Linting:** Run before submitting PRs:
```bash
make client-lint     # Check for issues
make client-format   # Auto-fix formatting
```


Client unit tests run automatically on every pull request via GitHub
Actions. Prettier enforces code style, so run `make client-lint` and
`make client-format` before submitting. If tests fail unrelated to
your changes, request a re-run.


## Tool Framework Tests Overview

**Location:** `test/functional/tools/`

**What they test:**
- Galaxy tool wrapper definitions (XML)
- Complex tool internals via actual tool execution
- Legacy behavior compatibility

**When to use:**
- Testing tool XML features
- Verifying tool test assertions work correctly
- No need to write Python - just XML


A surprising amount of Galaxy's complexity is in tool wrapper definitions.
The Tool Framework Tests ("Framework Tests") exercise these internals by
running actual tool tests. This suite uses sample tools in
`test/functional/tools/` to verify everything from simple parameter
handling to complex output discovery. Adding a test here is often simpler
than writing a Python API test.


## Adding a Tool Test

**Option 1:** Add test block to existing tool

```xml
<!-- In test/functional/tools/some_tool.xml -->
<tests>
    <test>
        <param name="input1" value="test.txt"/>
        <output name="out_file1" file="expected.txt"/>
    </test>
</tests>
```

**Option 2:** Add new tool to `sample_tool_conf.xml`

```xml
<tool file="my_new_tool.xml" />
```

**Run:** `./run_tests.sh -framework`


To add a framework test, either add a `<test>` block to an existing sample
tool or create a new tool XML file and register it in
`test/functional/tools/sample_tool_conf.xml`. The test framework handles
server startup, tool execution, and output verification automatically.
See Planemo's Test-Driven Development documentation for detailed guidance
on writing Galaxy tool tests.


## Workflow Framework Tests

**Location:** `lib/galaxy_test/workflow/`

**What they test:**
- Workflow evaluation engine
- Input handling and connections
- Output assertions

**Structure:** Each test has two files:
- `*.gxwf.yml` - Workflow definition (Format2 YAML)
- `*.gxwf-tests.yml` - Test cases with assertions

**Run:** `./run_tests.sh -framework-workflows`


Workflow Framework Tests verify Galaxy's workflow evaluation by running
workflows and checking outputs. Unlike tool tests which use embedded
`<tests>` blocks, workflow tests use separate definition and test files.
The workflow is defined in Galaxy's Format2 YAML syntax, and test cases
specify inputs and expected outputs.


## Workflow Framework Example

**Workflow** (`default_values.gxwf.yml`):
```yaml
class: GalaxyWorkflow
inputs:
  input_int:
    type: int
    default: 1
outputs:
  out:
    outputSource: my_tool/out_file1
steps:
  my_tool:
    tool_id: integer_default
    in:
      input1: { source: input_int }
```

**Tests** (`default_values.gxwf-tests.yml`):
```yaml
- doc: Test default value works
  job: {}
  outputs:
    out:
      asserts:
      - that: has_text
        text: "1"
```


This example shows a workflow that uses a default value for an integer
input. The test case provides an empty `job` (no inputs), expecting the
default to be used. The `asserts` section verifies the output contains
"1". You can also use `expect_failure: true` to verify workflows fail
correctly for invalid inputs.


## Framework Test CI

**Tool Framework:**
- Workflow: `.github/workflows/framework_tools.yaml`
- Stable, rarely flaky

**Workflow Framework:**
- Workflow: `.github/workflows/framework_workflows.yaml`
- Stable, rarely flaky

Both run on every PR and are maintained in GitHub Actions.


Framework tests run automatically on every pull request via GitHub Actions.
Both tool and workflow framework tests are among the most stable CI jobs,
typically not experiencing transient failures unrelated to the changes
under test. Failures usually indicate a real problem with your changes.


## API Tests Overview

**Location:** `lib/galaxy_test/api/`

**What they test:**
- Galaxy backend via HTTP API
- Standard Galaxy configuration
- Most backend functionality

**When to use:**
- Testing API endpoints
- Backend logic accessible via API
- No custom Galaxy config needed

**Run:** `./run_tests.sh -api`


API tests are Python tests that exercise Galaxy's backend by making HTTP
requests to the Galaxy API. They run against a Galaxy server with default
configuration and are generally preferred over integration tests because
they're faster (shared server) and can be run against external Galaxy
instances for deployment testing.


## Test Class Structure

```python
from galaxy_test.base.populators import DatasetPopulator
from ._framework import ApiTestCase

class TestMyFeatureApi(ApiTestCase):
    dataset_populator: DatasetPopulator

    def setUp(self):
        super().setUp()
        self.dataset_populator = DatasetPopulator(self.galaxy_interactor)

    def test_something(self):
        history_id = self.dataset_populator.new_history()
        response = self._get(f"histories/{history_id}")
        self._assert_status_code_is(response, 200)
```


API tests inherit from `ApiTestCase` which provides HTTP methods, server
setup, and Celery task handling. The `setUp` method initializes populators
for creating test data. The `galaxy_interactor` handles authentication
and request routing.


## HTTP Methods

```python
# GET request
response = self._get("histories")

# POST with data
response = self._post("histories", data={"name": "Test"})

# PUT, PATCH, DELETE
response = self._put(f"histories/{history_id}", data=payload)
response = self._patch(f"histories/{history_id}", data=updates)
response = self._delete(f"histories/{history_id}")

# Admin operations
response = self._get("users", admin=True)

# Run as different user (requires admin)
response = self._post("histories", data=data,
                      headers={"run-as": other_user_id}, admin=True)
```


The base class provides wrapped HTTP methods that handle authentication
and URL routing. Use `admin=True` for admin-only endpoints. The `run-as`
header lets admin users execute requests on behalf of other users.


## Populators Concept

**What:** Abstractions over Galaxy API for test data creation

**Why use them:**
- Simpler than raw HTTP requests
- Handle waiting for async operations
- Encapsulate common patterns
- Maintain consistency across tests

**Three main populators:**
- `DatasetPopulator` - datasets, histories, tools
- `WorkflowPopulator` - workflows
- `DatasetCollectionPopulator` - collections


Populators are the primary abstraction for creating test fixtures in
Galaxy tests. Rather than making raw API calls and handling async
operations manually, populators provide convenient methods that handle
the complexity. Despite its name, `DatasetPopulator` has become a hub
for many Galaxy operations beyond just datasets.


## DatasetPopulator

```python
self.dataset_populator = DatasetPopulator(self.galaxy_interactor)

# Create history and dataset
history_id = self.dataset_populator.new_history("Test History")
hda = self.dataset_populator.new_dataset(history_id, content="data", wait=True)

# Run a tool
result = self.dataset_populator.run_tool(
    tool_id="cat1",
    inputs={"input1": {"src": "hda", "id": hda["id"]}},
    history_id=history_id
)
self.dataset_populator.wait_for_tool_run(history_id, result, assert_ok=True)

# Get dataset content
content = self.dataset_populator.get_history_dataset_content(history_id)
```


`DatasetPopulator` is the most commonly used populator. It creates
histories and datasets, runs tools, and waits for jobs to complete.
The `wait=True` parameter blocks until the operation finishes. Use
`assert_ok=True` to fail the test if jobs don't complete successfully.


## DatasetPopulator Advanced

**Getting content - multiple ways to specify dataset:**
```python
# Most recent dataset in history
content = self.dataset_populator.get_history_dataset_content(history_id)
# By position (hid)
content = self.dataset_populator.get_history_dataset_content(history_id, hid=7)
# By dataset ID
content = self.dataset_populator.get_history_dataset_content(history_id, dataset_id=hda["id"])
```

**The `_raw` pattern** - for testing error responses:
```python
# Convenience: returns parsed dict, asserts success
result = self.dataset_populator.run_tool("cat1", inputs, history_id)

# Raw: returns Response for testing edge cases
response = self.dataset_populator.run_tool_raw("cat1", inputs, history_id)
assert_status_code_is(response, 400)  # Test error handling
```


Many populator methods have `_raw` variants that return the raw Response
object instead of parsed JSON. Use raw methods when testing error responses,
status codes, or API edge cases. The convenience methods are better for
readable tests focused on functionality rather than API details.


## WorkflowPopulator

```python
self.workflow_populator = WorkflowPopulator(self.galaxy_interactor)

# Create a simple workflow
workflow_id = self.workflow_populator.simple_workflow("Test Workflow")

# Upload workflow from YAML
workflow_id = self.workflow_populator.upload_yaml_workflow("""
class: GalaxyWorkflow
inputs:
  input1: data
steps:
  step1:
    tool_id: cat1
    in:
      input1: input1
""")

# Wait for invocation
self.workflow_populator.wait_for_invocation(workflow_id, invocation_id)
```


`WorkflowPopulator` handles workflow creation and execution. Use
`simple_workflow()` for basic tests or `upload_yaml_workflow()` with
Format2 YAML for more complex workflows. The populator also provides
methods to invoke workflows and wait for their completion.


## DatasetCollectionPopulator

```python
self.dataset_collection_populator = DatasetCollectionPopulator(
    self.galaxy_interactor
)

# Create a list collection
hdca = self.dataset_collection_populator.create_list_in_history(
    history_id,
    contents=["data1", "data2", "data3"],
    wait=True
)

# Create a paired collection
pair = self.dataset_collection_populator.create_pair_in_history(
    history_id,
    contents=[("forward", "ACGT"), ("reverse", "TGCA")],
    wait=True
)

# Create nested collections (list:paired)
identifiers = self.dataset_collection_populator.nested_collection_identifiers(
    history_id, "list:paired"
)
```


`DatasetCollectionPopulator` creates dataset collections for testing
collection-aware tools and workflows. It supports lists, pairs, and
nested structures like `list:paired`. The `contents` parameter can
be simple strings or tuples for paired data.


## API Test Assertions

```python
from galaxy_test.base.api_asserts import (
    assert_status_code_is,
    assert_status_code_is_ok,
    assert_has_keys,
    assert_error_code_is,
    assert_error_message_contains,
)

# Check HTTP status codes
response = self._get("histories")
assert_status_code_is(response, 200)
assert_status_code_is_ok(response)  # Any 2XX

# Check response structure
data = response.json()
assert_has_keys(data[0], "id", "name", "state")

# Check Galaxy error codes
assert_error_code_is(response, error_codes.USER_REQUEST_INVALID_PARAMETER)
assert_error_message_contains(response, "required field")
```


The `api_asserts` module provides assertion helpers for common API
test patterns. These give better error messages than plain asserts.
The test class also provides wrapper methods like
`self._assert_status_code_is()` for convenience.


## Test Decorators

```python
from galaxy_test.base.decorators import (
    requires_admin,
    requires_new_user,
    requires_new_history,
)
from galaxy_test.base.populators import skip_without_tool

class TestMyApi(ApiTestCase):
    @requires_admin
    def test_admin_only_endpoint(self):
        # Test runs only with admin user
        ...

    @requires_new_user
    def test_fresh_user(self):
        # Creates new user for test isolation
        ...

    @skip_without_tool("cat1")
    def test_cat_tool(self):
        # Skips if cat1 tool not installed
        ...
```


Decorators provide conditional test execution. `@requires_admin` ensures
the test runs as an admin user. `@requires_new_user` creates a fresh user
for isolation. `@skip_without_tool` skips tests when required tools aren't
available (useful for tests that depend on specific tool installations).


## Context Managers

**User switching:**
```python
def test_permissions(self):
    # Create resource as default user
    history_id = self.dataset_populator.new_history()

    # Test access as different user
    with self._different_user("other@example.com"):
        response = self._get(f"histories/{history_id}")
        self._assert_status_code_is(response, 403)

    # Test anonymous access
    with self._different_user(anon=True):
        response = self._get("histories")
        # Verify anonymous behavior
```


Context managers enable testing with different user contexts within
the same test. Use `_different_user()` to verify permission checks
and access controls. The `anon=True` parameter tests unauthenticated
access.


## Async & Celery

```python
# Wait for history jobs to complete
self.dataset_populator.wait_for_history(history_id, assert_ok=True)

# Wait for specific job
job_id = result["jobs"][0]["id"]
self.dataset_populator.wait_for_job(job_id, assert_ok=True)

# Wait for workflow invocation
self.workflow_populator.wait_for_invocation(workflow_id, invocation_id)

# Wait for async task (Celery)
self.dataset_populator.wait_on_task(async_response)
```

`ApiTestCase` includes `UsesCeleryTasks` - Celery is auto-configured.


Galaxy uses Celery for background tasks. Many operations (tool execution,
exports) return immediately with a task that must be awaited. The populator
wait methods handle polling and timeout logic. `ApiTestCase` automatically
configures Celery for testing.


## API Test CI

**CI Platform:** GitHub Actions

**Workflow:** `.github/workflows/api.yaml`

**Characteristics:**
- Fairly stable, rarely flaky
- Split into chunks for parallelization
- Uses PostgreSQL (not SQLite)
- Runs on every PR

Failures usually indicate real issues with your changes.


API tests run on every pull request via GitHub Actions. The test suite
is split into chunks that run in parallel for faster feedback. Unlike
some other test suites, API tests are quite stable and failures typically
indicate actual problems with the code under test.


## Integration Tests Overview

**Location:** `test/integration/`

**When to use instead of API tests:**
- Need custom Galaxy configuration
- Need direct database access
- Need Galaxy app internals (`self._app`)

**Trade-off:** Each test class spins up its own Galaxy server (slower)

**Run:** `./run_tests.sh -integration`


Integration tests have more power than API tests - they control Galaxy's
configuration and access internals. However, this comes at a cost: each
test case spins up its own Galaxy server, making them slower. API tests
are generally preferred; use integration tests only when an API test
won't work.


## Example: test_quota.py

```python
from galaxy_test.base.populators import DatasetPopulator
from galaxy_test.driver import integration_util

class TestQuotaIntegration(integration_util.IntegrationTestCase):
    dataset_populator: DatasetPopulator
    require_admin_user = True

    @classmethod
    def handle_galaxy_config_kwds(cls, config):
        super().handle_galaxy_config_kwds(config)
        config["enable_quotas"] = True

    def setUp(self):
        super().setUp()
        self.dataset_populator = DatasetPopulator(self.galaxy_interactor)

    def test_create(self):
        # ... test quota API
```


This example shows the key integration test patterns: inherit from
`IntegrationTestCase`, override `handle_galaxy_config_kwds` to modify
configuration, and use class attributes like `require_admin_user`.
The test has full access to populators and HTTP methods just like API tests.


## Class Attributes

```python
class TestMyFeature(integration_util.IntegrationTestCase):
    # Require the default API user to be an admin
    require_admin_user = True

    # Include Galaxy's sample tools and datatypes
    framework_tool_and_types = True
```

| Attribute | Default | Purpose |
|-----------|---------|---------|
| `require_admin_user` | False | API user must be admin |
| `framework_tool_and_types` | False | Include sample tools/datatypes |


Class attributes control test setup. `require_admin_user` ensures the
test user has admin privileges. `framework_tool_and_types` loads the
sample tools and datatypes used by framework tests, useful when your
integration test needs to run tools.


## Direct Config Options

The simplest pattern - set config values directly:

```python
@classmethod
def handle_galaxy_config_kwds(cls, config):
    super().handle_galaxy_config_kwds(config)
    config["enable_quotas"] = True
    config["metadata_strategy"] = "extended"
    config["allow_path_paste"] = True
    config["ftp_upload_dir"] = "/tmp/ftp"
```

The `config` dict corresponds to `galaxy.yml` options.


The `handle_galaxy_config_kwds` class method receives the Galaxy
configuration dictionary before the server starts. You can set any
option that would normally go in `galaxy.yml`. Always call
`super().handle_galaxy_config_kwds(config)` first to preserve
base configuration.


## External Config Files

For complex configs (job runners, object stores), use external files:

```python
import os
SCRIPT_DIRECTORY = os.path.dirname(__file__)
JOB_CONFIG_FILE = os.path.join(SCRIPT_DIRECTORY, "my_job_conf.yml")

class TestCustomRunner(integration_util.IntegrationTestCase):
    @classmethod
    def handle_galaxy_config_kwds(cls, config):
        super().handle_galaxy_config_kwds(config)
        config["job_config_file"] = JOB_CONFIG_FILE
```

Common: `job_config_file`, `object_store_config_file`, `file_sources_config_file`


Complex configurations like job runners and object stores are easier
to maintain as separate YAML or XML files. Point to them with the
appropriate config option. Store these config files alongside your
test file in the `test/integration/` directory.


## Dynamic Config Templates

For configs needing runtime values (temp dirs, ports):

```python
import string

OBJECT_STORE_TEMPLATE = string.Template("""
<object_store type="disk">
    <files_dir path="${temp_directory}/files"/>
</object_store>
""")

@classmethod
def handle_galaxy_config_kwds(cls, config):
    super().handle_galaxy_config_kwds(config)
    temp_dir = cls._test_driver.mkdtemp()
    config_content = OBJECT_STORE_TEMPLATE.safe_substitute(
        temp_directory=temp_dir
    )
    config_path = os.path.join(temp_dir, "object_store_conf.xml")
    with open(config_path, "w") as f:
        f.write(config_content)
    config["object_store_config_file"] = config_path
```


When your config needs runtime values like temporary directories or
dynamically allocated ports, use `string.Template` to substitute values.
Use `cls._test_driver.mkdtemp()` to get a managed temporary directory
that's cleaned up after tests.


## Configuration Mixins

Mixin classes simplify common configuration patterns:

```python
class TestWithObjectStore(
    integration_util.ConfiguresObjectStores,
    integration_util.IntegrationTestCase
):
    @classmethod
    def handle_galaxy_config_kwds(cls, config):
        cls._configure_object_store(STORE_TEMPLATE, config)
```

| Mixin | Purpose |
|-------|---------|
| `ConfiguresObjectStores` | Object store setup |
| `ConfiguresDatabaseVault` | Encrypted secrets |
| `PosixFileSourceSetup` | File upload sources |


Galaxy provides mixin classes for common configuration patterns. Use
multiple inheritance to compose capabilities. These mixins encapsulate
boilerplate configuration code, making tests more readable and reducing
duplication.


## Accessing Galaxy Internals

Integration tests can access Galaxy's app object via `self._app`:

```python
from galaxy.model import StoredWorkflow
from sqlalchemy import select

def test_workflow_storage(self):
    # Query database directly
    stmt = select(StoredWorkflow).order_by(StoredWorkflow.id.desc())
    workflow = self._app.model.session.execute(stmt).scalar_one()

    # Access application services
    table = self._app.tool_data_tables.get("all_fasta")

    # Get managed temp directory
    temp_dir = self._test_driver.mkdtemp()
```


Direct app access enables testing internal state not exposed via API.
You can query the database with SQLAlchemy, access tool data tables,
or inspect any Galaxy service. Use this sparingly - prefer API-based
assertions when possible as they're more representative of real usage.


## Skip Decorators & External Services

```python
from galaxy_test.driver import integration_util

@integration_util.skip_unless_docker()
def test_docker_feature(self):
    ...

@integration_util.skip_unless_kubernetes()
def test_k8s_feature(self):
    ...
```

| Decorator | Skips Unless |
|-----------|--------------|
| `skip_unless_docker()` | Docker available |
| `skip_unless_kubernetes()` | kubectl configured |
| `skip_unless_postgres()` | Using PostgreSQL |
| `skip_unless_amqp()` | AMQP URL configured |


Skip decorators allow tests to gracefully skip when required services
aren't available. CI provides PostgreSQL, RabbitMQ, Minikube, and
Apptainer. Some tests start their own Docker containers in setUpClass
and clean up in tearDownClass.


## Integration Test CI

**CI Platform:** GitHub Actions

**Workflow:** `.github/workflows/integration.yaml`

**CI provides:**
- PostgreSQL database
- RabbitMQ message queue
- Minikube (Kubernetes)
- Apptainer/Singularity

**Stability:** Moderately prone to flaky failures


Integration tests run on every pull request via GitHub Actions. The CI
environment provides external services like PostgreSQL and RabbitMQ.
This suite is more prone to transient failures than API tests. If you
see failures unrelated to your changes, request a re-run from the
Galaxy committers.


## Selenium Tests Overview

**Location:** `lib/galaxy_test/selenium/`

**What they test:**
- Full-stack UI with real browsers
- User workflows through the interface
- Visual correctness and accessibility

**Technologies:**
- Selenium WebDriver (browser automation)
- Smart component system (navigation.yml)

**Run:** `./run_tests.sh -selenium`


Selenium tests are full-stack tests that drive Galaxy's UI with real
browsers. They inherit all API test infrastructure, so you can use
populators for setup while testing actual UI interactions. These tests
are slower but catch issues that API tests miss.


## API vs UI Methods

**Use API methods** for setup (faster, more reliable):
```python
self.dataset_populator.new_dataset(self.history_id, content="data")
```

**Use UI methods** when testing the UI itself:
```python
self.perform_upload(self.get_filename("1.sam"))
```

| Scenario | Use | Method |
|----------|-----|--------|
| Need dataset for other test | API | `dataset_populator.new_dataset()` |
| Testing upload form | UI | `perform_upload()` |
| Need workflow for test | API | `workflow_populator.run_workflow()` |
| Testing workflow editor | UI | `workflow_run_open_workflow()` |


Selenium tests should use API methods for test setup and UI methods
only for what you're actually testing. This makes tests faster and
avoids false failures from unrelated UI bugs. If you're testing
dataset details, create the dataset via API, not through the upload form.


## Test Class Structure

```python
from .framework import (
    managed_history,
    selenium_test,
    SeleniumTestCase,
)

class TestMyFeature(SeleniumTestCase):
    ensure_registered = True  # Auto-login before each test

    @selenium_test
    @managed_history
    def test_something(self):
        self.perform_upload(self.get_filename("1.sam"))
        self.history_panel_wait_for_hid_ok(1)
```

| Attribute | Purpose |
|-----------|---------|
| `ensure_registered` | Auto-login before each test |
| `run_as_admin` | Login as admin user instead |


Selenium tests inherit from `SeleniumTestCase` which provides browser
automation plus all API test infrastructure. Set `ensure_registered = True`
to automatically login before each test. Use `run_as_admin = True` for
tests that need admin privileges.


## Test Decorators

```python
@selenium_test
@managed_history
def test_upload(self):
    ...
```

| Decorator | Purpose |
|-----------|---------|
| `@selenium_test` | **Required** - handles retries, debug dumps, accessibility |
| `@managed_history` | Creates isolated history, auto-cleanup |
| `@selenium_only(reason)` | Skip if using Playwright backend |
| `@playwright_only(reason)` | Skip if using Selenium backend |


The `@selenium_test` decorator is required for all Selenium tests. It
handles automatic retries (via `GALAXY_TEST_SELENIUM_RETRIES`), debug
dumps on failure, and baseline accessibility checks. Use `@managed_history`
to get an isolated history per test.


## Smart Component System

Access UI elements via `self.components` (defined in `navigation.yml`):

```python
# Access nested components
editor = self.components.workflow_editor
save_button = editor.save_button

# SmartTarget methods wait and interact
save_button.wait_for_visible()
save_button.wait_for_and_click()
save_button.assert_disabled()

# Parameterized selectors
self.components.history_panel.item(hid=1).wait_for_visible()
```


The smart component system wraps UI selectors with driver-aware methods.
Components are defined in `client/src/utils/navigation/navigation.yml`
and accessed via `self.components`. This provides a clean API and
automatic waiting, reducing test flakiness.


## SmartTarget Methods

| Method | Purpose |
|--------|---------|
| `wait_for_visible()` | Wait for visibility, return element |
| `wait_for_and_click()` | Wait then click |
| `wait_for_text()` | Wait, return `.text` |
| `wait_for_value()` | Wait, return input value |
| `wait_for_absent_or_hidden()` | Wait for element to disappear |
| `assert_absent_or_hidden()` | Fail if element visible |
| `assert_disabled()` | Verify disabled state |
| `all()` | Return list of all matching elements |


SmartTarget methods handle the common pattern of waiting for an element
and then interacting with it. They include built-in timeouts and retry
logic, making tests more reliable than raw Selenium calls.


## History & Workflow Operations

**File uploads:**
```python
self.perform_upload(self.get_filename("1.sam"))
self.perform_upload(self.get_filename("1.sam"), ext="txt", genome="hg18")
```

**History panel:**
```python
self.history_panel_wait_for_hid_ok(1)
self.history_panel_click_item_title(hid=1)
self.wait_for_history()
```

**Workflows (via `RunsWorkflows` mixin):**
```python
self.workflow_run_open_workflow(WORKFLOW_YAML)
self.workflow_run_submit()
self.workflow_run_wait_for_ok(hid=2)
```


The test framework provides specialized methods for common Galaxy
operations. File uploads, history panel interactions, and workflow
execution all have dedicated helper methods that handle waiting and
error checking.


## Accessibility Testing

`@selenium_test` automatically runs [axe-core](https://www.deque.com/axe/) accessibility checks.

**Component-level checks:**
```python
login = self.components.login
login.form.assert_no_axe_violations_with_impact_of_at_least("moderate")

# With known violations excluded
EXCEPTIONS = ["heading-order", "label"]
self.components.history_panel._.assert_no_axe_violations_with_impact_of_at_least(
    "moderate", EXCEPTIONS
)
```

**Impact levels:** `"minor"`, `"moderate"`, `"serious"`, `"critical"`


Galaxy's Selenium tests include automatic accessibility testing using
axe-core. The `@selenium_test` decorator runs baseline checks, and you
can add component-level assertions with specific impact thresholds.
This helps ensure Galaxy remains accessible to all users.


## Shared State Tests

For expensive one-time setup, use `SharedStateSeleniumTestCase`:

```python
class TestPublishedPages(SharedStateSeleniumTestCase):
    @selenium_test
    def test_index(self):
        self.navigate_to_pages()
        # ... test using shared state

    def setup_shared_state(self):
        # Called once before first test in class
        self.user1_email = self._get_random_email("test1")
        self.register(self.user1_email)
        self.new_public_page()
        self.logout_if_needed()
```


`SharedStateSeleniumTestCase` runs `setup_shared_state()` once per class
rather than per test. Use this for expensive setup like creating multiple
users or published resources. State persists across all test methods
in the class.


## Selenium Test CI

**CI Platform:** GitHub Actions

**Workflow:** `.github/workflows/selenium.yaml`

**Features:**
- Split into 3 chunks for parallelization
- Auto-retry on failure (`GALAXY_TEST_SELENIUM_RETRIES=1`)
- Debug artifacts uploaded on failure
- PostgreSQL backend

**Stability:** More prone to flaky failures than API tests


Selenium tests run on every pull request via GitHub Actions. The CI
automatically retries failed tests once and uploads debug artifacts
(screenshots, HTML dumps) on failure. These tests are more prone to
transient failures; request a re-run if failures seem unrelated.


## Playwright Tests

**Same test files** as Selenium (`lib/galaxy_test/selenium/`)

**Why Playwright?**
- Faster execution
- Better reliability
- Modern browser automation

**Run:**
```bash
./run_tests.sh -playwright
```

**Install browser:**
```bash
playwright install chromium --with-deps
```


Playwright is a modern alternative to Selenium that uses the same test
files. Tests work with both backends; use `@selenium_only` or
`@playwright_only` decorators for backend-specific tests. Playwright
tends to be faster and more reliable.


## Playwright CI

**CI Platform:** GitHub Actions

**Workflow:** `.github/workflows/playwright.yaml`

**Differences from Selenium CI:**
- Installs Playwright via `playwright install chromium`
- Uses headless mode (`GALAXY_TEST_SELENIUM_HEADLESS=1`)
- Same test splitting (3 chunks)

Both Selenium and Playwright CI run on every PR.


Playwright tests run in a separate CI workflow from Selenium tests.
This provides redundancy and helps catch browser-specific issues.
Both workflows run on every pull request, testing the same code with
different browser automation backends.


## Selenium Integration Tests

**Location:** `test/integration_selenium/`

**Combines:**
- Selenium browser automation
- Integration test config hooks (`handle_galaxy_config_kwds`)

**When to use:**
- UI testing that needs custom Galaxy configuration
- Testing UI features behind config flags

**Run:** `./run_tests.sh -integration test/integration_selenium`


Selenium Integration tests combine browser automation with integration
test capabilities. Use them when you need to test UI behavior with
custom Galaxy configuration - for example, testing an admin feature
that requires specific config options enabled.


## Selenium Integration CI

**Example:** `test/integration_selenium/test_upload_ftp.py`
- Tests FTP upload UI
- Requires `ftp_upload_dir` configuration

**CI Platform:** GitHub Actions

**Workflow:** `.github/workflows/integration_selenium.yaml`

Runs on every PR, similar stability to regular Selenium tests.


Selenium Integration tests have their own CI workflow. Like regular
Selenium tests, they can be flaky due to browser timing issues. The
CI uploads debug artifacts on failure to help diagnose issues.


## Handling Flaky Tests

Some tests fail intermittently due to:
- Race conditions
- Timing issues
- External dependencies

**Galaxy's approach:**
- Track via GitHub issues with `transient-test-error` label
- Mark tests with `@transient_failure` decorator
- Modified error messages help reviewers identify non-blocking failures


Flaky tests are tests that sometimes pass and sometimes fail without
code changes. Galaxy provides infrastructure to track and manage these
tests so they don't block legitimate pull requests while still
maintaining visibility into the underlying issues.


## @transient_failure Decorator

```python
from galaxy.util.unittest_utils import transient_failure

@transient_failure(issue=21224)
@selenium_test
def test_sharing_private_history(self):
    # Test that sometimes fails due to race condition
    ...
```

**Parameters:**
- `issue` - GitHub issue number tracking this failure
- `potentially_fixed=True` - Indicates fix was implemented

When test fails, error message includes issue link and tracking info.


The `@transient_failure` decorator wraps test failures with additional
context linking to a tracking issue. This helps CI reviewers quickly
identify known flaky tests vs. real failures.


## Flaky Test Workflow

1. **Identify** - Test fails intermittently in CI
2. **Track** - Create GitHub issue with `transient-test-error` label
3. **Mark** - Add `@transient_failure(issue=XXXXX)` decorator
4. **Fix** - When implemented, set `potentially_fixed=True`

```python
@transient_failure(issue=21242, potentially_fixed=True)
def test_delete_job_with_message(self, history_id):
    ...
```

5. **Close** - If no failures for ~1 month, remove decorator and close issue


The workflow ensures flaky tests are tracked and eventually fixed rather
than being ignored. The `potentially_fixed` flag triggers reviewers to
report any subsequent failures, helping determine if fixes are effective.


## Running Tests Reference

**Quick reference:**
```bash
./run_tests.sh --help          # Full documentation

# Common patterns
./run_tests.sh -unit           # Python unit tests
./run_tests.sh -api            # API tests
./run_tests.sh -integration    # Integration tests
./run_tests.sh -selenium       # Selenium tests
./run_tests.sh -framework      # Tool framework tests
```

**Client tests:**
```bash
make client-test               # All client tests
yarn --cwd client test:watch   # Watch mode
```


The `run_tests.sh` script is the primary entry point for running Galaxy's
test suites. Use `--help` for complete documentation including all flags,
environment variables, and test selection options.


## Key Takeaways
- Unit tests for isolated components (no server needed)
- API tests for backend behavior via Galaxy API
- Integration tests for custom Galaxy configurations
- Framework tests for tool/workflow XML validation
- Selenium/Playwright tests for UI with browser automation
- Populators simplify test data creation
- Each test type has a dedicated CI workflow
