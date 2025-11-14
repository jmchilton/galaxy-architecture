#!/usr/bin/env python3
"""Generate prose blocks with file links for architecture documentation.

Parses YAML mindmap files that describe Galaxy's file structure,
verifies files exist in ~/workspace/galaxy, and generates prose blocks
with links to GitHub for the architecture slides.
"""

from pathlib import Path
import yaml


def parse_mindmap_yaml_items(items: list, prefix: str = "") -> dict[str, str]:
    """Recursively parse items from mindmap YAML."""
    files = {}

    for item in items:
        # Handle both dict items and string items
        if isinstance(item, str):
            # Simple string item without documentation
            item_label = item
            item_doc = ""
        else:
            item_label = item.get('label', '')
            item_doc = item.get('doc', '')

        item_path = f"{prefix}/{item_label}".lstrip('/')

        if item_doc:
            files[item_path] = item_doc

        # Recursively process sub-items (only dict items can have sub-items)
        if isinstance(item, dict) and 'items' in item:
            sub_files = parse_mindmap_yaml_items(item['items'], item_path)
            files.update(sub_files)

    return files


def parse_mindmap_yaml(filepath: str) -> dict[str, str]:
    """Parse YAML mindmap file and extract file paths with descriptions.

    Returns dict of {file_path: description}
    """
    files = {}

    with open(filepath) as f:
        data = yaml.safe_load(f)

    if not data:
        return files

    label = data.get('label', '/')
    current_path = label.lstrip('/')

    # Parse items at this level
    files.update(parse_mindmap_yaml_items(data.get('items', []), current_path))

    return files


def verify_files_in_galaxy(files: dict[str, str]) -> dict[str, str]:
    """Verify files exist in ~/workspace/galaxy and return verified files."""
    galaxy_root = Path.home() / 'workspace' / 'galaxy'
    verified = {}

    for filepath, description in files.items():
        full_path = galaxy_root / filepath
        if full_path.exists():
            verified[filepath] = description
        else:
            print(f"⚠️  Not found: {filepath}")

    return verified


def generate_prose_block(slide_id: str, files: dict[str, str]) -> str:
    """Generate YAML prose block with file links."""
    if not files:
        return ""

    block = f"""- type: prose
  id: {slide_id}-files
  content: |-
    **Files:**
"""

    for filepath, description in sorted(files.items()):
        github_url = f"https://github.com/galaxyproject/galaxy/blob/dev/{filepath}"
        line = f"    - [{filepath}]({github_url})"
        if description:
            line += f" - {description}"
        block += line + "\n"

    return block


def process_mindmap_files(images_dir: str) -> None:
    """Process file-related mindmap files and generate prose blocks.

    Only processes mindmaps with 'files' in the name to exclude conceptual
    diagrams like core_plugins_overview.mindmap.yml.
    """
    images_path = Path(images_dir)

    # Only process mindmaps with "files" in the name
    mindmap_files = list(images_path.glob("*files*.mindmap.yml"))
    print(f"Found {len(mindmap_files)} file-related mindmap files\n")

    for mindmap_file in sorted(mindmap_files):
        print(f"Processing {mindmap_file.name}...")

        # Parse mindmap
        files = parse_mindmap_yaml(str(mindmap_file))
        print(f"  Found {len(files)} files/directories")

        # Verify in Galaxy
        verified = verify_files_in_galaxy(files)
        print(f"  Verified {len(verified)} in ~/workspace/galaxy")

        # Generate prose block
        slide_id = mindmap_file.stem.replace('.mindmap', '')
        prose = generate_prose_block(slide_id, verified)

        if prose:
            print(f"\nGenerated prose block for {slide_id}:\n")
            print(prose)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generate_files_prose.py <images_dir>")
        print("Example: python generate_files_prose.py images/")
        sys.exit(1)

    process_mindmap_files(sys.argv[1])
