# Metadata Schema

Every topic must have a `metadata.yaml` file following this schema.

## Required Fields

### `topic_id` (string)
Unique identifier for the topic. Must match directory name.
```yaml
topic_id: dependency-injection
```

### `title` (string)
Human-readable title for the topic.
```yaml
title: Dependency Injection in Galaxy
```

### `status` (enum: draft | stable | deprecated)
Current status of the documentation.
```yaml
status: stable
```

### `training` (object)
Metadata for training slides.

#### `training.questions` (list of strings)
Learning questions this topic addresses.
```yaml
training:
  questions:
    - What is dependency injection?
    - How does Galaxy implement DI?
```

#### `training.objectives` (list of strings)
Learning objectives.
```yaml
training:
  objectives:
    - Understand DI patterns in Galaxy
    - Identify injection points
```

#### `training.key_points` (list of strings)
Key takeaways.
```yaml
training:
  key_points:
    - Galaxy uses PasteScript-style DI
    - Managers are injected via app
```

#### `training.time_estimation` (string)
Estimated time to learn this material.
```yaml
training:
  time_estimation: 30m
```

#### `training.prerequisites` (list of strings)
Other topics that should be learned before this one.
```yaml
training:
  prerequisites:
    - architecture-frameworks
    - application-components
```

#### `training.contributors` (list of strings)
GitHub usernames of contributors to this topic.
```yaml
training:
  contributors:
    - jmchilton
    - bgruening
```

## Optional Fields

### `created` (date: YYYY-MM-DD)
When topic was first created.

### `last_updated` (date: YYYY-MM-DD)
When topic was last significantly updated.

### `last_updated_by` (string)
Who last updated the topic.

### `training.prerequisites` (list of strings)
Other topics to learn first.
```yaml
training:
  prerequisites:
    - frameworks
    - application-components
```

### `sphinx` (object)
Metadata for Sphinx documentation.
```yaml
sphinx:
  section: Architecture
  subsection: Core Patterns
  level: intermediate  # beginner | intermediate | advanced
  toc_depth: 2
```

### `hub` (object)
Metadata for Galaxy Hub articles.
```yaml
hub:
  audience: [developers, contributors]
  tags: [architecture, design-patterns]
```

### `related_topics` (list of strings)
Cross-references to other topics.
```yaml
related_topics:
  - application-components
  - startup
```

### `related_code_paths` (list of strings)
Galaxy code paths relevant to this topic. These should be mentioned in the content files.
```yaml
related_code_paths:
  - lib/galaxy/managers/
  - lib/galaxy/app.py
  - lib/galaxy/di/
```

### `images` (list of objects)
Images used in slides (shared across topics). Each image entry should have:
- `path`: Relative path from repo root (e.g., `../../images/file.svg`)
- `description`: Human-readable description
- `source`: Optional path to source file (e.g., PlantUML `.txt` file)
```yaml
images:
  - path: ../../images/app_py2.plantuml.svg
    description: "Python 2 era app structure"
    source: images/app_py2.plantuml.txt
  - path: ../../images/lagom_ss.png
    description: "Lagom dependency injection library website screenshot"
```

### `claude` (object)
AI context metadata.
```yaml
claude:
  priority: high  # low | medium | high
  focus_areas:
    - Dependency injection patterns
    - Manager initialization
```

## Validation Rules

Run `uv run python scripts/validate.py` to check all metadata files.

### Required Fields
The following fields are **required** and validation will fail if missing:
- `topic_id` - Must match directory name
- `title` - Human-readable title
- `status` - Must be one of: `draft`, `stable`, `deprecated`
- `training.questions` - List of learning questions
- `training.objectives` - List of learning objectives
- `training.key_points` - List of key takeaways
- `training.time_estimation` - Estimated time (e.g., "15m", "30m")

### Validation Checks
The validation script checks:
- ✅ All required fields present
- ✅ `topic_id` matches directory name
- ✅ `status` is valid enum value
- ✅ Training fields are lists (not strings)
- ✅ Related topics exist (if specified)
- ✅ Image files exist (if specified)
- ✅ Code paths are mentioned in content (warning if not)

### Optional Fields
Optional fields improve output quality but don't cause validation errors:
- `created`, `last_updated`, `last_updated_by` - Tracking metadata
- `training.prerequisites` - Learning dependencies
- `training.contributors` - Attribution
- `sphinx` - Sphinx documentation metadata (for future use)
- `hub` - Galaxy Hub metadata (for future use)
- `related_topics` - Cross-references
- `related_code_paths` - Code path references
- `images` - Image metadata
- `claude` - AI context metadata

