#!/usr/bin/env python3
"""
Validate that all referenced images exist and copy missing ones from training-material.

Usage:
    python scripts/validate_images.py [--copy] [--verbose]

Options:
    --copy      Actually copy missing images (dry-run by default)
    --verbose   Show detailed information
"""

import sys
import re
from pathlib import Path
from typing import Set, Dict, List

# Add scripts to path for models import
sys.path.insert(0, str(Path(__file__).parent))

from models import load_content


def extract_image_paths(markdown: str) -> Set[str]:
    """Extract all image paths from markdown content.

    Returns set of image paths like:
    - "../../images/docker-chart.png"
    - "../../../../images/app_py2.plantuml.svg"
    - "{{ site.baseurl }}/assets/images/GTNLogo1000.png"
    """
    paths = set()

    # Pattern: ![alt](path/to/image)
    pattern = r'!\[[^\]]*\]\(([^)]+)\)'
    matches = re.findall(pattern, markdown)

    for match in matches:
        # Skip external URLs
        if match.startswith(('http://', 'https://', 'data:')):
            continue
        paths.add(match)

    return paths


def categorize_image_path(path: str) -> tuple[str, str]:
    """Categorize image path and extract filename.

    Returns: (category, filename) where category is one of:
    - "dev_images" for ../../images/...
    - "shared_images" for {{ site.baseurl }}/...
    - "project_images" for ../../../../images/...
    """
    filename = Path(path).name

    if '{{ site.baseurl }}' in path:
        return ("shared_images", filename)
    elif path.startswith('../../images/'):
        return ("dev_images", filename)
    elif path.startswith('../../../../'):
        return ("project_images", filename)
    else:
        return ("unknown", filename)


def find_missing_images(verbose: bool = False) -> Dict[str, List[str]]:
    """Scan all topics and find missing images.

    Returns dict mapping image category to list of missing filenames.
    """
    missing = {
        "dev_images": [],
        "shared_images": [],
        "project_images": [],
        "unknown": []
    }

    images_dir = Path("images")
    topics_dir = Path("topics")

    # Collect all referenced images
    all_paths: Dict[str, Set[str]] = {
        "dev_images": set(),
        "shared_images": set(),
        "project_images": set(),
        "unknown": set()
    }

    for topic_dir in topics_dir.glob("*/"):
        try:
            content = load_content(topic_dir.name)

            for block in content.root:
                if block.content:
                    paths = extract_image_paths(block.content)
                    for path in paths:
                        category, filename = categorize_image_path(path)
                        all_paths[category].add(filename)
        except Exception as e:
            if verbose:
                print(f"Warning: Could not load {topic_dir.name}: {e}")

    # Check which images exist
    for category, filenames in all_paths.items():
        for filename in filenames:
            if not (images_dir / filename).exists():
                missing[category].append(filename)

    return missing, all_paths


def copy_from_training_material(copy: bool = False, verbose: bool = False):
    """Copy missing images from training-material repo.

    Args:
        copy: If True, actually copy files. If False, dry-run.
        verbose: Print detailed information.
    """
    training_material = Path.home() / "workspace" / "training-material"

    if not training_material.exists():
        print(f"ERROR: training-material not found at {training_material}")
        return False

    missing, all_referenced = find_missing_images(verbose)

    if not any(missing.values()):
        print("✓ All referenced images exist!")
        return True

    print("\nMissing images by category:")

    # Dev images
    if missing["dev_images"]:
        print(f"\n  Dev images ({len(missing['dev_images'])} missing):")
        source_dir = training_material / "topics" / "dev" / "images"
        for filename in sorted(missing["dev_images"]):
            source = source_dir / filename
            dest = Path("images") / filename
            status = "✓" if source.exists() else "✗"
            print(f"    {status} {filename}")

            if copy and source.exists():
                dest.write_bytes(source.read_bytes())
                if verbose:
                    print(f"      → copied to {dest}")

    # Shared images
    if missing["shared_images"]:
        print(f"\n  Shared images ({len(missing['shared_images'])} missing):")
        source_dir = training_material / "shared" / "images"
        for filename in sorted(missing["shared_images"]):
            source = source_dir / filename
            dest = Path("images") / filename
            status = "✓" if source.exists() else "✗"
            print(f"    {status} {filename}")

            if copy and source.exists():
                dest.write_bytes(source.read_bytes())
                if verbose:
                    print(f"      → copied to {dest}")

    # Project images (should exist locally)
    if missing["project_images"]:
        print(f"\n  Project images ({len(missing['project_images'])} missing locally!):")
        for filename in sorted(missing["project_images"]):
            print(f"    ✗ {filename} (not found in ./images/)")
            print(f"      This image is referenced but missing from the project!")

    if missing["unknown"]:
        print(f"\n  Unknown path format ({len(missing['unknown'])} items):")
        for filename in sorted(missing["unknown"]):
            print(f"    ? {filename}")

    if copy:
        total_copied = sum(len(v) for k, v in missing.items() if k != "unknown")
        print(f"\n✓ Copied {total_copied} missing images")
        return True
    else:
        print("\n(Run with --copy to actually copy files)")
        return False


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate images referenced in content and copy missing ones"
    )
    parser.add_argument("--copy", action="store_true", help="Actually copy missing images")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    success = copy_from_training_material(copy=args.copy, verbose=args.verbose)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
