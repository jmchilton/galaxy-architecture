#!/usr/bin/env python3
"""
Validate all topics for completeness and correctness.

Checks:
- metadata.yaml has all required fields and valid structure
- content.yaml has valid structure and references
- All referenced files exist
- Internal topic references are valid
"""

import sys
from pathlib import Path

from pydantic import ValidationError

from models import load_metadata, load_content, validate_topic_structure


def validate_topic(topic_dir: Path) -> tuple[list[str], list[str]]:
    """Validate a single topic directory."""
    errors = []
    warnings = []
    topic_name = topic_dir.name

    # Check for .claude/CLAUDE.md (not critical but recommended)
    if not (topic_dir / ".claude" / "CLAUDE.md").exists():
        warnings.append("Missing .claude/CLAUDE.md")

    # Use Pydantic models to validate everything
    try:
        metadata, content = validate_topic_structure(topic_name)
    except FileNotFoundError as e:
        errors.append(str(e))
        return errors, warnings
    except ValidationError as e:
        # Format Pydantic validation errors nicely
        for error in e.errors():
            loc = " -> ".join(str(l) for l in error['loc'])
            msg = error['msg']
            errors.append(f"{loc}: {msg}")
        return errors, warnings
    except ValueError as e:
        errors.append(str(e))
        return errors, warnings

    return errors, warnings


def validate_all() -> bool:
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
                # Indent multiline errors
                for line in error.split('\n'):
                    print(f"    {line}")
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
