#!/usr/bin/env python3
"""
Sphinx Output Image Linter

Scans built Sphinx HTML output to find missing/broken image references.
Parses HTML files and checks if all referenced images exist.

Usage:
    python scripts/sphinx_image_linter.py [--verbose] [--html-dir doc/build/html]

Output:
    - Summary of missing images by location
    - Total count of broken references
    - Suggestions for fixes
"""

import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from html.parser import HTMLParser
from urllib.parse import urlparse


class ImageExtractor(HTMLParser):
    """Extract image references from HTML."""

    def __init__(self):
        super().__init__()
        self.images = []  # List of (src, context)
        self.current_file = None

    def set_file(self, filepath):
        self.current_file = filepath

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr, value in attrs:
                if attr == 'src':
                    self.images.append((value, self.current_file))


def extract_images_from_html(html_file: Path) -> List[Tuple[str, Path]]:
    """Extract all image references from an HTML file."""
    try:
        content = html_file.read_text(errors='ignore')
    except Exception as e:
        print(f"  Error reading {html_file}: {e}", file=sys.stderr)
        return []

    parser = ImageExtractor()
    parser.set_file(html_file)
    try:
        parser.feed(content)
    except Exception as e:
        print(f"  Error parsing {html_file}: {e}", file=sys.stderr)

    return [(src, html_file) for src, _ in parser.images]


def is_external_url(src: str) -> bool:
    """Check if src is an external URL."""
    return src.startswith(('http://', 'https://', 'data:', 'blob:'))


def resolve_image_path(html_file: Path, src: str, html_root: Path) -> Path:
    """
    Resolve relative image path to absolute path on filesystem.

    Args:
        html_file: Path to HTML file containing image reference
        src: Image src attribute value
        html_root: Root of HTML output directory

    Returns:
        Absolute path where image should exist
    """
    # Remove query params and fragments
    src = src.split('?')[0].split('#')[0]

    if src.startswith('/'):
        # Absolute path from HTML root
        return (html_root / src.lstrip('/')).resolve()
    else:
        # Relative path from HTML file directory
        html_dir = html_file.parent
        resolved = (html_dir / src).resolve()

        # Ensure the resolved path is within html_root (or reasonably close)
        # If it resolves outside html_root, it's a broken reference
        return resolved


def lint_sphinx_output(html_root: Path = None, verbose: bool = False) -> Dict:
    """
    Scan Sphinx HTML output for missing images.

    Args:
        html_root: Root of built HTML (default: doc/build/html)
        verbose: Show all image references, not just missing ones

    Returns:
        Dict with results including missing_images, total_images, by_directory
    """
    if html_root is None:
        html_root = Path("doc/build/html")

    # Always convert to absolute path
    html_root = html_root.resolve()

    if not html_root.exists():
        print(f"Error: HTML root not found: {html_root}")
        return {"error": f"HTML root not found: {html_root}"}

    print(f"Scanning HTML in: {html_root}")
    print()

    # Find all HTML files
    html_files = list(html_root.rglob("*.html"))
    print(f"Found {len(html_files)} HTML files")

    # Extract all images
    all_images: List[Tuple[str, Path]] = []
    for html_file in html_files:
        images = extract_images_from_html(html_file)
        all_images.extend(images)

    print(f"Found {len(all_images)} image references\n")

    # Check which exist
    missing_images: List[Dict] = []
    image_dirs: Dict[str, List[Dict]] = {}

    for src, html_file in all_images:
        if is_external_url(src):
            if verbose:
                print(f"  ✓ {src} (external)")
            continue

        resolved_path = resolve_image_path(html_file, src, html_root)
        exists = resolved_path.exists()

        # Extract directory for categorization (safely handle paths outside html_root)
        try:
            image_dir = str(resolved_path.parent.relative_to(html_root))
        except ValueError:
            # Path is outside html_root
            image_dir = str(resolved_path.parent)

        if image_dir not in image_dirs:
            image_dirs[image_dir] = []

        result = {
            "src": src,
            "html_file": html_file,
            "resolved_path": resolved_path,
            "exists": exists,
            "relative_html": html_file.relative_to(html_root),
        }

        image_dirs[image_dir].append(result)

        if not exists:
            missing_images.append(result)
            if verbose:
                print(f"  ✗ {src}")
                print(f"    HTML: {html_file.relative_to(html_root)}")
                print(f"    Expected: {resolved_path.relative_to(html_root)}")
        elif verbose:
            print(f"  ✓ {src}")

    return {
        "html_root": html_root,
        "total_images": len(all_images),
        "missing_images": missing_images,
        "missing_count": len(missing_images),
        "image_dirs": image_dirs,
    }


