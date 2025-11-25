#!/usr/bin/env python3
"""
Compare generated slides with training-material slides.

Usage:
    uv run python scripts/compare_slides.py ecosystem
    uv run python scripts/compare_slides.py --all
"""

import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import Optional

import yaml

# Add scripts to path for models
sys.path.insert(0, str(Path(__file__).parent))
from models import load_metadata


def extract_markdown_from_html(html_path: Path) -> str:
    """Extract markdown content from RemarkJS HTML file or Jekyll markdown."""
    if not html_path.exists():
        return ""

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if this is a Jekyll markdown file (starts with ---)
    if content.strip().startswith('---'):
        # Extract content after second ---
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2].strip()

    # Otherwise, it's RemarkJS HTML - extract from textarea
    # Use regex to find: <textarea id="source">...</textarea>
    match = re.search(r'<textarea[^>]*id=["\']source["\'][^>]*>(.*?)</textarea>', content, re.DOTALL)
    if match:
        # Unescape HTML entities
        markdown = match.group(1)
        markdown = markdown.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        return markdown

    return ""


def extract_front_matter(html_path: Path) -> dict:
    """Parse YAML front matter from GTN slides HTML or Jekyll markdown."""
    if not html_path.exists():
        return {}

    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Look for YAML front matter between --- markers (at start of file)
    match = re.search(r'^---\s*\n(.*?)\n---', content, re.MULTILINE | re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return {}

    return {}


def count_slides(markdown: str) -> int:
    """Count number of slides in markdown (separated by ---)."""
    if not markdown:
        return 0
    return len([s.strip() for s in markdown.split('\n---\n') if s.strip()])


def compare_front_matter(ours: dict, theirs: dict) -> list[str]:
    """Compare front matter and return list of differences."""
    changes = []

    # Handle empty dicts
    if not ours and not theirs:
        return ["  Both have no front matter"]
    if not ours:
        return ["  Our slides have no front matter (embedded in HTML)"]
    if not theirs:
        return ["  Their slides have no front matter"]

    # Check for added/removed keys
    our_keys = set(ours.keys() if isinstance(ours, dict) else [])
    their_keys = set(theirs.keys() if isinstance(theirs, dict) else [])

    added = our_keys - their_keys
    removed = their_keys - our_keys
    common = our_keys & their_keys

    if added:
        changes.append(f"  Added keys: {', '.join(sorted(added))}")
    if removed:
        changes.append(f"  Removed keys: {', '.join(sorted(removed))}")

    # Check for modified values
    for key in sorted(common):
        our_val = ours[key]
        their_val = theirs[key]

        if our_val != their_val:
            # For lists, show more detail
            if isinstance(our_val, list) and isinstance(their_val, list):
                if len(our_val) != len(their_val):
                    changes.append(f"  {key}: {len(their_val)} items → {len(our_val)} items")
                else:
                    changes.append(f"  {key}: Modified")
            else:
                # Truncate long values
                our_str = str(our_val)[:50]
                their_str = str(their_val)[:50]
                changes.append(f"  {key}: {their_str!r} → {our_str!r}")

    return changes


def generate_unified_diff(ours: str, theirs: str, topic_id: str) -> str:
    """Generate unified diff between two markdown strings."""
    ours_lines = ours.splitlines(keepends=True)
    theirs_lines = theirs.splitlines(keepends=True)

    diff = difflib.unified_diff(
        theirs_lines,
        ours_lines,
        fromfile=f'training-material/{topic_id}',
        tofile=f'galaxy-architecture/{topic_id}',
        lineterm=''
    )

    return ''.join(diff)


def compare_topics(topic_id: str, training_material_root: Path) -> None:
    """Compare single topic and print report."""
    print(f"\n{'='*60}")
    print(f"Topic: {topic_id}")
    print('='*60)

    # Load our metadata
    metadata = load_metadata(topic_id)
    tutorial_num = metadata.training.tutorial_number

    # Find paths
    our_slides = Path(f"outputs/training-slides/generated/architecture-{topic_id}/slides.html")
    their_dir = training_material_root / f"topics/dev/tutorials/architecture-{tutorial_num}-{topic_id}"
    their_slides = their_dir / "slides.html"

    # Check files exist
    if not our_slides.exists():
        print(f"⚠️  Our slides not found: {our_slides}")
        print("   Run: make build-slides")
        return

    if not their_slides.exists():
        print(f"⚠️  Training-material slides not found: {their_slides}")
        return

    # Extract content
    our_markdown = extract_markdown_from_html(our_slides)
    their_markdown = extract_markdown_from_html(their_slides)

    our_front_matter = extract_front_matter(our_slides)
    their_front_matter = extract_front_matter(their_slides)

    # Compare slide counts
    our_count = count_slides(our_markdown)
    their_count = count_slides(their_markdown)

    print(f"\nSLIDE COUNT:")
    if our_count != their_count:
        print(f"  {their_count} → {our_count} slides (Δ {our_count - their_count:+d})")
    else:
        print(f"  {our_count} slides (no change)")

    # Compare front matter
    print(f"\nFRONT MATTER CHANGES:")
    fm_changes = compare_front_matter(our_front_matter, their_front_matter)
    if fm_changes:
        for change in fm_changes:
            print(change)
    else:
        print("  No changes")

    # Show markdown diff
    print(f"\nMARKDOWN DIFF:")
    diff = generate_unified_diff(our_markdown, their_markdown, topic_id)
    if diff:
        # Limit diff output
        diff_lines = diff.split('\n')
        if len(diff_lines) > 50:
            print('\n'.join(diff_lines[:25]))
            print(f"\n  ... ({len(diff_lines) - 50} more lines) ...\n")
            print('\n'.join(diff_lines[-25:]))
        else:
            print(diff)
    else:
        print("  No differences")


def main():
    parser = argparse.ArgumentParser(description='Compare slides with training-material')
    parser.add_argument('topic', nargs='?', help='Topic ID to compare')
    parser.add_argument('--all', action='store_true', help='Compare all topics')
    parser.add_argument(
        '--training-material-root',
        type=Path,
        default=Path.home() / 'workspace' / 'training-material',
        help='Path to training-material repository'
    )

    args = parser.parse_args()

    if not args.all and not args.topic:
        parser.error("Either specify a topic or use --all")

    if not args.training_material_root.exists():
        print(f"❌ Training-material not found: {args.training_material_root}")
        sys.exit(1)

    # Get list of topics
    if args.all:
        topics_dir = Path('topics')
        topics = sorted([d.name for d in topics_dir.iterdir() if d.is_dir()])
    else:
        topics = [args.topic]

    # Compare each topic
    for topic in topics:
        try:
            compare_topics(topic, args.training_material_root)
        except Exception as e:
            print(f"\n❌ Error comparing {topic}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n{'='*60}")
    print(f"Compared {len(topics)} topic(s)")
    print('='*60)


if __name__ == '__main__':
    main()
