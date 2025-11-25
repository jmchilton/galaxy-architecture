#!/usr/bin/env python3
"""
Generate GTN-compatible slides and standalone HTML from topic content.

Usage:
    uv run python outputs/training-slides/build.py dependency-injection
    uv run python outputs/training-slides/build.py all
"""

import sys
from pathlib import Path
from jinja2 import Template

# Add scripts to path so we can import models
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from models import load_metadata, load_content, ContentBlockType


def rewrite_image_paths_for_html(markdown: str, topic_name: str) -> str:
    """Rewrite image paths for standalone HTML slides.

    For HTML slides stored at: outputs/training-slides/generated/architecture-{topic}/slides.html
    Root images are at: ./images/

    Directory depth from slides to root:
    outputs/training-slides/generated/architecture-{topic}/
    = 4 levels up (../../../..)

    So paths need to be: ../../../../images/

    Also handle:
    - GTN template variables: {{ site.baseurl }}/assets/images/... -> ../../../../images/
    - Shared resources: ../../../../shared/images/ -> ../../../../images/ (map to main images dir)
    - Relative paths: ../../images/ -> ../../../../images/
    """
    import re

    # Handle GTN template variables - convert directly to root images
    # {{ site.baseurl }}/assets/images/filename.png -> ../../../../images/filename.png
    markdown = re.sub(
        r'\{\{\s*site\.baseurl\s*\}\}/assets/images/',
        '../../../../images/',
        markdown
    )

    # Handle shared images: ../../../../shared/images/ -> ../../../../images/
    markdown = re.sub(
        r'(\[.*?\])\(../../../../shared/images/',
        r'\1(../../../../images/',
        markdown
    )

    # Handle regular images: ../../images/ -> ../../../../images/
    # Only match if not already a full URL (contains ://)
    markdown = re.sub(
        r'(\[.*?\])\((?!https?://)(?!data:)../../images/',
        r'\1(../../../../images/',
        markdown
    )

    return markdown


def extract_markdown_from_content_block(block) -> str:
    """Extract markdown text from a content block.

    Args:
        block: ContentBlock object with 'source' property

    Returns:
        Markdown text content or empty string
    """
    if not hasattr(block, 'source'):
        return ""

    source = block.source
    if isinstance(source, str):
        return source
    elif isinstance(source, dict):
        # If source is a dict, it might have 'text' or 'content' key
        if 'text' in source:
            return source['text']
        elif 'content' in source:
            return source['content']

    return ""


def process_code_wrappers(text):
    """Convert {.code} marker before code blocks to .code[```...```] format.
    
    Handles patterns like:
    {.code}
    ```python
    code...
    ```
    
    Converts to:
    .code[```python
    code...
    ```]
    """
    import re
    
    # Pattern: {.code} followed by optional blank lines, then code block
    pattern = r'\{\.code\}\s*\n(\s*)```(\w+)\n(.*?)```'
    
    def replace_code_block(match):
        indent = match.group(1)
        lang = match.group(2)
        code = match.group(3)
        # Wrap the code block
        return f".code[```{lang}\n{code}```]"
    
    # Use DOTALL flag so . matches newlines
    result = re.sub(pattern, replace_code_block, text, flags=re.DOTALL)
    return result


def markdown_to_slides(markdown_text):
    """Convert markdown to Remark.js slides.
    
    Splits on ## headings or --- separators.
    Each section becomes a slide.
    Supports layout classes via `class:` directive.
    
    Returns list of dicts with 'content' and 'class' keys.
    """
    slides = []
    current_slide = []
    pending_class = None

    lines = markdown_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a slide separator
        if line.strip() == '---':
            # Only create slide if we have non-blank content
            if current_slide and any(l.strip() for l in current_slide):
                slides.append({
                    'content': '\n'.join(current_slide),
                    'class': pending_class
                })
            current_slide = []
            # Don't reset pending_class here - it might apply to next slide
        # Check if this is a class directive - store for next slide (don't add to content yet)
        elif line.strip().startswith('class:'):
            pending_class = line.strip()
        # Check if this is a new slide heading (##)
        elif line.startswith('## '):
            # End previous slide if it has content
            if current_slide and any(l.strip() for l in current_slide):
                slides.append({
                    'content': '\n'.join(current_slide),
                    'class': pending_class
                })
            # Start new slide, prepend class if we have one
            if pending_class:
                current_slide = [pending_class, '', line]
                pending_class = None
            else:
                current_slide = [line]
                pending_class = None
        else:
            # Only add non-blank lines if we don't have a pending class waiting
            # (blank lines before class directive should be ignored)
            if not (pending_class and not line.strip()):
                current_slide.append(line)
        
        i += 1

    # Add the last slide
    if current_slide:
        slides.append({
            'content': '\n'.join(current_slide),
            'class': pending_class
        })

    return slides


def generate_navigation_footnote(metadata) -> str:
    """Generate navigation footnote for last slide.

    Format: .footnote[Previous: [Topic](link) | Next: [Topic](link)]
    """
    parts = []

    # Previous link
    if metadata.training.previous_to:
        prev_topic = load_metadata(metadata.training.previous_to)
        prev_num = prev_topic.training.tutorial_number
        prev_title = prev_topic.title
        prev_link = f"{{% link topics/dev/tutorials/architecture-{prev_num}-{metadata.training.previous_to}/slides.html %}}"
        parts.append(f"Previous: [{prev_title}]({prev_link})")

    # Next link
    if metadata.training.continues_to:
        next_topic = load_metadata(metadata.training.continues_to)
        next_num = next_topic.training.tutorial_number
        next_title = next_topic.title
        next_link = f"{{% link topics/dev/tutorials/architecture-{next_num}-{metadata.training.continues_to}/slides.html %}}"
        parts.append(f"Next: [{next_title}]({next_link})")

    if parts:
        return f".footnote[{' | '.join(parts)}]"
    return ""


