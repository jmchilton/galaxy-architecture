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
Galaxy code paths relevant to this topic.
```yaml
related_code_paths:
  - lib/galaxy/managers/
  - lib/galaxy/app.py
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

## Validation

Run `python scripts/validate.py` to check all metadata files.

Required fields are enforced. Optional fields improve output quality.

