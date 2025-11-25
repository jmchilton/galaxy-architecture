#!/usr/bin/env python3
"""
Sync images to training-material repository.

Only copies rendered images (SVG, PNG, JPG), not source files (.plantuml.txt, .mindmap.yml).
Per IMAGE_HANDLING.md and BACK_TO_TRAINING_PLAN.md.

Usage:
    uv run python scripts/sync_images.py --topic ecosystem
    uv run python scripts/sync_images.py --all
    uv run python scripts/sync_images.py --all --dry-run
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Set

# Add scripts to path for models
sys.path.insert(0, str(Path(__file__).parent))
from models import load_content


def should_copy_image(image_path: Path) -> bool:
    """Only copy rendered images, not source files."""
    # Copy these extensions
    if image_path.suffix.lower() in ['.svg', '.png', '.jpg', '.jpeg', '.gif']:
        # BUT skip source files for PlantUML/mindmaps
        if '.plantuml.txt' in image_path.name:
            return False
        if '.mindmap.yml' in image_path.name:
            return False
        return True

    # Don't copy these
    return False


def find_referenced_images(topic_id: str) -> Set[str]:
    """Extract all image filenames from content blocks."""
    content = load_content(topic_id)
    images = set()

    for block in content.root:
        # Get markdown from block
        markdown = ""

        if block.content:
            # Inline content
            markdown = block.content
        elif block.file:
            # Read from single file
            file_path = Path('topics') / topic_id / block.file
            if file_path.exists():
                markdown = file_path.read_text()
        elif block.fragments:
            # Read multiple fragments
            for frag in block.fragments:
                frag_path = Path('topics') / topic_id / 'fragments' / frag
                if frag_path.exists():
                    markdown += frag_path.read_text() + "\n"

        if not markdown:
            continue

        # Find all image references: ![alt](path)
        img_matches = re.findall(r'!\[.*?\]\((.*?)\)', markdown)
        for img_path in img_matches:
            # Skip external URLs
            if img_path.startswith('http://') or img_path.startswith('https://'):
                continue

            # Extract filename from path
            filename = Path(img_path).name
            images.add(filename)

    return images


def categorize_image_source(image_name: str, images_dir: Path) -> str:
    """
    Determine image category.

    Returns:
        'plantuml' - PlantUML/mindmap SVG diagram
        'shared' - Shared GTN image (like GTNLogo1000.png, conda_logo.png)
        'dev' - Dev topic image
    """
    # PlantUML/mindmap diagrams
    if '.plantuml.svg' in image_name or '.mindmap.plantuml.svg' in image_name:
        return 'plantuml'

    # Shared images (hardcoded common ones)
    shared_images = ['GTNLogo1000.png', 'conda_logo.png', 'gtn_logo.png']
    if image_name in shared_images:
        return 'shared'

    # Default: dev topic image
    return 'dev'


def sync_topic_images(
    topic_id: str,
    training_material_root: Path,
    dry_run: bool = False
) -> dict:
    """
    Sync images for a single topic to training-material.

    Returns dict with:
        - copied: list of (src, dst) tuples
        - skipped: list of (filename, reason) tuples
        - missing: list of filenames not found
    """
    result = {
        'copied': [],
        'skipped': [],
        'missing': []
    }

    # Find images referenced in content
    images = find_referenced_images(topic_id)
    images_dir = Path('images')

    for image_name in sorted(images):
        src_path = images_dir / image_name

        # Check if image exists
        if not src_path.exists():
            result['missing'].append(image_name)
            continue

        # Check if we should copy it
        if not should_copy_image(src_path):
            result['skipped'].append((image_name, 'source file (not copied)'))
            continue

        # Determine destination
        category = categorize_image_source(image_name, images_dir)

        if category == 'shared':
            dst_path = training_material_root / 'shared' / 'images' / image_name
        else:  # plantuml or dev
            dst_path = training_material_root / 'topics' / 'dev' / 'images' / image_name

        # Create destination directory
        if not dry_run:
            dst_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        if dry_run:
            result['copied'].append((str(src_path), str(dst_path)))
        else:
            shutil.copy2(src_path, dst_path)
            result['copied'].append((str(src_path), str(dst_path)))

    return result


def main():
    parser = argparse.ArgumentParser(description='Sync images to training-material')
    parser.add_argument('--topic', help='Topic ID to sync')
    parser.add_argument('--all', action='store_true', help='Sync all topics')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be copied without copying')
    parser.add_argument(
        '--training-material-root',
        type=Path,
        default=Path.home() / 'workspace' / 'training-material',
        help='Path to training-material repository'
    )

    args = parser.parse_args()

    if not args.all and not args.topic:
        parser.error("Either specify --topic or use --all")

    if not args.training_material_root.exists():
        print(f"❌ Training-material not found: {args.training_material_root}")
        sys.exit(1)

    # Get list of topics
    if args.all:
        topics_dir = Path('topics')
        topics = sorted([d.name for d in topics_dir.iterdir() if d.is_dir()])
    else:
        topics = [args.topic]

    # Sync each topic
    total_copied = 0
    total_skipped = 0
    total_missing = 0

    for topic in topics:
        print(f"\n{'='*60}")
        print(f"Topic: {topic}")
        print('='*60)

        try:
            result = sync_topic_images(topic, args.training_material_root, args.dry_run)

            if result['copied']:
                print(f"\n✅ Copied {len(result['copied'])} image(s):")
                for src, dst in result['copied']:
                    print(f"  {Path(src).name} → {dst}")
                total_copied += len(result['copied'])

            if result['skipped']:
                print(f"\n⏭️  Skipped {len(result['skipped'])} image(s):")
                for name, reason in result['skipped']:
                    print(f"  {name} ({reason})")
                total_skipped += len(result['skipped'])

            if result['missing']:
                print(f"\n⚠️  Missing {len(result['missing'])} image(s):")
                for name in result['missing']:
                    print(f"  {name}")
                total_missing += len(result['missing'])

            if not result['copied'] and not result['skipped'] and not result['missing']:
                print("\n  No images referenced in this topic")

        except Exception as e:
            print(f"\n❌ Error syncing {topic}: {e}")
            import traceback
            traceback.print_exc()

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Topics processed: {len(topics)}")
    print(f"Images copied: {total_copied}")
    print(f"Images skipped: {total_skipped}")
    print(f"Images missing: {total_missing}")

    if args.dry_run:
        print("\n(DRY RUN - no files were actually copied)")


if __name__ == '__main__':
    main()
