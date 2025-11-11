#!/usr/bin/env python3
"""Generate Sphinx markdown documentation from topic content.

Usage:
    python outputs/sphinx-docs/build.py dependency-injection
    python outputs/sphinx-docs/build.py all
"""

import sys
import shutil
from pathlib import Path
from typing import Optional

# Add scripts to path so we can import models
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from models import load_metadata, load_content, ContentBlockType


def process_markdown_for_sphinx(markdown: str, topic_id: str) -> str:
    """Process markdown for Sphinx compatibility.

    - Fix image paths (../../images/ -> ../_images/)
    - Convert bare URLs to markdown links
    """
    import re

    # Fix image paths: ../../images/ becomes ../_images/
    # This assumes doc/source/architecture/ and images at doc/source/_images/
    markdown = markdown.replace("../../images/", "../_images/")

    # Convert bare URLs (lines that are just a URL) to markdown links
    # Pattern: lines that contain only https://... or http://...
    lines = markdown.split('\n')
    processed_lines = []

    for line in lines:
        stripped = line.strip()
        # Match lines that are just a URL (possibly with leading/trailing whitespace)
        if stripped and re.match(r'^https?://', stripped) and not line.strip().startswith('['):
            # Convert to markdown link format: [URL](URL)
            processed_lines.append(f"[{stripped}]({stripped})")
        else:
            processed_lines.append(line)

    return '\n'.join(processed_lines)


def get_block_content(block, topic_dir: Path) -> str:
    """Extract content from a block, handling all content sources."""
    if block.content:
        return block.content

    if block.file:
        file_path = topic_dir / block.file
        if file_path.exists():
            return file_path.read_text()
        else:
            return f"[Error: File not found: {block.file}]"

    if block.fragments:
        parts = []
        for fragment in block.fragments:
            fragment_path = topic_dir / fragment
            if fragment_path.exists():
                parts.append(fragment_path.read_text())
            else:
                parts.append(f"[Error: Fragment not found: {fragment}]")
        return block.separator.join(parts)

    return ""


def generate_topic_markdown(topic_id: str, topic_dir: Path) -> str:
    """Generate markdown for a single topic.

    Args:
        topic_id: Topic identifier
        topic_dir: Path to topic directory

    Returns:
        Generated markdown content
    """
    # Load metadata and content
    metadata, content = load_metadata(topic_id), load_content(topic_id)

    # Start with title
    lines = [f"# {metadata.title}"]
    lines.append("")

    # Add overview if metadata has description
    if metadata.training.questions:
        lines.append("## Learning Questions")
        for q in metadata.training.questions:
            lines.append(f"- {q}")
        lines.append("")

    if metadata.training.objectives:
        lines.append("## Learning Objectives")
        for obj in metadata.training.objectives:
            lines.append(f"- {obj}")
        lines.append("")

    # Process content blocks
    for block in content.root:
        # Only include slide blocks in Sphinx output (not prose)
        if block.type != ContentBlockType.SLIDE:
            continue

        # Get block content
        block_content = get_block_content(block, topic_dir)

        # Add heading if present
        if block.heading:
            lines.append(f"## {block.heading}")
            lines.append("")

        # Add content
        lines.append(block_content)
        lines.append("")

    # Add key points as summary
    if metadata.training.key_points:
        lines.append("## Key Takeaways")
        for point in metadata.training.key_points:
            lines.append(f"- {point}")
        lines.append("")

    return "\n".join(lines)


def copy_topic_images(topic_id: str, src_dir: Path, dest_dir: Path) -> None:
    """Copy images from topic to Sphinx _images directory.

    Args:
        topic_id: Topic identifier
        src_dir: Source images directory
        dest_dir: Destination _images directory
    """
    topic_images_dir = src_dir / topic_id

    # Copy images directory if it exists
    if (src_dir / "*.svg").resolve() or (src_dir / "*.png").resolve():
        # For now, we'll handle this when needed
        # Images are already in images/ directory
        pass


def generate_sphinx_docs(topic_name: str) -> None:
    """Generate Sphinx documentation for a topic.

    Args:
        topic_name: Topic ID or 'all' for all topics
    """
    topics_dir = Path("topics")
    outputs_dir = Path("outputs/sphinx-docs/generated/architecture")
    doc_arch_dir = Path("doc/source/architecture")

    # Create output directories
    outputs_dir.mkdir(parents=True, exist_ok=True)
    doc_arch_dir.mkdir(parents=True, exist_ok=True)

    # Determine which topics to generate
    if topic_name == "all":
        topic_ids = [d.name for d in topics_dir.iterdir() if d.is_dir() and (d / "metadata.yaml").exists()]
    else:
        topic_ids = [topic_name]

    # Generate each topic
    for topic_id in sorted(topic_ids):
        topic_dir = topics_dir / topic_id

        if not topic_dir.exists():
            print(f"❌ Topic not found: {topic_id}")
            continue

        try:
            # Generate markdown
            markdown = generate_topic_markdown(topic_id, topic_dir)

            # Process for Sphinx compatibility
            sphinx_markdown = process_markdown_for_sphinx(markdown, topic_id)

            # Write to outputs/sphinx-docs/generated/
            output_file = outputs_dir / f"{topic_id}.md"
            output_file.write_text(sphinx_markdown)
            print(f"✓ Generated: {output_file}")

            # Copy to doc/source/architecture/ for local testing
            doc_file = doc_arch_dir / f"{topic_id}.md"
            doc_file.write_text(sphinx_markdown)
            print(f"✓ Copied to: {doc_file}")

        except Exception as e:
            print(f"❌ Error generating {topic_id}: {e}")
            import traceback
            traceback.print_exc()


def update_architecture_index(topics_to_include: list[str]) -> None:
    """Update doc/source/architecture/index.md with generated topics.

    Args:
        topics_to_include: List of topic IDs to include
    """
    index_file = Path("doc/source/architecture/index.md")

    # Build toctree
    toctree_items = "\n".join(topics_to_include)

    content = f"""# Architecture Topics

Core documentation about Galaxy's internal architecture and design.

```{{toctree}}
:maxdepth: 1

{toctree_items}
```

## Available Topics

This section documents Galaxy's key architectural patterns:

"""

    # Add links for each topic
    topics_dir = Path("topics")
    for topic_id in sorted(topics_to_include):
        topic_dir = topics_dir / topic_id
        if (topic_dir / "metadata.yaml").exists():
            from models import load_metadata
            metadata = load_metadata(topic_id)
            content += f"- **[{metadata.title}]({topic_id}.md)**\n"

    index_file.write_text(content)
    print(f"✓ Updated: {index_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build.py <topic-name|all>")
        print("Example: python build.py dependency-injection")
        print("Example: python build.py all")
        sys.exit(1)

    topic_name = sys.argv[1]

    # Generate Sphinx docs
    generate_sphinx_docs(topic_name)

    # Update index with all available topics
    topics_dir = Path("topics")
    available_topics = sorted([
        d.name for d in topics_dir.iterdir()
        if d.is_dir() and (d / "metadata.yaml").exists()
    ])

    if available_topics:
        update_architecture_index(available_topics)

    print("\n✓ Sphinx documentation generated successfully!")
    print(f"  Generated files: outputs/sphinx-docs/generated/architecture/")
    print(f"  Copied to: doc/source/architecture/")
    print(f"  Build with: cd doc && make html")
    print(f"  View at: doc/build/html/index.html")
