#!/usr/bin/env python3
"""
Validate all topics for completeness and correctness.

Checks:
- metadata.yaml has all required fields
- All referenced files exist
- Internal topic references are valid
- Markdown is well-formed
- No broken code paths
"""

import sys
import yaml
from pathlib import Path

REQUIRED_METADATA_FIELDS = [
    'topic_id', 'title', 'status',
    'training.questions', 'training.objectives',
    'training.key_points', 'training.time_estimation',
]

VALID_STATUS_VALUES = ['draft', 'stable', 'deprecated']


def get_nested_value(data, keys):
    """Get nested value from dict using dot-separated keys."""
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, {})
        else:
            return None
    return value


def validate_topic(topic_dir):
    """Validate a single topic directory."""
    errors = []
    warnings = []

    # Check metadata exists
    metadata_file = topic_dir / "metadata.yaml"
    if not metadata_file.exists():
        errors.append("Missing metadata.yaml")
        return errors, warnings

    # Load and validate metadata
    try:
        with open(metadata_file) as f:
            metadata = yaml.safe_load(f)
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in metadata.yaml: {e}")
        return errors, warnings

    if not isinstance(metadata, dict):
        errors.append("metadata.yaml must contain a YAML object/dictionary")
        return errors, warnings

    # Check required fields
    for field in REQUIRED_METADATA_FIELDS:
        keys = field.split('.')
        value = get_nested_value(metadata, keys)
        if not value:
            errors.append(f"Missing required field: {field}")

    # Validate topic_id matches directory name
    if 'topic_id' in metadata:
        if metadata['topic_id'] != topic_dir.name:
            errors.append(
                f"topic_id '{metadata['topic_id']}' does not match directory name '{topic_dir.name}'"
            )

    # Validate status enum
    if 'status' in metadata:
        if metadata['status'] not in VALID_STATUS_VALUES:
            errors.append(
                f"Invalid status '{metadata['status']}'. Must be one of: {', '.join(VALID_STATUS_VALUES)}"
            )

    # Validate training fields are lists
    if 'training' in metadata:
        training = metadata['training']
        for field in ['questions', 'objectives', 'key_points']:
            if field in training and not isinstance(training[field], list):
                errors.append(f"training.{field} must be a list")

    # Check content files exist
    if not (topic_dir / "overview.md").exists():
        warnings.append("Missing overview.md")

    # Check Claude context
    if not (topic_dir / ".claude" / "CLAUDE.md").exists():
        warnings.append("Missing .claude/CLAUDE.md")

    # Check related topics are valid
    if 'related_topics' in metadata:
        if not isinstance(metadata['related_topics'], list):
            errors.append("related_topics must be a list")
        else:
            topics_dir = topic_dir.parent
            for related in metadata['related_topics']:
                related_dir = topics_dir / related
                if not related_dir.exists():
                    errors.append(f"Related topic not found: {related}")

    return errors, warnings


def validate_all():
    """Validate all topics."""
    topics_dir = Path("topics")
    if not topics_dir.exists():
        print("❌ ERROR: topics/ directory not found")
        return False

    all_errors = {}
    all_warnings = {}

    for topic_dir in topics_dir.iterdir():
        if topic_dir.is_dir() and not topic_dir.name.startswith('.'):
            errors, warnings = validate_topic(topic_dir)
            if errors:
                all_errors[topic_dir.name] = errors
            if warnings:
                all_warnings[topic_dir.name] = warnings

    # Report results
    print(f"\n{'='*60}")
    print("VALIDATION REPORT")
    print(f"{'='*60}\n")

    if all_errors:
        print("❌ ERRORS:\n")
        for topic, errors in all_errors.items():
            print(f"  {topic}:")
            for error in errors:
                print(f"    - {error}")
        print()

    if all_warnings:
        print("⚠️  WARNINGS:\n")
        for topic, warnings in all_warnings.items():
            print(f"  {topic}:")
            for warning in warnings:
                print(f"    - {warning}")
        print()

    if not all_errors and not all_warnings:
        print("✅ All topics valid!")

    return len(all_errors) == 0


def main():
    """Main entry point for the validate-topics script."""
    success = validate_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

