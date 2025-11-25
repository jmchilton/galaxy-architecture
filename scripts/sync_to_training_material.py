#!/usr/bin/env python3
"""
Sync generated slides to training-material repository.

Copies Jekyll markdown slides (slides.md) to training-material as slides.html.
Also syncs images per IMAGE_HANDLING.md (SVG/PNG/JPG only, not source files).

Usage:
    uv run python scripts/sync_to_training_material.py ecosystem
    uv run python scripts/sync_to_training_material.py --all
    uv run python scripts/sync_to_training_material.py --all --dry-run
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Add scripts to path for models
sys.path.insert(0, str(Path(__file__).parent))
from models import load_metadata
from sync_images import sync_topic_images


def generate_navigation_footnote(metadata) -> str:
    """Generate navigation footnote for training-material slides.

    Format: .footnote[Previous: [Topic](link) | Next: [Topic](link)]
    Only used for training-material sync, not for local sphinx or standalone HTML.
    """
    parts = []

    # Previous link
    if metadata.training.previous_to:
        prev_topic = load_metadata(metadata.training.previous_to)
        prev_num = prev_topic.training.tutorial_number
        prev_title = prev_topic.title
        # Remove "Architecture NN - " prefix for cleaner link text
        prev_display_title = prev_title.replace(f"Architecture {prev_num:02d} - ", "")
        prev_link = f"{{% link topics/dev/tutorials/architecture-{metadata.training.previous_to}/slides.html %}}"
        parts.append(f"Previous: [{prev_display_title}]({prev_link})")

    # Next link
    if metadata.training.continues_to:
        next_topic = load_metadata(metadata.training.continues_to)
        next_num = next_topic.training.tutorial_number
        next_title = next_topic.title
        # Remove "Architecture NN - " prefix for cleaner link text
        next_display_title = next_title.replace(f"Architecture {next_num:02d} - ", "")
        next_link = f"{{% link topics/dev/tutorials/architecture-{metadata.training.continues_to}/slides.html %}}"
        parts.append(f"Next: [{next_display_title}]({next_link})")

    if parts:
        return f".footnote[{' | '.join(parts)}]"
    return ""


def get_training_material_directory(metadata, tm_root: Path) -> Path:
    """Build path from topic_id: architecture-{topic_id}."""
    topic_id = metadata.topic_id
    return tm_root / "topics/dev/tutorials" / f"architecture-{topic_id}"


def sync_topic(
    topic_id: str,
    training_material_root: Path,
    dry_run: bool = False
) -> dict:
    """
    Sync single topic to training-material.

    Returns dict with:
        - slides_copied: bool
        - images_result: dict from sync_topic_images
        - target_dir: Path to training-material directory
    """
    result = {
        'slides_copied': False,
        'images_result': None,
        'target_dir': None,
        'error': None
    }

    try:
        # Load metadata
        metadata = load_metadata(topic_id)
        target_dir = get_training_material_directory(metadata, training_material_root)
        result['target_dir'] = target_dir

        # Check if our Jekyll markdown slides exist (NOT the standalone HTML)
        our_slides = Path(f"outputs/training-slides/generated/architecture-{topic_id}/slides.md")
        if not our_slides.exists():
            result['error'] = f"Slides not found: {our_slides}. Run: make build-slides"
            return result

        # Check if target directory exists
        if not target_dir.exists():
            result['error'] = f"Training-material directory not found: {target_dir}"
            return result

        # Copy Jekyll markdown slides to slides.html (training-material naming convention)
        target_slides = target_dir / "slides.html"

        # Read slides and add navigation footnote
        slides_content = our_slides.read_text()
        footnote = generate_navigation_footnote(metadata)

        # Add footnote to last slide (before final closing line if present)
        if footnote:
            # Find the last slide separator or end of file
            lines = slides_content.split('\n')
            # Insert footnote before the last line if it's empty, otherwise at end
            if lines and not lines[-1].strip():
                lines.insert(-1, footnote)
            else:
                lines.append(footnote)
            slides_content = '\n'.join(lines)

        if dry_run:
            print(f"  Would copy: {our_slides} → {target_slides}")
            print(f"  With footnote: {footnote if footnote else '(none)'}")
            result['slides_copied'] = True
        else:
            target_slides.write_text(slides_content)
            result['slides_copied'] = True

        # Sync images
        result['images_result'] = sync_topic_images(topic_id, training_material_root, dry_run)

    except Exception as e:
        result['error'] = str(e)
        import traceback
        traceback.print_exc()

    return result


def main():
    parser = argparse.ArgumentParser(description='Sync slides to training-material')
    parser.add_argument('topic', nargs='?', help='Topic ID to sync')
    parser.add_argument('--all', action='store_true', help='Sync all topics')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be copied without copying')
    parser.add_argument(
        '--training-material-root',
        type=Path,
        default=Path.home() / 'workspace' / 'training-material',
        help='Path to training-material repository'
    )
    parser.add_argument(
        '--rebuild-slides',
        action='store_true',
        help='Rebuild slides before syncing'
    )

    args = parser.parse_args()

    if not args.all and not args.topic:
        parser.error("Either specify a topic or use --all")

    if not args.training_material_root.exists():
        print(f"❌ Training-material not found: {args.training_material_root}")
        sys.exit(1)

    # Rebuild slides if requested
    if args.rebuild_slides:
        print("Rebuilding slides...")
        result = subprocess.run(['make', 'build-slides'], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Failed to rebuild slides:\n{result.stderr}")
            sys.exit(1)
        print("✅ Slides rebuilt\n")

    # Get list of topics
    if args.all:
        topics_dir = Path('topics')
        topics = sorted([d.name for d in topics_dir.iterdir() if d.is_dir()])
    else:
        topics = [args.topic]

    # Sync each topic
    successes = 0
    failures = 0

    for topic in topics:
        print(f"\n{'='*60}")
        print(f"Topic: {topic}")
        print('='*60)

        result = sync_topic(topic, args.training_material_root, args.dry_run)

        if result['error']:
            print(f"\n❌ Error: {result['error']}")
            failures += 1
            continue

        # Show slides sync result
        if result['slides_copied']:
            print(f"\n✅ Slides synced to: {result['target_dir']}")
        else:
            print(f"\n⚠️  Slides not copied")

        # Show images sync result
        img_result = result['images_result']
        if img_result:
            if img_result['copied']:
                print(f"   Images copied: {len(img_result['copied'])}")
            if img_result['skipped']:
                print(f"   Images skipped: {len(img_result['skipped'])}")
            if img_result['missing']:
                print(f"   ⚠️ Images missing: {len(img_result['missing'])}")
                for name in img_result['missing']:
                    print(f"      - {name}")

        successes += 1

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    print(f"Topics synced: {successes}/{len(topics)}")
    if failures:
        print(f"Failures: {failures}")

    if args.dry_run:
        print("\n(DRY RUN - no files were actually copied)")
    else:
        print(f"\nNext steps:")
        print(f"1. cd {args.training_material_root}")
        print(f"2. git status")
        print(f"3. git diff topics/dev/tutorials/architecture-*/slides.html")
        print(f"4. Review changes and commit if satisfied")


if __name__ == '__main__':
    main()
