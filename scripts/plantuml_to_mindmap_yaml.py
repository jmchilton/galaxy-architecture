#!/usr/bin/env python3
"""Convert PlantUML mindmap files to YAML mindmap format."""

from pathlib import Path
import re
import yaml
from html import unescape


def parse_plantuml_mindmap(content: str) -> dict:
    """Parse PlantUML mindmap and extract structure.

    PlantUML mindmap format:
    * label          (root)
    ** label         (level 1)
    *** label        (level 2)
    etc.

    Each line can have optional :description; after the label.
    Labels can be wrapped in <b><i>text</i></b> for formatting.
    """
    lines = content.strip().split('\n')

    root = None
    stack = []  # Stack of (level, item_dict)

    for line in lines:
        # Skip includes and markers
        if '!include' in line or '@start' in line or '@end' in line:
            continue

        # Count asterisks to determine level
        match = re.match(r'^(\*+)(:\S+)?\s*(.*)', line)
        if not match:
            continue

        level = len(match.group(1))
        label_part = match.group(3).strip()

        # Extract label and description
        # Format: <b><i>label</i></b>\n description;
        # or: label\n description;

        # Remove HTML tags
        label = re.sub(r'<[^>]+>', '', label_part)

        # Description comes after the label, can be on same line or next
        doc = ""
        if ';' in label:
            parts = label.split(';', 1)
            label = parts[0].strip()
            doc = parts[1].strip() if len(parts) > 1 else ""
        else:
            # Description might be on the same line after space
            # PlantUML format: ** label description;
            # Actually looking at the files, description is after newline
            label = label.rstrip(';').strip()

        # Create item
        item = {'label': label}
        if doc:
            item['doc'] = doc

        if level == 1:
            # Root level
            root = item
            stack = [(level, root)]
        else:
            # Pop stack until we find parent level
            while len(stack) > 0 and stack[-1][0] >= level:
                stack.pop()

            if len(stack) > 0:
                parent = stack[-1][1]
                if 'items' not in parent:
                    parent['items'] = []
                parent['items'].append(item)
                stack.append((level, item))

    return root if root else {}


def parse_plantuml_mindmap_v2(content: str) -> dict:
    """Parse PlantUML mindmap with multiline descriptions.

    Handles format where description spans multiple lines until next marker.
    """
    lines = content.strip().split('\n')

    root = None
    stack = []  # Stack of (level, item_dict)
    current_item = None
    current_level = 0

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        i += 1

        # Skip includes and markers
        if not line or '!include' in line or '@start' in line or '@end' in line:
            continue

        # Check if this is a mindmap node line
        if line.startswith('*'):
            # Count asterisks
            match = re.match(r'^(\*+)\s*(.*)', line)
            if not match:
                continue

            level = len(match.group(1))
            rest = match.group(2).strip()

            # Extract label and optional inline doc
            # Format: :<id>label or just label
            # Remove HTML formatting
            rest = re.sub(r'<[^>]+>', '', rest)

            # Split on colon prefix if present
            if ':' in rest and rest[0] != ':':
                # Has an id prefix
                parts = rest.split(':', 1)
                label = parts[1].strip()
            else:
                label = rest.lstrip(':').strip()

            # Decode HTML entities (e.g., &#95; -> _)
            label = unescape(label)

            # Look ahead for description on next line(s)
            doc = ""
            next_i = i
            desc_lines = []
            while next_i < len(lines):
                next_line = lines[next_i].rstrip()
                # Stop if we hit another node (starts with *), marker, or empty line followed by marker
                if next_line.startswith('*') or next_line.startswith('@') or not next_line or '!include' in next_line:
                    break
                # Collect description lines
                desc_lines.append(next_line)
                next_i += 1

            if desc_lines:
                doc = ' '.join(desc_lines).rstrip(';').strip()
                # Clean up any remaining markers
                doc = re.sub(r'\s*@\w+.*', '', doc)
                # Decode HTML entities in doc
                doc = unescape(doc)
                i = next_i  # Skip the description lines we consumed

            # Create item
            item = {'label': label}
            if doc:
                item['doc'] = doc

            if level == 1:
                # Root level
                root = item
                stack = [(level, root)]
            else:
                # Pop stack until we find parent level
                while len(stack) > 0 and stack[-1][0] >= level:
                    stack.pop()

                if len(stack) > 0:
                    parent = stack[-1][1]
                    if 'items' not in parent:
                        parent['items'] = []
                    parent['items'].append(item)
                    stack.append((level, item))

    return root if root else {}


def plantuml_file_to_yaml(input_file: Path, output_file: Path) -> None:
    """Convert PlantUML mindmap file to YAML mindmap format."""
    with open(input_file) as f:
        content = f.read()

    # Parse PlantUML
    data = parse_plantuml_mindmap_v2(content)

    if not data:
        print(f"⚠️  Could not parse {input_file.name}")
        return

    # Write YAML
    with open(output_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"✓ {input_file.name} -> {output_file.name}")


if __name__ == "__main__":
    import sys

    images_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('images')

    # Find all PlantUML mindmap files
    plantuml_files = list(images_dir.glob("*.plantuml.txt"))

    # Filter for ones with @startmindmap
    mindmap_files = []
    for f in plantuml_files:
        with open(f) as file:
            if '@startmindmap' in file.read():
                mindmap_files.append(f)

    # Find ones that don't have a corresponding .mindmap.yml
    yaml_files = {f.stem.replace('.mindmap', '') for f in images_dir.glob("*.mindmap.yml")}

    to_convert = []
    for f in sorted(mindmap_files):
        base = f.stem.replace('.plantuml', '')
        if base not in yaml_files:
            to_convert.append(f)

    if not to_convert:
        print("No PlantUML mindmap files to convert.")
        sys.exit(0)

    print(f"Converting {len(to_convert)} PlantUML mindmap files:\n")

    for input_file in to_convert:
        output_file = input_file.parent / input_file.name.replace('.plantuml.txt', '.mindmap.yml')
        plantuml_file_to_yaml(input_file, output_file)

    print(f"\n✓ Done!")
