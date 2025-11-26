# Metadata and Content Schema

This document describes the structure of `metadata.yaml` and `content.yaml` files.
The schema is enforced by Pydantic models in `scripts/models.py`.

## Overview

Each topic directory contains:

- **metadata.yaml** - Topic configuration and metadata for all output formats
- **content.yaml** - Ordered sequence of content blocks with rendering rules
- **fragments/** - Markdown fragments referenced by content blocks

---

# metadata.yaml

## TopicMetadata

Complete topic metadata from metadata.yaml.

This is the source of truth for topic configuration across all output formats.

### `topic_id`

**Type:** `string`

**Required**

Unique identifier (lowercase, hyphenated)


### `title`

**Type:** `string`

**Required**

Human-readable title


### `training`

**Type:** `TrainingMetadata`

**Required**

Training slide configuration


### `sphinx`

**Type:** `Optional`

**Optional**

Sphinx documentation configuration


### `contributors`

**Type:** `list of string`

**Required**

List of contributors (e.g., GitHub usernames)


### `related_topics`

**Type:** `list of string`

**Default:** `PydanticUndefined`

Related topic IDs for cross-referencing


### `related_code_paths`

**Type:** `list of string`

**Default:** `PydanticUndefined`

Galaxy code paths relevant to this topic



## Nested Types

### TrainingMetadata

Training slide metadata.

Defines the learning objectives and structure for training materials.

### `tutorial_number`

**Type:** `integer`

**Required**

Tutorial number in training-material (e.g., 1 for architecture-1-ecosystem)


### `subtitle`

**Type:** `string`

**Required**

Subtitle for title slide (e.g., 'The architecture of the ecosystem.')


### `questions`

**Type:** `list of string`

**Required**

Learning questions this topic addresses


### `objectives`

**Type:** `list of string`

**Required**

Learning objectives for trainees


### `key_points`

**Type:** `list of string`

**Required**

Key takeaways from the training


### `time_estimation`

**Type:** `string`

**Required**

Estimated time to complete (e.g., '30m', '1h')


### `prerequisites`

**Type:** `list of string`

**Default:** `PydanticUndefined`

Topic IDs that should be learned first


### `previous_to`

**Type:** `Optional`

**Optional**

Topic ID that precedes this topic in sequence


### `continues_to`

**Type:** `Optional`

**Optional**

Topic ID that follows this topic in sequence


### SphinxMetadata

Sphinx documentation metadata.

Controls how the topic appears in Galaxy's Sphinx documentation.

### `section`

**Type:** `string`

**Required**

Top-level section (e.g., 'Architecture')


### `subsection`

**Type:** `Optional`

**Optional**

Subsection within the section



---

# content.yaml

Content is defined as a YAML list of content blocks.

## Smart Defaults

- **Prose blocks:** Render in docs by default, NOT in slides
- **Slide blocks:** Render in BOTH docs and slides by default

To override, explicitly set `doc.render: false` or `slides.render: false`.

## ContentBlock

Single content block in content.yaml.

Represents one unit of content (prose paragraph or slide) with rendering
configuration for different output formats.

### `type`

**Type:** `enum: PROSE, SLIDE`

**Required**

Type of content block


### `id`

**Type:** `string`

**Required**

Unique identifier for this block


### `content`

**Type:** `Optional`

**Optional**

Inline content (for short blocks)


### `file`

**Type:** `Optional`

**Optional**

Single fragment file path (relative to topic dir)


### `fragments`

**Type:** `Optional`

**Optional**

Multiple fragment file paths to combine


### `heading`

**Type:** `Optional`

**Optional**

Heading text (optional for slides)


### `separator`

**Type:** `string`

**Default:** `

`

Separator when combining fragments


### `class_`

**Type:** `Optional`

**Optional**

CSS classes for slides (shorthand for slides.class_)


### `doc`

**Type:** `DocRenderConfig`

**Default:** `PydanticUndefined`

Documentation rendering config


### `slides`

**Type:** `SlideRenderConfig`

**Default:** `PydanticUndefined`

Slide rendering config



## Rendering Configuration

### DocRenderConfig

Configuration for rendering in documentation (Sphinx).

Controls how content appears in continuous documentation format.

### `render`

**Type:** `boolean`

**Default:** `True`

Whether to include in documentation


### `heading_level`

**Type:** `Optional`

**Optional**

Heading level for this section (1-6)


### SlideRenderConfig

Configuration for rendering in training slides.

Controls how content appears in slide presentation format.

### `render`

**Type:** `boolean`

**Default:** `True`

Whether to include in slides


### `class_`

**Type:** `Optional`

**Optional**

CSS classes to apply to slides (e.g., 'center', 'reduce90', 'enlarge150')


### `layout_name`

**Type:** `Optional`

**Optional**

Named layout to reference (e.g., 'left-aligned')



---

# Example metadata.yaml

```yaml
topic_id: dependency-injection
title: Dependency Injection in Galaxy
status: stable

created: 2025-01-15
last_updated: 2025-01-15
last_updated_by: jmchilton

training:
  questions:
    - What is dependency injection?
  objectives:
    - Understand DI patterns
  key_points:
    - Galaxy uses type-based DI
  time_estimation: 15m

sphinx:
  section: Architecture
  level: intermediate

related_topics:
  - frameworks

contributors:
  - jmchilton
```

# Example content.yaml

```yaml
# Prose intro (docs only by default)
- type: prose
  id: intro
  content: |
    Introduction paragraph...

# Slide (appears in both by default)
- type: slide
  id: problem
  heading: The Problem
  file: fragments/problem.md

# Prose transition (docs only)
- type: prose
  id: transition
  content: |
    Now let's look at solutions...

# Slide with custom heading level for docs
- type: slide
  id: solution
  heading: The Solution
  file: fragments/solution.md
  doc:
    heading_level: 3

# Multiple fragments combined
- type: slide
  id: examples
  heading: Examples
  fragments:
    - fragments/example1.md
    - fragments/example2.md
  separator: "\n\n---\n\n"
```

---

# Validation

Run validation with:

```bash
uv run python scripts/validate.py
```

This checks:

- All required fields present
- Field types and formats correct
- Referenced files exist
- Related topics exist
- No duplicate block IDs
- At least one slide present
- Smart defaults applied correctly
