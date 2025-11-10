#!/usr/bin/env python3
"""
Generate GTN-compatible slides from topic content.

Usage:
    uv run python outputs/training-slides/build.py dependency-injection
"""

import sys
import yaml
from pathlib import Path
from jinja2 import Template


def load_topic(topic_name):
    """Load all files for a topic."""
    topic_dir = Path(f"topics/{topic_name}")

    # Load metadata
    with open(topic_dir / "metadata.yaml") as f:
        metadata = yaml.safe_load(f)

    # Load content files (exclude .claude directory)
    content = {}
    for md_file in topic_dir.glob("*.md"):
        if md_file.parent.name != ".claude":
            content[md_file.stem] = md_file.read_text()

    return metadata, content


def markdown_to_slides(markdown_text):
    """Convert markdown to Remark.js slides.
    
    Splits on ## headings or --- separators.
    Each section becomes a slide.
    """
    slides = []
    current_slide = []

    for line in markdown_text.split('\n'):
        # Check if this is a slide separator
        if line.strip() == '---':
            if current_slide:
                slides.append('\n'.join(current_slide))
            current_slide = []
        # Check if this is a new slide heading (##)
        elif line.startswith('## '):
            if current_slide:
                slides.append('\n'.join(current_slide))
            current_slide = [line]
        else:
            current_slide.append(line)

    # Add the last slide
    if current_slide:
        slides.append('\n'.join(current_slide))

    return slides


def generate_slides(topic_name):
    """Generate slides for a topic."""
    metadata, content = load_topic(topic_name)

    # Load template
    template_path = Path(__file__).parent / "template.html"
    template = Template(template_path.read_text())

    # Convert content to slides
    # Order: overview, examples (testing excluded - not in original slides)
    all_slides = []
    for section_name in ['overview', 'examples']:
        if section_name in content:
            slides = markdown_to_slides(content[section_name])
            all_slides.extend(slides)

    # Render template
    output = template.render(
        title=metadata['title'],
        questions=metadata['training']['questions'],
        objectives=metadata['training']['objectives'],
        key_points=metadata['training']['key_points'],
        time_estimation=metadata['training']['time_estimation'],
        slides=all_slides,
        topic_id=metadata['topic_id'],
    )

    # Write output
    output_dir = Path(f"outputs/training-slides/generated/architecture-{topic_name}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "slides.html"
    output_file.write_text(output)

    print(f"✓ Generated slides: {output_file}")
    print(f"  Copy to training-material/topics/dev/tutorials/architecture-{metadata['topic_id']}/slides.html")
    return output_file


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run python outputs/training-slides/build.py <topic-name>")
        sys.exit(1)

    generate_slides(sys.argv[1])

