#!/usr/bin/env python3
"""Migrate architecture topic slides from training-material into this project.

Usage:
    python scripts/migrate_topic.py "Dependency Injection"
    python scripts/migrate_topic.py "Application Startup"
"""

import re
import sys
import shutil
from pathlib import Path
from typing import Optional
import yaml

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))
from models import TopicMetadata, TrainingMetadata, SphinxMetadata


def kebab_case(text: str) -> str:
    """Convert text to kebab-case."""
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text.lower())
    # Remove any non-alphanumeric characters except hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)
    # Remove consecutive hyphens
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def find_source_directory(topic_name: str) -> Optional[tuple[Path, int]]:
    """Find the architecture-N-* directory matching the topic name.

    Returns tuple of (directory_path, number) or None if not found.
    """
    training_dir = Path.home() / "workspace" / "training-material" / "topics" / "dev" / "tutorials"

    if not training_dir.exists():
        print(f"❌ Training material directory not found: {training_dir}")
        return None

    # Look for architecture-N-* directories
    for arch_dir in sorted(training_dir.glob("architecture-*")):
        if arch_dir.is_dir():
            # Extract number from directory name
            match = re.match(r'architecture-(\d+)-', arch_dir.name)
            if match:
                num = int(match.group(1))
                # Check if this directory matches the topic name
                dir_name = arch_dir.name.lower()
                search_term = topic_name.lower()
                if search_term in dir_name:
                    return arch_dir, num

    print(f"❌ No matching architecture directory found for: {topic_name}")
    print(f"   Searched in: {training_dir}")
    return None


def extract_images_from_slides(slides: list[str]) -> set[str]:
    """Extract image filenames referenced in slides."""
    images = set()

    for slide in slides:
        # Match markdown image syntax: ![alt](path/image.ext)
        matches = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', slide)
        for alt, path in matches:
            # Get just the filename
            filename = Path(path).name
            images.add(filename)

    return images


def copy_images(image_files: set[str], dest_dir: Path) -> list[str]:
    """Copy image files from training-material to topic directory.

    Returns list of files that were copied.
    """
    source_images_dir = Path.home() / "workspace" / "training-material" / "topics" / "dev" / "images"
    copied = []

    if not source_images_dir.exists():
        print(f"⚠️  Source images directory not found: {source_images_dir}")
        return copied

    for image_file in image_files:
        source = source_images_dir / image_file
        if source.exists():
            shutil.copy2(source, dest_dir / image_file)
            copied.append(image_file)
        else:
            print(f"⚠️  Image not found: {image_file}")

    return copied


