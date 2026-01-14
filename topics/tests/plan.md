# Slide Plan for Galaxy Testing Infrastructure

Source: `/Users/jxc755/projects/worktrees/galaxy/branch/writing-tests-docs/doc/source/dev/writing_tests.md`

## Section 1: Introduction & Overview (5 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 1 | title | **Title: Writing Tests for Galaxy** | Motivation, why testing matters |
| 2 | other-resources | **Other Resources** | run_tests.sh --help, GTN tutorial, client/README.md links |
| 3 | quick-reference | **Quick Reference Table** | Test type summary table - copy from doc |
| 4 | decision-tree | **Decision Tree** | Mermaid flowchart - KEY visual, center of this topic |
| 5 | decision-walkthrough | **Decision Tree Walkthrough** | Text explanation of the branches |

## Section 2: Python Unit Tests (4 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 6 | python-unit | **Python Unit Tests** | Location test/unit/, pytest, when to use |
| 7 | doctests | **Doctests Guidance** | When doctests OK vs standalone - brief |
| 8 | external-deps | **External Dependency Tests** | @external_dependency_management marker, tox -e mulled |
| 9 | python-unit-ci | **Python Unit Test CI** | CircleCI |

## Section 3: Frontend/ES6 Unit Tests (12 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 10 | es6-overview | **Frontend Unit Tests** | Vitest, Vue Test Utils, MSW |
| 11 | es6-test-structure | **Test File Structure** | *.test.ts placement, standard imports |
| 12 | es6-localvue | **Galaxy Testing Infrastructure** | getLocalVue(), test data factories, suppressing warnings |
| 13 | es6-msw | **API Mocking with MSW** | useServerMock(), OpenAPI-MSW, type-safe handlers |
| 14 | es6-shallow-mount | **shallowMount vs mount** | Prefer shallowMount, Selenium for integration |
| 15 | es6-mount-wrapper | **Mount Wrapper Factories** | Reusable factory functions for complex setup |
| 16 | es6-selectors | **Selector Constants & Events** | SELECTORS pattern, wrapper.emitted() |
| 17 | es6-pinia | **Pinia Store Testing** | createTestingPinia, isolated store tests |
| 18 | es6-async | **Async Operations** | flushPromises(), nextTick() |
| 19 | es6-best-practices | **Testing Best Practices** | 7 key practices summary |
| 20 | es6-running-tests | **Running Client Tests** | make client-test, yarn test:watch |
| 21 | es6-ci | **Client Test CI** | GitHub Actions, linting |

## Section 4: Framework Tests (5 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 22 | tool-framework | **Tool Framework Tests Overview** | What, why, when - test/functional/tools/ |
| 23 | adding-tool-test | **Adding a Tool Test** | sample_tool_conf.xml, adding test blocks |
| 24 | workflow-framework | **Workflow Framework Tests** | Format2 YAML, test definition files |
| 25 | workflow-example | **Workflow Framework Example** | Show .gxwf.yml + .gxwf-tests.yml pair |
| 26 | framework-ci | **Framework Test CI** | framework_tools.yaml, framework_workflows.yaml |

## Section 5: API Tests (13 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 27 | api-overview | **API Tests Overview** | What they test, lib/galaxy_test/api/ |
| 28 | api-class-structure | **Test Class Structure** | ApiTestCase inheritance diagram, setUp pattern |
| 29 | http-methods | **HTTP Methods** | _get, _post, _put, _patch, _delete, admin param |
| 30 | populators-concept | **Populators Concept** | What they are, why use them vs raw requests |
| 31 | dataset-populator | **DatasetPopulator** | new_history, new_dataset, run_tool, wait_for_history |
| 32 | dataset-populator-advanced | **DatasetPopulator Advanced** | get_history_dataset_content options, _raw pattern |
| 33 | workflow-populator | **WorkflowPopulator** | simple_workflow, upload_yaml_workflow |
| 34 | collection-populator | **DatasetCollectionPopulator** | create_list_in_history, pairs, nested |
| 35 | api-assertions | **API Test Assertions** | api_asserts module, status codes, error codes |
| 36 | api-decorators | **Test Decorators** | requires_admin, requires_new_user, skip_without_tool |
| 37 | context-managers | **Context Managers** | _different_user(), anonymous access testing |
| 38 | async-celery | **Async & Celery** | wait_for_history, wait_for_job, wait_on_task |
| 39 | api-ci | **API Test CI** | api.yaml workflow |

