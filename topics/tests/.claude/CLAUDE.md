# Galaxy Testing Infrastructure - Claude Context

You are an expert on Galaxy's testing infrastructure, covering unit tests, API tests, integration tests, and browser automation.

## Core Concepts

- **Unit tests** for isolated components (no running server needed)
- **API tests** use populators to create test data and hit Galaxy API
- **Integration tests** for custom Galaxy configurations
- **Framework tests** for tool/workflow XML validation
- **Selenium/Playwright tests** for browser-based UI testing
- **Decision tree** guides developers to the right test type

## Key Files to Reference

Unit Tests:
- `test/unit/` - Python unit tests
- `client/src/` - Client unit tests (Vitest)
- `test/unit/tool_util/` - External dependency tests

API Tests:
- `lib/galaxy_test/api/` - API test implementations
- `lib/galaxy_test/api/_framework.py` - ApiTestCase base class
- `lib/galaxy_test/base/populators.py` - DatasetPopulator, WorkflowPopulator
- `lib/galaxy_test/base/api_asserts.py` - Assertion helpers

Integration Tests:
- `test/integration/` - Integration test implementations
- `lib/galaxy_test/driver/integration_util.py` - IntegrationTestCase base class

Browser Tests:
- `lib/galaxy_test/selenium/` - Selenium/Playwright tests
- `lib/galaxy_test/selenium/framework.py` - SeleniumTestCase
- `client/src/utils/navigation/navigation.yml` - Component selectors

Framework Tests:
- `test/functional/tools/` - Tool framework tests
- `lib/galaxy_test/workflow/` - Workflow framework tests

CI Workflows:
- `.github/workflows/api.yaml`
- `.github/workflows/integration.yaml`
- `.github/workflows/selenium.yaml`
- `.github/workflows/playwright.yaml`

## Test Type Decision Tree

```
Does test need running Galaxy server?
├─ NO → Unit test
│       ├─ Python? → test/unit/ (pytest)
│       └─ Client? → client/src/ (Vitest)
└─ YES → Functional test
         Does test need web browser?
         ├─ NO → Does test need custom config?
         │       ├─ NO → API test
         │       └─ YES → Integration test
         └─ YES → Selenium/Playwright test
```

## Populator Pattern

```python
# DatasetPopulator - most commonly used
self.dataset_populator = DatasetPopulator(self.galaxy_interactor)
history_id = self.dataset_populator.new_history()
hda = self.dataset_populator.new_dataset(history_id, content="data")
self.dataset_populator.wait_for_history(history_id)

# WorkflowPopulator
workflow_id = self.workflow_populator.upload_yaml_workflow(yaml)

# DatasetCollectionPopulator
hdca = self.dataset_collection_populator.create_list_in_history(history_id, contents=[...])
```

## API Test Pattern

```python
from galaxy_test.base.populators import DatasetPopulator
from ._framework import ApiTestCase

class TestMyFeature(ApiTestCase):
    dataset_populator: DatasetPopulator

    def setUp(self):
        super().setUp()
        self.dataset_populator = DatasetPopulator(self.galaxy_interactor)

    def test_something(self):
        history_id = self.dataset_populator.new_history()
        response = self._get(f"histories/{history_id}")
        self._assert_status_code_is(response, 200)
```

## Integration Test Pattern

```python
from galaxy_test.driver import integration_util

class TestWithConfig(integration_util.IntegrationTestCase):
    require_admin_user = True

    @classmethod
    def handle_galaxy_config_kwds(cls, config):
        super().handle_galaxy_config_kwds(config)
        config["enable_quotas"] = True
```

## Selenium Test Pattern

```python
from .framework import managed_history, selenium_test, SeleniumTestCase

class TestUI(SeleniumTestCase):
    @selenium_test
    @managed_history
    def test_upload(self):
        self.perform_upload(self.get_filename("1.sam"))
        self.history_panel_wait_for_hid_ok(1)
        self.components.history_panel.item(hid=1).wait_for_visible()
```

## When Updating This Topic

1. **Verify examples** against current Galaxy codebase
2. **Check** if new test types or patterns have been added
3. **Update** `related_code_paths` in metadata.yaml if new files are relevant
4. **Regenerate** all outputs: `make build`
5. **Run validation**: `make validate`

## Common Questions

**Q: Where should I put my test?**
A: Use the decision tree. Start with "Does test need running Galaxy server?"

**Q: API test vs integration test?**
A: API test for standard Galaxy config. Integration test when you need `handle_galaxy_config_kwds()`.

**Q: What are populators?**
A: Abstraction layer over Galaxy API that simplifies creating test fixtures.

**Q: Why is my integration test slow?**
A: Each integration test spins up a new Galaxy server. Consider if an API test would suffice.

**Q: How do I test Celery tasks?**
A: API tests include `UsesCeleryTasks` mixin automatically. Use `wait_on_task()` methods.

**Q: How do I mock in unit tests?**
A: Use pytest fixtures and standard mocking. No special Galaxy infrastructure needed.

## Related Topics

- **project-management** - CI/CD overview
- **dependency-injection** - DI patterns used in test fixtures
- **application-components** - What gets tested
- **frameworks** - FastAPI/WSGI patterns in API tests

## Diagram Opportunities

- Decision tree flowchart (Mermaid)
- Test infrastructure architecture (sequence or component diagram)
- CI workflow relationship to test types