def print_report(results: Dict, verbose: bool = False):
    """Print formatted report of linter results."""
    if "error" in results:
        print(f"Error: {results['error']}")
        return

    print("=" * 70)
    print("SPHINX IMAGE LINTER REPORT")
    print("=" * 70)
    print()

    total = results["total_images"]
    missing = results["missing_count"]

    if missing == 0:
        print(f"✓ All {total} image references are valid!")
        print()
        return

    print(f"Found {missing} missing images out of {total} references")
    print()

    if missing > 0:
        print("MISSING IMAGES:")
        print("-" * 70)

        # Group by directory for clarity
        by_dir: Dict[str, List] = {}
        for img in results["missing_images"]:
            try:
                dir_path = str(img["resolved_path"].parent.relative_to(results["html_root"]))
            except ValueError:
                # Outside html_root
                dir_path = str(img["resolved_path"].parent)
            if dir_path not in by_dir:
                by_dir[dir_path] = []
            by_dir[dir_path].append(img)

        for dir_name in sorted(by_dir.keys()):
            images = by_dir[dir_name]
            print(f"\n{dir_name}/ ({len(images)} missing)")
            for img in sorted(images, key=lambda x: x["src"]):
                print(f"  • {img['src']}")
                print(f"    Referenced in: {img['relative_html']}")
                try:
                    expected_path = img['resolved_path'].relative_to(results['html_root'])
                except ValueError:
                    expected_path = img['resolved_path']
                print(f"    Expected at:  {expected_path}")

        print()
        print("-" * 70)
        print()

        # Analyze patterns
        print("ANALYSIS:")
        print()

        # Group by src pattern
        src_patterns: Dict[str, int] = {}
        for img in results["missing_images"]:
            # Extract directory from src
            src_dir = img["src"].split('/')[0] if '/' in img["src"] else 'root'
            src_patterns[src_dir] = src_patterns.get(src_dir, 0) + 1

        print("Missing by source directory:")
        for pattern in sorted(src_patterns.keys()):
            count = src_patterns[pattern]
            pct = (count / missing) * 100
            print(f"  {pattern:15} {count:3} images  ({pct:5.1f}%)")

        print()
        print("SUGGESTIONS:")
        print()

        # Check if images are in different locations
        images_dir = results["html_root"] / "images"
        images_underscore_dir = results["html_root"] / "_images"

        if images_dir.exists():
            images_in_dir = list(images_dir.glob("*"))
            print(f"  • Found {len(images_in_dir)} files in {images_dir.relative_to(results['html_root'])}/")

        if images_underscore_dir.exists():
            images_in_underscore = list(images_underscore_dir.glob("*"))
            print(f"  • Found {len(images_in_underscore)} files in {images_underscore_dir.relative_to(results['html_root'])}/")

        print()

        # Suggest what files are missing
        missing_filenames = set()
        for img in results["missing_images"]:
            filename = Path(img["src"]).name
            missing_filenames.add(filename)

        if missing_filenames:
            print(f"  Missing {len(missing_filenames)} unique filenames:")
            for filename in sorted(missing_filenames):
                print(f"    - {filename}")

        print()

    print("=" * 70)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Lint Sphinx HTML output for missing images"
    )
    parser.add_argument(
        "--html-dir",
        type=Path,
        default=Path("doc/build/html"),
        help="Path to built HTML directory (default: doc/build/html)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show all images, not just missing ones"
    )

    args = parser.parse_args()

    results = lint_sphinx_output(html_root=args.html_dir, verbose=args.verbose)
    print_report(results, verbose=args.verbose)

    # Exit with error code if images are missing
    sys.exit(0 if results.get("missing_count", 0) == 0 else 1)


if __name__ == "__main__":
    main()