## Section 6: Integration Tests (10 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 40 | integration-overview | **Integration Tests Overview** | When vs API tests, handle_galaxy_config_kwds |
| 41 | integration-example | **Example: test_quota.py** | IntegrationTestCase, require_admin_user |
| 42 | integration-attrs | **Class Attributes** | require_admin_user, framework_tool_and_types |
| 43 | config-direct | **Direct Config Options** | Setting config dict values |
| 44 | config-files | **External Config Files** | job_config_file, object_store_config_file |
| 45 | config-templates | **Dynamic Config Templates** | string.Template pattern |
| 46 | config-mixins | **Configuration Mixins** | ConfiguresObjectStores, PosixFileSourceSetup |
| 47 | galaxy-internals | **Accessing Galaxy Internals** | self._app, database queries, vault |
| 48 | skip-decorators | **Skip Decorators & External Services** | skip_unless_docker, CI-provided services |
| 49 | integration-ci | **Integration Test CI** | integration.yaml workflow |

## Section 7: Selenium Tests (10 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 50 | selenium-overview | **Selenium Tests Overview** | Full stack UI testing, lib/galaxy_test/selenium |
| 51 | api-vs-ui | **API vs UI Methods** | Decision table - when to use which |
| 52 | selenium-class | **Test Class Structure** | SeleniumTestCase, ensure_registered |
| 53 | selenium-decorators | **Test Decorators** | @selenium_test, @managed_history, @selenium_only |
| 54 | smart-components | **Smart Component System** | self.components hierarchy, navigation.yml |
| 55 | smart-target | **SmartTarget Methods** | wait_for_visible, wait_for_and_click, etc. |
| 56 | history-workflow-ops | **History & Workflow Operations** | perform_upload, history_panel_*, RunsWorkflows |
| 57 | accessibility | **Accessibility Testing** | axe-core integration, impact levels |
| 58 | shared-state | **Shared State Tests** | SharedStateSeleniumTestCase, setup_shared_state |
| 59 | selenium-ci | **Configuration & CI** | GALAXY_TEST_END_TO_END_CONFIG, selenium.yaml |

## Section 8: Playwright Tests (2 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 60 | playwright-overview | **Playwright Overview** | Same test files, faster execution |
| 61 | playwright-ci | **Running & CI** | playwright install, playwright.yaml |

## Section 9: Selenium Integration Tests (2 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 62 | selenium-integration | **Selenium Integration Overview** | Combines Selenium + Integration capabilities |
| 63 | selenium-integration-ci | **Example & CI** | test_upload_ftp.py, integration_selenium.yaml |

## Section 10: Flaky Tests (3 slides) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 64 | flaky-overview | **Handling Flaky Tests** | transient-test-error label workflow |
| 65 | transient-failure | **@transient_failure Decorator** | issue param, potentially_fixed |
| 66 | flaky-workflow | **Flaky Test Workflow** | Create issue -> decorate -> fix -> monitor |

## Section 11: Running Tests (1 slide) ✓ DONE

| # | ID | Topic | Notes |
|---|-----|-------|-------|
| 67 | run-tests | **run_tests.sh Reference** | Point to --help, common options |

---

## Summary

| Section | Slide Count | Status |
|---------|-------------|--------|
| Introduction & Overview | 5 | ✓ DONE |
| Python Unit Tests | 4 | ✓ DONE |
| Frontend/ES6 Unit Tests | 12 | ✓ DONE |
| Framework Tests | 5 | ✓ DONE |
| API Tests | 13 | ✓ DONE |
| Integration Tests | 10 | ✓ DONE |
| Selenium Tests | 10 | ✓ DONE |
| Playwright Tests | 2 | ✓ DONE |
| Selenium Integration | 2 | ✓ DONE |
| Flaky Tests | 3 | ✓ DONE |
| Running Tests | 1 | ✓ DONE |
| **Total** | **67 slides** | ✓ COMPLETE |

---

## Diagrams Needed

1. **Decision Tree Flowchart** (Mermaid) - slide 4 - `../../images/tests-decision-tree.mermaid.svg` ✓ DONE
2. **Populator Relationships** (class diagram) - slide 30
3. **Smart Component Hierarchy** (mindmap or tree) - slide 54

---

## Unresolved Questions

- Combine all CI slides into one summary or keep per-section?
- Jupyter+Selenium section worth a slide or skip (specialized)?
- Include run_tests_help.txt content or just reference?
- Depth on Celery/async - 1 slide or 2?
