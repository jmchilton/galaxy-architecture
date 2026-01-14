# Improvement Suggestions for `review-di` Operation

Suggestions for enhancing content.yaml to make the `review-di` code review operation more effective.

## Content Gaps Identified

### 1. Missing: Common Migration Patterns

**Problem:** The content shows before/after examples but lacks systematic migration patterns for common scenarios.

**Suggestion:** Add a slide or prose block covering:
- Step-by-step migration from `app.manager` access to injected dependency
- How to identify which dependencies to extract from `app` usage
- Order of operations when refactoring multiple dependent managers

### 2. Missing: Anti-pattern Catalog

**Problem:** The content implicitly shows anti-patterns but doesn't catalog them explicitly.

**Suggestion:** Add content block listing common DI anti-patterns:
- Service locator pattern (asking container for dependencies at runtime)
- Property injection vs constructor injection trade-offs
- Mixing DI styles (some deps injected, some from `app`)
- Partial migration states and their risks

### 3. Missing: Testing Implications

**Problem:** Slide `testing_problems` mentions testing is difficult, `design_benefits_di` mentions unit testing, but no concrete testing examples.

**Suggestion:** Add content showing:
- Before/after test code comparing `app` mocking vs DI mocking
- How to set up test fixtures with Lagom container
- Mock injection patterns for unit tests

### 4. Missing: Container Registration

**Problem:** Content shows consumption of DI but not registration side.

**Suggestion:** Add content covering:
- How to register new types with Galaxy's container
- When singletons vs transients are appropriate
- Location of container configuration in codebase

### 5. Missing: Error Messages and Debugging

**Problem:** No content about what happens when DI goes wrong.

**Suggestion:** Add content about:
- Common Lagom error messages and their meaning
- How to debug circular dependency errors
- Type mismatch resolution

## Specific Content Additions

### Add: `depends()` vs `Depends()` Detailed Comparison

The slide `di_fastapi_limitations` could be expanded with:
- Why Galaxy created its own `depends()` function
- Internal implementation differences
- When (if ever) to use FastAPI's `Depends()`

### Add: Interface Design Guidelines

Expand on `why_interface` slide:
- When to create a new interface vs use existing
- Interface segregation principle applied to Galaxy
- `StructuredApp` vs specialized interfaces (when to use which)

### Add: Real-world Refactoring Case Study

Add narrative content showing:
- Actual PR that migrated a component to DI
- Problems encountered during migration
- Final outcome and lessons learned

## Priority Ranking

1. **High:** Anti-pattern catalog - directly supports review task
2. **High:** Container registration - reviewers need to know proper registration
3. **Medium:** Migration patterns - helps when suggesting fixes
4. **Medium:** Testing implications - validates correct DI usage
5. **Low:** Error messages - useful but less common in reviews
