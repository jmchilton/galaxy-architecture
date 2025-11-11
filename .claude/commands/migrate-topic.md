# Migrate Architecture Topic from Training Material

Migrate slides from ~/workspace/training-material/topics/dev/tutorials/architecture-* into this project.

## Usage

```
/migrate-topic <topic-name>
```

## Arguments

- **topic-name**: Human-readable name (e.g., "Dependency Injection", "Application Startup")

## Examples

```
/migrate-topic "Dependency Injection"
/migrate-topic "Application Startup"
/migrate-topic "Configuration Management"
```

## What it does

1. Lists ~/workspace/training-material/topics/dev/tutorials/ to find matching architecture-N-* directory
2. Infers topic-id by kebab-casing the topic-name (e.g., "Dependency Injection" → "dependency-injection")
3. Extracts slides from the matched slides.html file
4. Converts Remark.js slide format to content.yaml format
5. Identifies and copies required images from ~/workspace/training-material/topics/dev/images/
6. Creates topic directory structure:
   - `topics/<topic-id>/metadata.yaml` - Auto-populated with training metadata
   - `topics/<topic-id>/content.yaml` - Slide blocks with unique IDs
   - `topics/<topic-id>/.claude/CLAUDE.md` - Topic-specific context template
7. Validates with `make validate`
8. Builds Sphinx docs with `make build-sphinx`
9. Reports any issues found and fixes needed

## Implementation details

- Auto-detects architecture-N-* directory matching the topic name
- Each Remark.js slide (separated by `---`) becomes a content block
- Image references automatically extracted from markdown and copied
- Slide headings become block IDs (slugified)
- Learning questions/objectives extracted from frontmatter if present
- Creates template .claude/CLAUDE.md for user to complete

## Requirements

- Source slides must exist in ~/workspace/training-material/topics/dev/tutorials/
- Matching architecture-N-* directory must be found
- Images referenced in slides must exist in ~/workspace/training-material/topics/dev/images/
