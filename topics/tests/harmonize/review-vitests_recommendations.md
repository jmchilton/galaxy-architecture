# Harmonization Recommendations: review-vitests

## Context Clarification

- **Static command** (`review/static_commands/gx-vitest-review.md`) - hand-written, 158 lines
- **Generated command** (`generated_agentic_operations/commands/tests-review-vitests.md`) - from docs, 295 lines
- **The TODO in metadata.yaml prompt IS working** - the generator properly synthesizes from the referenced content blocks

The question: Is the generated command good enough to replace the static one?

**Answer: Yes, the generated command is better.** It includes:
- Galaxy-specific infrastructure (LocalVue, MSW, test factories)
- related_code_paths section
- All the anti-patterns and verification techniques
- AI-generated test guidelines

## Documentation Improvements

To make the generated command even better (and cover what the static command has):

1. **Add Options API testing guidance**
   - Static command has explicit "Test Options API Components" section
   - content.yaml doesn't have this - only mentions avoiding `wrapper.vm` briefly
   - **Add prose or agent-context block**: `es6-options-api-testing` covering:
     - Don't access `wrapper.vm` directly
     - Test through template interactions
     - Options API vs Composition API testing differences

2. **Consider adding "test verification workflow" to agent-context**
   - `es6-test-verification` has techniques but no step-by-step workflow
   - Could add: "Pick 2-3 tests and: 1) comment out impl, 2) verify test fails, 3) report if it doesn't"

3. **Add "when NOT to write a test" guidance**
   - Neither command covers this well
   - Consider agent-context block for: framework code, trivial getters, tests that only test mocks

## Prompt Improvements

The prompt in metadata.yaml is already good - it has the TODO marker that the generator honors. Minor improvements:

1. **Add instruction to include related_code_paths**

   Add after the TODO:
   ```
   Include a "Related Code Paths" section listing client-testing paths from metadata.yaml.
   ```

2. **Add output structure guidance** (optional)

   Could add:
   ```
   Structure with sections: Input formats, Persona, Actions, Code paths, Best practices, Red flags, Verification, AI guidelines, Infrastructure, Running tests.
   ```

3. **Clarify Composition vs Options API coverage**

   In the TODO, add `es6-options-api-testing` once that block exists in content.yaml.

## Action Items

1. ✅ **Use generated command** - it's better than static
2. 📝 **Add Options API block to content.yaml** - single gap in generated output
3. 📝 **Update prompt** to mention related_code_paths explicitly
4. 🗑️ **Retire static command** once docs are complete

## One-liner Summary

Generated command wins - add Options API testing content to docs, then retire the static command.
