# Output Formats

This document explains the different output formats generated from topic content and how the builders work.

## Overview

The repository generates multiple output formats from a single source of truth (markdown + metadata). Each output format has its own builder script and template.

## Current Output Formats

### Training Slides (GTN)

**Purpose**: Generate Galaxy Training Network (GTN) compatible Remark.js slides for architecture tutorials.

**Builder**: `outputs/training-slides/build.py`

**Template**: `outputs/training-slides/template.html`

**Usage**:
```bash
uv run python outputs/training-slides/build.py <topic-id>
```

**Output Location**: `outputs/training-slides/generated/architecture-<topic-id>/slides.html`

**Features**:
- GTN-compatible Remark.js format
- Dynamic metadata rendering (questions, objectives, key points, contributors)
- Layout class support (`reduce90`, `enlarge150`)
- Special code block formatting (`.code[]` wrapper)
- Diff format support for code changes
- Image integration from shared `images/` directory

**How It Works**:
1. Loads `metadata.yaml` and markdown content files (`overview.md`, `examples.md`)
2. Splits markdown into slides based on `##` headings and `---` separators
3. Processes layout classes and code wrappers
4. Renders using Jinja2 template with GTN frontmatter
5. Outputs HTML file ready for GTN

**Copying to GTN**:
After generation, copy the output to:
```
training-material/topics/dev/tutorials/architecture-<topic-id>/slides.html
```

**Troubleshooting**:
- **Images not showing**: Check that image paths use `../../images/` format
- **Layout classes not working**: Ensure `class:` directive appears on its own line after `---`
- **Code blocks not styled**: Use `{.code}` marker before code block for special formatting
- **Contributors missing**: Add `training.contributors` to `metadata.yaml`

## Future Output Formats

### Sphinx Documentation (Planned)

**Purpose**: Generate Galaxy Sphinx documentation from topic content.

**Status**: Not yet implemented (Phase 9)

**Planned Features**:
- RST generation from markdown
- Integration with Galaxy docs structure
- Cross-references between topics
- Code examples with syntax highlighting

### Hub Articles (Planned)

**Purpose**: Generate Galaxy Hub articles for galaxyproject.org.

**Status**: Not yet implemented

**Planned Features**:
- Markdown article format
- Hub-specific metadata
- Tag and category support
- Publication workflow

## How Builders Work

### Builder Pattern

Each builder follows a similar pattern:

1. **Load Topic**: Read `metadata.yaml` and content files
2. **Process Content**: Transform markdown to target format
3. **Render Template**: Use Jinja2 template with metadata
4. **Write Output**: Save generated file(s)

### Adding a New Output Format

To add a new output format:

1. **Create builder directory**:
   ```bash
   mkdir -p outputs/<format-name>/{templates,generated}
   ```

2. **Create builder script** (`outputs/<format-name>/build.py`):
   ```python
   #!/usr/bin/env python3
   """Generate <format> from topic content."""
   
   import sys
   import yaml
   from pathlib import Path
   from jinja2 import Template
   
   def load_topic(topic_name):
       # Load metadata and content
       pass
   
   def generate_<format>(topic_name):
       # Generate output
       pass
   
   if __name__ == "__main__":
       generate_<format>(sys.argv[1])
   ```

3. **Create template** (`outputs/<format-name>/templates/template.<ext>`):
   - Use Jinja2 syntax
   - Reference metadata fields
   - Include content sections

4. **Test**: Generate output for existing topic and verify

5. **Document**: Add to this file with usage and features

## Common Issues

### Content Not Appearing

- Check that content files are named correctly (`overview.md`, `examples.md`)
- Verify markdown files are in the topic directory (not `.claude/`)
- Ensure content is properly formatted markdown

### Metadata Errors

- Run `uv run python scripts/validate.py` to check metadata
- Verify all required fields are present
- Check YAML syntax is correct

### Template Errors

- Check Jinja2 syntax in template
- Verify all referenced metadata fields exist
- Test template with minimal content first

### Output Format Issues

- Compare with working examples
- Check template matches expected format
- Verify special formatting (code blocks, images) is handled correctly

## Best Practices

1. **Always validate** before generating outputs
2. **Test locally** before committing generated files
3. **Keep templates simple** - complex logic should be in builder script
4. **Document format-specific features** in this file
5. **Update builders together** when schema changes