def extract_frontmatter(slide: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from a slide.

    Handles both --- delimited and plain YAML at start of slide.
    Returns tuple of (frontmatter_dict, remaining_content).
    """
    import yaml as yaml_lib

    data = {}
    remaining = slide

    # Try to match YAML frontmatter with --- delimiters first
    match = re.match(r'^---?\s*\n(.*?)\n---?\s*\n(.*)', slide, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        remaining = match.group(2)
        try:
            data = yaml_lib.safe_load(yaml_content) or {}
        except:
            return {}, slide
        return data, remaining

    # Try plain YAML at start (no delimiters)
    # Remark.js puts YAML at the start, look for it before markdown content
    lines = slide.split('\n')
    yaml_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Empty lines are ok in YAML
        if stripped == '':
            yaml_lines.append(line)
        # Lines with ':' are YAML (key: value or list items)
        elif ':' in line or line.startswith('  -'):
            # This looks like YAML or list continuation
            yaml_lines.append(line)
        # Comments are ok
        elif stripped.startswith('#'):
            yaml_lines.append(line)
        # If we hit a line that doesn't look like YAML, stop
        else:
            # This is where content starts
            break

    if yaml_lines:
        yaml_content = '\n'.join(yaml_lines).strip()
        if yaml_content:
            try:
                data = yaml_lib.safe_load(yaml_content) or {}
                # Remaining content is after YAML
                remaining = '\n'.join(lines[len(yaml_lines):])
            except:
                return {}, slide

            return data, remaining

    return data, remaining


def create_content_blocks(slides: list[str], frontmatter: dict) -> list[dict]:
    """Convert slides to content.yaml block format.

    Skips the first slide if it's frontmatter, starts from actual content.
    Returns list of content block dictionaries.
    """
    blocks = []
    start_idx = 0

    # Skip first slide if it's just metadata/frontmatter
    if slides and ('layout' in slides[0] or 'questions' in slides[0] or 'title' in slides[0]):
        # First slide is likely Remark.js metadata, skip it
        start_idx = 1

    for i, slide in enumerate(slides[start_idx:], start=start_idx):
        if not slide.strip():
            continue

        # Extract heading from slide (first # heading or ## heading)
        heading_match = re.search(r'^#+\s+(.+?)$', slide, re.MULTILINE)
        heading = heading_match.group(1).strip() if heading_match else f"Slide {i+1}"

        # Generate ID from heading
        block_id = kebab_case(heading)

        # Ensure unique ID
        base_id = block_id
        counter = 1
        for existing_block in blocks:
            if existing_block['id'] == block_id:
                block_id = f"{base_id}-{counter}"
                counter += 1

        block = {
            'type': 'slide',
            'id': block_id,
            'heading': heading,
            'content': slide,
        }

        blocks.append(block)

    return blocks


def create_metadata(topic_name: str, topic_id: str, num: int, frontmatter: dict) -> dict:
    """Create metadata.yaml structure.

    Uses extracted frontmatter from slides if available.
    """
    # Extract training metadata from frontmatter
    questions = frontmatter.get('questions', [])
    objectives = frontmatter.get('objectives', [])
    key_points = frontmatter.get('key_points', [])
    time_estimation = frontmatter.get('time_estimation', '30m')

    # Ensure these are lists
    if isinstance(questions, str):
        questions = [questions]
    if isinstance(objectives, str):
        objectives = [objectives]
    if isinstance(key_points, str):
        key_points = [key_points]

    return {
        'topic_id': topic_id,
        'title': topic_name,
        'training': {
            'questions': questions or [f"What is {topic_name}?"],
            'objectives': objectives or [f"Understand {topic_name}"],
            'key_points': key_points or [f"Key concept about {topic_name}"],
            'time_estimation': time_estimation,
        },
        'sphinx': {
            'section': 'Architecture',
            'subsection': topic_name,
        },
        'related_topics': [],
        'related_code_paths': [],
    }


def create_claude_context(topic_name: str, topic_id: str, source_num: int) -> str:
    """Create template .claude/CLAUDE.md for the topic."""
    return f"""# {topic_name}

Architecture documentation for Galaxy's {topic_name.lower()}.

## Content

This topic covers {topic_name.lower()} patterns and practices in Galaxy.

## Key Files

- `lib/galaxy/` - Implementation details
- Related modules and components

## How to Update

1. Edit `content.yaml` to add, remove, or reorder slides
2. Update slide content inline or in fragments/
3. Update metadata.yaml if learning objectives change
4. Run `make validate` to check structure
5. Run `make build-sphinx` to regenerate docs

## Common Questions

(To be filled in by contributors)

## References

- Original slides: architecture-{source_num}-{topic_id}
- Galaxy documentation: https://docs.galaxyproject.org/
"""


def migrate_topic(topic_name: str) -> bool:
    """Main migration function.

    Returns True if successful, False otherwise.
    """
    print(f"\n🚀 Migrating: {topic_name}")

    # Find source directory
    source_info = find_source_directory(topic_name)
    if not source_info:
        return False

    source_dir, arch_num = source_info
    print(f"✓ Found source: {source_dir.name}")

    # Generate topic ID from topic name
    topic_id = kebab_case(topic_name)
    print(f"✓ Topic ID: {topic_id}")

    # Create topic directory
    topic_path = Path("topics") / topic_id
    if topic_path.exists():
        print(f"❌ Topic directory already exists: {topic_path}")
        return False

    topic_path.mkdir(parents=True)
    print(f"✓ Created directory: {topic_path}")

    # Extract slides
    slides_file = source_dir / "slides.html"
    try:
        raw_content = slides_file.read_text()
        # Extract textarea content which contains the markdown
        textarea_match = re.search(r'<textarea[^>]*>(.*?)</textarea>', raw_content, re.DOTALL)
        if textarea_match:
            markdown = textarea_match.group(1)
        else:
            markdown = raw_content

        # Split by --- separator (Remark.js slide separator)
        all_slides = markdown.split('---')

        # First slide (before first ---) is usually empty, next slide is frontmatter
        slides = [s.strip() for s in all_slides if s.strip()]
        print(f"✓ Extracted {len(slides)} slides")
    except Exception as e:
        print(f"❌ Error extracting slides: {e}")
        shutil.rmtree(topic_path)
        return False

    # Extract frontmatter from first non-empty slide
    frontmatter = {}
    if slides:
        frontmatter, _ = extract_frontmatter(slides[0])

    # Extract and copy images
    image_files = extract_images_from_slides(slides)
    if image_files:
        copied = copy_images(image_files, Path("images"))
        print(f"✓ Copied {len(copied)} images")
        if len(copied) < len(image_files):
            print(f"⚠️  {len(image_files) - len(copied)} images not found")

    # Create content blocks (skips frontmatter slide if present)
    content_blocks = create_content_blocks(slides, frontmatter)

    # Write content.yaml
    content_yaml_path = topic_path / "content.yaml"
    with open(content_yaml_path, 'w') as f:
        yaml.dump(content_blocks, f, default_flow_style=False, sort_keys=False)
    print(f"✓ Created: {content_yaml_path}")

    # Write metadata.yaml
    metadata = create_metadata(topic_name, topic_id, arch_num, frontmatter)
    metadata_yaml_path = topic_path / "metadata.yaml"
    with open(metadata_yaml_path, 'w') as f:
        yaml.dump(metadata, f, default_flow_style=False, sort_keys=False)
    print(f"✓ Created: {metadata_yaml_path}")

    # Create .claude directory and CLAUDE.md
    claude_dir = topic_path / ".claude"
    claude_dir.mkdir()
    claude_md = create_claude_context(topic_name, topic_id, arch_num)
    (claude_dir / "CLAUDE.md").write_text(claude_md)
    print(f"✓ Created: {claude_dir / 'CLAUDE.md'}")

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/migrate_topic.py '<Topic Name>'")
        print("Example: python scripts/migrate_topic.py 'Dependency Injection'")
        sys.exit(1)

    topic_name = sys.argv[1]

    success = migrate_topic(topic_name)

    if success:
        print(f"\n✅ Migration complete!")
        print(f"\nNext steps:")
        print(f"1. Review the generated files in topics/<topic-id>/")
        print(f"2. Run: make validate")
        print(f"3. Fix any validation errors")
        print(f"4. Run: make build-sphinx")
        print(f"5. Update .claude/CLAUDE.md with detailed context")
        sys.exit(0)
    else:
        print(f"\n❌ Migration failed")
        sys.exit(1)
