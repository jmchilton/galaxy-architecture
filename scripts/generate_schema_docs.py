#!/usr/bin/env python3
"""Generate SCHEMA.md documentation from Pydantic models."""

from datetime import date
from pathlib import Path
from typing import Any, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo

from models import (
    TopicMetadata,
    TopicContent,
    ContentBlock,
    TrainingMetadata,
    SphinxMetadata,
    HubMetadata,
    ClaudeMetadata,
    ImageMetadata,
    DocRenderConfig,
    SlideRenderConfig,
    TopicStatus,
    ContentBlockType,
)


def format_type(field_info: FieldInfo) -> str:
    """Format field type as a readable string."""
    annotation = field_info.annotation

    # Handle Optional types
    origin = get_origin(annotation)
    if origin is type(None) or (hasattr(annotation, '__origin__') and annotation.__origin__ is type(None)):
        return "null"

    # Handle Union types (including Optional)
    args = get_args(annotation)
    if origin is type or origin is type(None):
        if len(args) == 2 and type(None) in args:
            # This is Optional[T]
            inner_type = args[0] if args[1] is type(None) else args[1]
            return f"optional {format_simple_type(inner_type)}"

    return format_simple_type(annotation)


def format_simple_type(t: Any) -> str:
    """Format a simple type."""
    if t is str:
        return "string"
    elif t is int:
        return "integer"
    elif t is bool:
        return "boolean"
    elif t is date:
        return "date (YYYY-MM-DD)"

    origin = get_origin(t)
    if origin is list:
        args = get_args(t)
        if args:
            return f"list of {format_simple_type(args[0])}"
        return "list"

    if origin is dict:
        return "object"

    # Handle Literal types
    if origin is type or (hasattr(t, '__origin__') and 'Literal' in str(t.__origin__)):
        args = get_args(t)
        if args:
            return f"enum: {', '.join(repr(a) for a in args)}"

    # Handle enums
    if isinstance(t, type) and issubclass(t, str) and hasattr(t, '__members__'):
        return f"enum: {', '.join(t.__members__.keys())}"

    return str(t.__name__ if hasattr(t, '__name__') else t)


def document_model(model: type[BaseModel], level: int = 2) -> str:
    """Generate markdown documentation for a Pydantic model."""
    lines = []
    heading = '#' * level

    # Model name and docstring
    lines.append(f"{heading} {model.__name__}")
    lines.append("")
    if model.__doc__:
        lines.append(model.__doc__.strip())
        lines.append("")

    # Fields
    for field_name, field_info in model.model_fields.items():
        lines.append(f"### `{field_name}`")
        lines.append("")

        # Type
        field_type = format_type(field_info)
        lines.append(f"**Type:** `{field_type}`")
        lines.append("")

        # Required/Optional
        is_required = field_info.is_required()
        if is_required:
            lines.append("**Required**")
        else:
            default = field_info.default
            if default is not None:
                lines.append(f"**Default:** `{default}`")
            else:
                lines.append("**Optional**")
        lines.append("")

        # Description
        description = field_info.description
        if description:
            lines.append(description)
            lines.append("")

        lines.append("")

    return "\n".join(lines)


def generate_schema_docs() -> str:
    """Generate complete SCHEMA.md content."""
    lines = [
        "# Metadata and Content Schema",
        "",
        "This document describes the structure of `metadata.yaml` and `content.yaml` files.",
        "The schema is enforced by Pydantic models in `scripts/models.py`.",
        "",
        "## Overview",
        "",
        "Each topic directory contains:",
        "",
        "- **metadata.yaml** - Topic configuration and metadata for all output formats",
        "- **content.yaml** - Ordered sequence of content blocks with rendering rules",
        "- **fragments/** - Markdown fragments referenced by content blocks",
        "",
        "---",
        "",
        "# metadata.yaml",
        "",
        document_model(TopicMetadata, level=2),
        "",
        "## Nested Types",
        "",
        document_model(TrainingMetadata, level=3),
        document_model(SphinxMetadata, level=3),
        document_model(HubMetadata, level=3),
        document_model(ClaudeMetadata, level=3),
        document_model(ImageMetadata, level=3),
        "",
        "---",
        "",
        "# content.yaml",
        "",
        "Content is defined as a YAML list of content blocks.",
        "",
        "## Smart Defaults",
        "",
        "- **Prose blocks:** Render in docs by default, NOT in slides",
        "- **Slide blocks:** Render in BOTH docs and slides by default",
        "",
        "To override, explicitly set `doc.render: false` or `slides.render: false`.",
        "",
        document_model(ContentBlock, level=2),
        "",
        "## Rendering Configuration",
        "",
        document_model(DocRenderConfig, level=3),
        document_model(SlideRenderConfig, level=3),
        "",
        "---",
        "",
        "# Example metadata.yaml",
        "",
        "```yaml",
        "topic_id: dependency-injection",
        "title: Dependency Injection in Galaxy",
        "status: stable",
        "",
        "created: 2025-01-15",
        "last_updated: 2025-01-15",
        "last_updated_by: jmchilton",
        "",
        "training:",
        "  questions:",
        "    - What is dependency injection?",
        "  objectives:",
        "    - Understand DI patterns",
        "  key_points:",
        "    - Galaxy uses type-based DI",
        "  time_estimation: 15m",
        "",
        "sphinx:",
        "  section: Architecture",
        "  level: intermediate",
        "",
        "related_topics:",
        "  - frameworks",
        "",
        "contributors:",
        "  - jmchilton",
        "```",
        "",
        "# Example content.yaml",
        "",
        "```yaml",
        "# Prose intro (docs only by default)",
        "- type: prose",
        "  id: intro",
        "  content: |",
        "    Introduction paragraph...",
        "",
        "# Slide (appears in both by default)",
        "- type: slide",
        "  id: problem",
        "  heading: The Problem",
        "  file: fragments/problem.md",
        "",
        "# Prose transition (docs only)",
        "- type: prose",
        "  id: transition",
        "  content: |",
        "    Now let's look at solutions...",
        "",
        "# Slide with custom heading level for docs",
        "- type: slide",
        "  id: solution",
        "  heading: The Solution",
        "  file: fragments/solution.md",
        "  doc:",
        "    heading_level: 3",
        "",
        "# Multiple fragments combined",
        "- type: slide",
        "  id: examples",
        "  heading: Examples",
        "  fragments:",
        "    - fragments/example1.md",
        "    - fragments/example2.md",
        "  separator: \"\\n\\n---\\n\\n\"",
        "```",
        "",
        "---",
        "",
        "# Validation",
        "",
        "Run validation with:",
        "",
        "```bash",
        "uv run python scripts/validate.py",
        "```",
        "",
        "This checks:",
        "",
        "- All required fields present",
        "- Field types and formats correct",
        "- Referenced files exist",
        "- Related topics exist",
        "- No duplicate block IDs",
        "- At least one slide present",
        "- Smart defaults applied correctly",
        "",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    docs = generate_schema_docs()
    output_path = Path("docs/SCHEMA.md")
    output_path.write_text(docs)
    print(f"✓ Generated {output_path}")