def generate_slides(topic_name):
    """Generate slides for a topic in two formats:
    1. slides.md - GTN-compatible Remark.js markdown format
    2. slides.html - Standalone HTML viewer with embedded Remark.js
    """
    metadata = load_metadata(topic_name)
    content = load_content(topic_name)

    # Extract all slide-type content blocks (exclude prose-only blocks)
    all_slides = []
    for block in content.root:
        # Include blocks that are explicitly slides or blocks that are not marked as prose-only
        # By default blocks render as slides (doc.render controls doc-only blocks)
        if block.type != ContentBlockType.PROSE:
            markdown = block.content or ""
            # Add heading to markdown if present
            if block.heading and block.heading.strip():
                markdown = f"### {block.heading}\n\n{markdown}"
            if markdown.strip():
                slides = markdown_to_slides(markdown)
                # Apply block-level layout class to all slides from this block
                # The class comes from the 'class:' shorthand in YAML, which gets propagated to slides.layout
                if block.slides.layout:
                    for slide in slides:
                        # Only set class if the slide doesn't already have one from its markdown
                        if not slide.get('class'):
                            slide['class'] = f"class: {block.slides.layout}"
                all_slides.extend(slides)

    # Convert slide dicts to strings for template
    formatted_slides = []
    for slide in all_slides:
        slide_content = slide['content']

        # Process .code[] wrapper syntax: {.code} before code block becomes .code[```...```]
        slide_content = process_code_wrappers(slide_content)

        # Class is already in content if it was set, or we use the class from dict
        lines = slide_content.split('\n')
        if lines and lines[0].strip().startswith('class:'):
            # Class already in content, use as-is
            formatted_slides.append(slide_content)
        elif slide['class']:
            # Add class directive before slide content
            formatted_slides.append(f"{slide['class']}\n\n{slide_content}")
        else:
            formatted_slides.append(slide_content)

    # Add navigation footnote to the last slide
    if formatted_slides:
        footnote = generate_navigation_footnote(metadata)
        if footnote:
            # Append footnote to last slide
            formatted_slides[-1] = formatted_slides[-1] + f"\n\n{footnote}"

    # Generate GTN-compatible markdown format (slides.md)
    gtn_template_path = Path(__file__).parent / "template.html"
    gtn_template = Template(gtn_template_path.read_text())

    gtn_output = gtn_template.render(
        title=metadata.title,
        subtitle=metadata.training.subtitle,
        questions=metadata.training.questions,
        objectives=metadata.training.objectives,
        key_points=metadata.training.key_points,
        time_estimation=metadata.training.time_estimation,
        slides=formatted_slides,
        topic_id=metadata.topic_id,
        contributors=metadata.contributors,
    )

    # Generate standalone HTML format (slides.html)
    html_wrapper_path = Path(__file__).parent / "html_wrapper_template.html"
    html_wrapper_template = Template(html_wrapper_path.read_text())

    # Build markdown content for embedding in HTML
    # Rewrite image paths for HTML context (different depth than GTN markdown)
    fixed_slides = [rewrite_image_paths_for_html(slide, topic_name) for slide in formatted_slides]

    # Join slides with --- separator (Remark.js requires this)
    # Title slide with subtitle
    subtitle = metadata.training.subtitle or ""
    title_slide = f"# {metadata.title}\n\n*{subtitle}.*"
    markdown_parts = [title_slide]

    # Add Learning Questions slide if questions exist
    if metadata.training.questions:
        questions_md = "### Learning Questions\n\n"
        questions_md += "\n".join(f"- {q}" for q in metadata.training.questions)
        markdown_parts.append(questions_md)

    # Add Learning Objectives slide if objectives exist
    if metadata.training.objectives:
        objectives_md = "### Learning Objectives\n\n"
        objectives_md += "\n".join(f"- {o}" for o in metadata.training.objectives)
        markdown_parts.append(objectives_md)

    # Add all formatted slides with --- separator between them
    markdown_content = '\n\n---\n\n'.join(markdown_parts + fixed_slides)

    html_output = html_wrapper_template.render(
        title=metadata.title,
        subtitle=metadata.training.subtitle,
        markdown_content=markdown_content,
    )

    # Write outputs
    output_dir = Path(f"outputs/training-slides/generated/architecture-{topic_name}")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write GTN markdown format
    md_file = output_dir / "slides.md"
    md_file.write_text(gtn_output)
    print(f"✓ Generated GTN slides: {md_file}")
    print(f"  Copy to training-material/topics/dev/tutorials/architecture-{metadata.topic_id}/slides.html")

    # Write standalone HTML format
    html_file = output_dir / "slides.html"
    html_file.write_text(html_output)
    print(f"✓ Generated standalone HTML: {html_file}")

    return md_file, html_file


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run python outputs/training-slides/build.py <topic-name>")
        sys.exit(1)

    generate_slides(sys.argv[1])

