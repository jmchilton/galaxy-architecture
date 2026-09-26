#!/usr/bin/env python3
"""Check that file paths in file-structure mindmaps exist in a Galaxy checkout.

Only mindmaps with 'files' in the name are checked; conceptual mindmaps
(e.g. core_plugins_overview.mindmap.yml) don't describe real paths.

Usage:
    GALAXY_ROOT=~/src/galaxy uv run python scripts/check_mindmap_paths.py
    uv run python scripts/check_mindmap_paths.py --galaxy-root ~/src/galaxy
"""

import argparse
import sys
from pathlib import Path
from typing import Iterator, Optional

import yaml

from repo_roots import RepoRootError, resolve_galaxy_root

# Mindmap placeholder for "and more"
ELLIPSIS = "..."


def _item_paths(items: list, prefix: str) -> Iterator[str]:
    for item in items:
        if isinstance(item, str):
            label, children = item, []
        else:
            label, children = item.get('label', ''), item.get('items', [])
        if label == ELLIPSIS:
            continue
        path = '/'.join(p for p in f"{prefix}/{label}".split('/') if p)
        yield path
        yield from _item_paths(children, path)


def mindmap_paths(mindmap: Optional[dict]) -> list[str]:
    """Paths of all entries in a parsed mindmap, relative to the Galaxy root."""
    if not mindmap:
        return []
    return list(_item_paths(mindmap.get('items', []), mindmap.get('label', '/')))


def check_mindmaps(images_dir: Path, galaxy_root: Path) -> dict[str, list[str]]:
    """Map each file-structure mindmap name to the paths missing from galaxy_root."""
    missing = {}
    for mindmap_file in sorted(images_dir.glob("*files*.mindmap.yml")):
        paths = mindmap_paths(yaml.safe_load(mindmap_file.read_text()))
        gone = [p for p in paths if not (galaxy_root / p).exists()]
        if gone:
            missing[mindmap_file.name] = gone
    return missing


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--images-dir', type=Path, default=Path('images'))
    parser.add_argument('--galaxy-root', type=Path, help='Galaxy checkout (default: $GALAXY_ROOT)')
    args = parser.parse_args()

    try:
        galaxy_root = resolve_galaxy_root(args.galaxy_root)
    except RepoRootError as e:
        print(f"❌ {e}")
        sys.exit(1)

    missing = check_mindmaps(args.images_dir, galaxy_root)
    for name, paths in missing.items():
        print(f"{name}:")
        for path in paths:
            print(f"  ⚠️  Not found: {path}")
    if missing:
        sys.exit(1)
    print(f"✓ All mindmap paths exist in {galaxy_root}")


if __name__ == "__main__":
    main()
