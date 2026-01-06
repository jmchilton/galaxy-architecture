# Code Path: lib/galaxy/managers/markdown_parse.py

## Role in Architecture

Lightweight, self-contained parser for Galaxy Flavored Markdown validation. Designed to be reusable in other projects (e.g., gxformat2) by avoiding Galaxy-specific dependencies.

## Core Responsibilities

**Single Purpose:** Validate and parse Galaxy Flavored Markdown by:
1. Recognizing Galaxy-specific directives within fenced code blocks
2. Validating directive syntax and arguments
3. Detecting embedded template directives in inline markdown
4. Reporting detailed validation errors with line numbers

## Directive Syntax

**Fenced Block Directives:**
```markdown
```galaxy
directive_name(arg1=value1, arg2=value2)
```
```

**Inline Embed Directives:**
```markdown
Text with ${galaxy history_dataset_name(invocation_id=ABC123)} embedded.
```

## Supported Directives

27 Galaxy directives with specific allowed arguments:

- **Dataset/History:** `history_dataset_as_image`, `history_dataset_as_table`, `history_dataset_display`, `history_dataset_info`, etc.
- **Workflow:** `workflow_display`, `workflow_image`, `workflow_license`
- **Job/Invocation:** `job_metrics`, `job_parameters`, `tool_stdout`, `tool_stderr`, `invocation_inputs`, `invocation_outputs`
- **Meta/System:** `generate_galaxy_version`, `generate_time`, `instance_*_link` (6 variants)

## Key Functions

### `validate_galaxy_markdown(galaxy_markdown, internal=True)`
Main entry point - validates entire markdown document.
- Returns None on success, raises ValueError with line number on failure
- Iterates line-by-line tracking fence state
- Distinguishes between fenced blocks and regular markdown
- Validates directive syntax and arguments

### `_split_markdown_lines(markdown)`
Generator that parses markdown structure without validation.
- Yields `(line, fenced, open_fence_this_iteration, line_number)` tuples
- Tracks block fences (```) and indent fences (4+ spaces)

### `_check_func_call(func_call_match, line_no)`
Validates directive arguments against allowed argument list.
- Extracts directive name from regex match
- Validates each argument name
- Skips validation for directives with DynamicArguments

## Design Patterns

**Separation of Concerns:**
- `markdown_parse.py` = pure parsing/validation (no Galaxy dependencies)
- `markdown_util.py` = Galaxy integration (loads objects, renders HTML)

**Fence Tracking State Machine:**
Handles edge cases like nested indentation, whitespace-only lines, multiple blocks.

**Fail-Fast Validation:**
- Raises on first invalid directive
- Reports precise line number (1-indexed)
- Enables early detection in CI/build pipelines

**Dynamic Argument Handling:**
Allows future directives to accept arbitrary arguments (like `visualization`).

## Regular Expression Patterns

- `GALAXY_FLAVORED_MARKDOWN_CONTAINER_LINE_PATTERN` - Matches opening ` ```galaxy ` lines
- `GALAXY_MARKDOWN_FUNCTION_CALL_LINE` - Matches `directive(arg=val, arg2=val2)`
- `EMBED_DIRECTIVE_REGEX` - Matches `${galaxy directive(...)}` in inline text
- `ARG_VAL_REGEX` - Matches unquoted IDs or quoted strings

## Documentation Highlights

**For training:**
- Explain directive syntax and validation rules
- Show examples of valid/invalid markdown
- Demonstrate error messages and how to fix
- Highlight reusability (no Galaxy dependencies)
