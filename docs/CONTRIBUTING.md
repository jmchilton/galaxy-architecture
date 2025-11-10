# Contributing Guide

## Adding a New Topic

1. **Choose a topic ID**
   - Lowercase, hyphenated (e.g., `plugin-system`)
   - Must be unique

2. **Create directory**
   ```bash
   mkdir -p topics/<topic-id>/.claude
   ```

3. **Create metadata.yaml**
   - Use another topic as template
   - Fill in all required fields
   - See docs/SCHEMA.md for details

4. **Write content**
   - Create overview.md at minimum
   - Additional .md files for subtopics
   - Use clear markdown headings

5. **Add Claude context**
   - Create .claude/CLAUDE.md
   - Explain what this topic covers
   - List relevant Galaxy code paths
   - Note how to update this topic

6. **Validate**
   ```bash
   uv run python scripts/validate.py
   ```

7. **Generate outputs**
   ```bash
   uv run python outputs/training-slides/build.py <topic-id>
   ```

8. **Commit**
   ```bash
   git add topics/<topic-id>
   git commit -m "Add <topic-id> documentation"
   ```

## Content Guidelines

### Markdown Style

- Use `##` for major sections (becomes slides)
- Use `###` for subsections
- Use `---` to force slide breaks
- Code blocks with language hints (e.g., ` ```python`)
- Use `{.code}` marker before code blocks for special formatting (converts to `.code[```...```]`)
- Use `class: reduce90` or `class: enlarge150` directives for layout classes
- Images: Use `![Alt text](../../images/file.svg)` format
- Diff format: Use ` ```diff` for showing code changes

### Example
```markdown
## What is Dependency Injection?

Pattern for managing dependencies.

???

Speaker note: Explain the difference between DI and service locator.

---

### Benefits

- Testability
- Loose coupling
- Flexibility
```

### Writing Style

- Clear and concise
- Assume intermediate Python knowledge
- Link to Galaxy code examples
- Prefer showing over telling

### Code Examples

- Use real Galaxy code when possible
- Keep examples short (< 20 lines)
- Include imports
- Add comments for clarity

## Updating Existing Topics

1. **Edit markdown files** in topics/<topic-id>/
2. **Update metadata.yaml** if needed
3. **Validate**: `uv run python scripts/validate.py`
4. **Regenerate outputs**: `/sync-slides <topic-id>`
5. **Commit with descriptive message**

## Testing Changes

Before committing:

1. **Validate**: `uv run python scripts/validate.py`
   - Checks metadata completeness
   - Validates content quality
   - Verifies images and links
   - Runs automatically in CI on push/PR

2. **Run tests**: `uv run pytest tests/ -v`
   - Unit tests for validation logic
   - Ensures validation rules work correctly

3. **Build slides**: `uv run python outputs/training-slides/build.py <topic-id>`
   - Generates GTN-compatible slides
   - Output: `outputs/training-slides/generated/architecture-<topic-id>/slides.html`

4. **Preview slides**: Open generated HTML in browser
   - Test navigation and formatting
   - Verify images display correctly
   - Check code blocks render properly

## Pull Request Process

1. Validate and build outputs locally
2. Include generated outputs if helpful for review
3. Describe what changed and why
4. Reference related Galaxy PRs if applicable

## Questions?

Open an issue or reach out to @jmchilton

