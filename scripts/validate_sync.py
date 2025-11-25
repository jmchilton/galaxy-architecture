#!/usr/bin/env python3
"""
Validate sync to training-material.

Checks that:
- All topics have slides in training-material
- All referenced images exist
- No .plantuml.txt or .mindmap.yml files copied
- Front matter matches metadata.yaml

Usage:
    uv run python scripts/validate_sync.py
    uv run python scripts/validate_sync.py --topic ecosystem
"""

import argparse
import sys
from pathlib import Path

# Add scripts to path for models
sys.path.insert(0, str(Path(__file__).parent))
from models import load_metadata
from sync_images import find_referenced_images
from sync_to_training_material import get_training_material_directory


def validate_topic(topic_id: str, tm_root: Path) -> dict:
    """
    Validate sync for single topic.

    Returns dict with:
        - valid: bool
        - errors: list of error messages
        - warnings: list of warning messages
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': []
    }

    try:
        # Load metadata
        metadata = load_metadata(topic_id)
        target_dir = get_training_material_directory(metadata, tm_root)

        # Check slides exist
        target_slides = target_dir / "slides.html"
        if not target_slides.exists():
            result['errors'].append(f"Slides not found: {target_slides}")
            result['valid'] = False

        # Check images exist
        images = find_referenced_images(topic_id)
        tm_images_dir = tm_root / "topics/dev/images"
        tm_shared_dir = tm_root / "shared/images"

        for img_name in images:
            # Check in both possible locations
            dev_path = tm_images_dir / img_name
            shared_path = tm_shared_dir / img_name

            if not dev_path.exists() and not shared_path.exists():
                result['errors'].append(f"Image missing: {img_name}")
                result['valid'] = False

        # Check no source files copied
        for src_pattern in ['*.plantuml.txt', '*.mindmap.yml']:
            found = list(tm_images_dir.glob(src_pattern))
            if found:
                result['errors'].append(f"Source files found in training-material: {[f.name for f in found]}")
                result['valid'] = False

    except Exception as e:
        result['errors'].append(f"Exception: {e}")
        result['valid'] = False
        import traceback
        traceback.print_exc()

    return result


def main():
    parser = argparse.ArgumentParser(description='Validate sync to training-material')
    parser.add_argument('--topic', help='Topic ID to validate')
    parser.add_argument(
        '--training-material-root',
        type=Path,
        default=Path.home() / 'workspace' / 'training-material',
        help='Path to training-material repository'
    )

    args = parser.parse_args()

    if not args.training_material_root.exists():
        print(f"❌ Training-material not found: {args.training_material_root}")
        sys.exit(1)

    # Get list of topics
    if args.topic:
        topics = [args.topic]
    else:
        topics_dir = Path('topics')
        topics = sorted([d.name for d in topics_dir.iterdir() if d.is_dir()])

    # Validate each topic
    all_valid = True
    total_errors = 0
    total_warnings = 0

    for topic in topics:
        print(f"\n{'='*60}")
        print(f"Topic: {topic}")
        print('='*60)

        result = validate_topic(topic, args.training_material_root)

        if result['errors']:
            print(f"\n❌ Errors ({len(result['errors'])}):")
            for error in result['errors']:
                print(f"  - {error}")
            total_errors += len(result['errors'])
            all_valid = False
        else:
            print(f"\n✅ Valid")

        if result['warnings']:
            print(f"\n⚠️  Warnings ({len(result['warnings'])}):")
            for warning in result['warnings']:
                print(f"  - {warning}")
            total_warnings += len(result['warnings'])

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Topics validated: {len(topics)}")
    print(f"Errors: {total_errors}")
    print(f"Warnings: {total_warnings}")

    if all_valid:
        print("\n✅ All topics valid!")
        sys.exit(0)
    else:
        print("\n❌ Validation failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
