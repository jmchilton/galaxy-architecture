# Suggestions for Improving `review-vitests` Operation

## Content Gaps Identified

### 1. Options API vs Composition API Testing
The current content focuses on Composition API components. Consider adding a prose block with guidance for testing Options API components:
- When to avoid `wrapper.vm` in Options API tests
- Differences in testing patterns between the two API styles
- Migration considerations when moving from Options to Composition

### 2. Suppressing Warnings Pattern
While `suppressBootstrapVueWarnings()` is mentioned in the `es6-localvue` slide, it could be expanded in a prose block to cover:
- Other common warning suppression patterns
- When suppression is appropriate vs when it indicates a real issue
- Keeping warning suppression up to date

### 3. Testing Emitted Events
The `es6-selectors` slide includes event testing, but this could be a standalone agent-context block with more depth:
- Common patterns for testing v-model events
- Testing complex event payloads
- Verifying event ordering

### 4. More AI Anti-Pattern Examples
The `es6-ai-guidelines` block is valuable but could benefit from concrete code examples showing:
- Side-by-side comparison of AI-generated low-value test vs refactored high-value test
- Real-world examples from Galaxy codebase of tests that were improved

### 5. Mount vs ShallowMount Decision Tree
Currently guidance is "prefer shallowMount" but an agent-context block could add nuance:
- Specific scenarios where `mount` is necessary
- How to handle testing components that heavily depend on child behavior
- Strategies for avoiding `mount` when it seems required

## Prompt Improvements

The metadata.yaml prompt is well-structured. Suggestions for enhancement:

1. **Add explicit running guidance**: Include "Run individual tests with `yarn test:watch <pattern>`" in the main task instructions since debugging often requires isolating tests.

2. **Include Pinia testing pattern**: The prompt could specifically mention checking for proper Pinia store setup and state management in tests.

3. **Add verification requirement**: Explicitly state "For suspicious tests, verify they actually test something by commenting out implementation and confirming test failure."

## New Content Blocks to Consider

### agent-context: Vitest-Specific Patterns
```yaml
- type: agent-context
  id: es6-vitest-patterns
  heading: Vitest-Specific Patterns
  content: |
    Galaxy uses Vitest features that differ from Jest:
    - `vi.fn()` vs `jest.fn()`
    - `vi.mocked()` for type-safe mocking
    - Vitest's native ESM support
    - Snapshot testing differences
```

### agent-context: Component Testing Boundaries
```yaml
- type: agent-context
  id: es6-testing-boundaries
  heading: Component Testing Boundaries
  content: |
    Clear guidance on what to mock vs test directly:
    - Mock: API calls (via MSW), external services, timers
    - Don't mock: Vue reactivity, component props/events, computed properties
    - Gray area: Child components (prefer shallowMount), router
```

### prose: Test File Organization
Expand on the brief file structure mention with more detail about:
- When to create separate test-utils files
- Shared fixtures across multiple test files
- Test data organization strategies
