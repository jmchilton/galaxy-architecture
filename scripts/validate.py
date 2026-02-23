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

from models import load_metadata, load_content, validate_topic_structure, TopicMetadata


def validate_tutorial_chain(all_metadata: dict[str, TopicMetadata]) -> list[str]:
    """Validate tutorial ordering is consistent across all topics.

    Checks:
    - No duplicate tutorial_numbers
    - previous_to/continues_to references exist
    - Bidirectional links are consistent (A->B means B<-A)
    - tutorial_numbers match the chain (previous is n-1, next is n+1)
    """
    errors = []

    # Build lookup by tutorial_number
    by_number: dict[int, list[str]] = {}
    for topic_id, meta in all_metadata.items():
        num = meta.training.tutorial_number
        if num not in by_number:
            by_number[num] = []
        by_number[num].append(topic_id)

    # Check for duplicate tutorial_numbers
    for num, topics in by_number.items():
        if len(topics) > 1:
            errors.append(f"Duplicate tutorial_number {num}: {', '.join(topics)}")

    # Validate chain consistency
    for topic_id, meta in all_metadata.items():
        num = meta.training.tutorial_number
        prev_to = meta.training.previous_to
        cont_to = meta.training.continues_to

        # Check previous_to reference exists
        if prev_to:
            if prev_to not in all_metadata:
                errors.append(f"{topic_id}: previous_to '{prev_to}' not found")
            else:
                prev_meta = all_metadata[prev_to]
                prev_num = prev_meta.training.tutorial_number

                # Check tutorial_number is one less
                if prev_num != num - 1:
                    errors.append(
                        f"{topic_id} (#{num}): previous_to '{prev_to}' has "
                        f"tutorial_number {prev_num}, expected {num - 1}"
                    )

                # Check bidirectional link
                if prev_meta.training.continues_to != topic_id:
                    errors.append(
                        f"{topic_id}: previous_to '{prev_to}' but "
                        f"'{prev_to}' continues_to '{prev_meta.training.continues_to}'"
                    )

        # Check continues_to reference exists
        if cont_to:
            if cont_to not in all_metadata:
                errors.append(f"{topic_id}: continues_to '{cont_to}' not found")
            else:
                cont_meta = all_metadata[cont_to]
                cont_num = cont_meta.training.tutorial_number

                # Check tutorial_number is one more
                if cont_num != num + 1:
                    errors.append(
                        f"{topic_id} (#{num}): continues_to '{cont_to}' has "
                        f"tutorial_number {cont_num}, expected {num + 1}"
                    )

                # Check bidirectional link
                if cont_meta.training.previous_to != topic_id:
                    errors.append(
                        f"{topic_id}: continues_to '{cont_to}' but "
                        f"'{cont_to}' previous_to '{cont_meta.training.previous_to}'"
                    )

    # Check chain has exactly one start (no previous_to) and one end (no continues_to)
    starts = [t for t, m in all_metadata.items() if not m.training.previous_to]
    ends = [t for t, m in all_metadata.items() if not m.training.continues_to]

    if len(starts) != 1:
        errors.append(f"Expected 1 chain start (no previous_to), found {len(starts)}: {starts}")
    if len(ends) != 1:
        errors.append(f"Expected 1 chain end (no continues_to), found {len(ends)}: {ends}")

    return errors


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

    # Validate agentic operations
    if metadata.agentic_operations:
        # Check for suggestions directory
        suggestions_dir = topic_dir / "suggestions"
        if not suggestions_dir.exists():
            warnings.append(
                "Consider creating suggestions/ directory for operation feedback"
            )

        # Check operation quality
        for op in metadata.agentic_operations:
            if len(op.prompt) < 20:
                warnings.append(
                    f"Operation '{op.name}': prompt is very short (< 20 chars)"
                )

            # Operations should have related_code_paths for context
            if not metadata.related_code_paths:
                warnings.append(
                    f"Operation '{op.name}': consider adding related_code_paths for context"
                )

    return errors, warnings


def validate_all() -> bool:
    """Validate all topics."""
    topics_dir = Path("topics")
    if not topics_dir.exists():
        print("❌ ERROR: topics/ directory not found")
        return False

    all_errors = {}
    all_warnings = {}
    all_metadata = {}

    for topic_dir in topics_dir.iterdir():
        if topic_dir.is_dir() and not topic_dir.name.startswith('.'):
            errors, warnings = validate_topic(topic_dir)
            if errors:
                all_errors[topic_dir.name] = errors
            if warnings:
                all_warnings[topic_dir.name] = warnings

            # Collect metadata for chain validation (only if no errors loading it)
            if not errors:
                try:
                    all_metadata[topic_dir.name] = load_metadata(topic_dir.name, topics_dir)
                except Exception:
                    pass  # Already reported in validate_topic

    # Validate tutorial chain across all topics
    if all_metadata:
        chain_errors = validate_tutorial_chain(all_metadata)
        if chain_errors:
            all_errors["[tutorial-chain]"] = chain_errors

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
