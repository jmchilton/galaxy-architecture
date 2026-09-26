#!/usr/bin/env python3
"""Generate Sphinx markdown documentation from topic content.

Usage:
    python outputs/sphinx-docs/build.py dependency-injection
    python outputs/sphinx-docs/build.py all
"""

import re
import sys
import shutil
from pathlib import Path
from typing import Callable, Optional

# Add scripts to path so we can import models
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from models import load_metadata, load_content, ContentBlockType


GTN_BASE_URL = "https://training.galaxyproject.org/training-material/"

FENCE_OPEN_RE = re.compile(r'^[ \t]*(`{3,}|~{3,})')
INLINE_CODE_RE = re.compile(r'(`+)(?:(?!\1).)+?\1', re.DOTALL)
SPEAKER_NOTES_RE = re.compile(r'^[ \t]*\?\?\?[ \t]*$')
MARKDOWN_LINK_RE = re.compile(r'\[[^\]\n]*\]\([^)\n]*\)')
BARE_URL_RE = re.compile(r'https?://[^\s)<>"\']+')
URL_TRAILING_PUNCTUATION = '.,;:!?*`'
LIQUID_LINK_RE = re.compile(r'\{%\s*link\s+(\S+?)\s*%\}')


def separate_fences_from_directives(markdown: str) -> str:
    """Put code fences glued to directive brackets (``.strike[```python``, `````]``) on their own lines."""
    markdown = re.sub(r'(\.\w+\[)(`{3,}|~{3,})', r'\1\n\2', markdown)
    return re.sub(r'^([ \t]*(?:`{3,}|~{3,}))\]', r'\1\n]', markdown, flags=re.M)


def split_fenced_code(markdown: str) -> list[tuple[bool, str]]:
    """Split markdown into (is_fenced_code, text) segments, preserving all text."""
    segments: list[tuple[bool, str]] = []
    current: list[str] = []
    fence: Optional[str] = None
    for line in markdown.splitlines(keepends=True):
        if fence is None:
            match = FENCE_OPEN_RE.match(line)
            if match:
                if current:
                    segments.append((False, "".join(current)))
                current = [line]
                fence = match.group(1)
            else:
                current.append(line)
        else:
            current.append(line)
            stripped = line.strip()
            if stripped.startswith(fence[0] * len(fence)) and stripped.strip(fence[0]) == "":
                segments.append((True, "".join(current)))
                current = []
                fence = None
    if current:
        segments.append((fence is not None, "".join(current)))
    return segments


def map_outside_code(markdown: str, transform: Callable[[str], str]) -> str:
    """Apply transform to text outside fenced blocks and inline code spans."""
    parts = []
    for is_code, segment in split_fenced_code(markdown):
        if is_code:
            parts.append(segment)
            continue
        pos = 0
        for match in INLINE_CODE_RE.finditer(segment):
            parts.append(transform(segment[pos:match.start()]))
            parts.append(match.group())
            pos = match.end()
        parts.append(transform(segment[pos:]))
    return "".join(parts)


def code_spans(markdown: str) -> list[tuple[int, int]]:
    """Return (start, end) offsets of fenced blocks and inline code spans."""
    spans = []
    offset = 0
    for is_code, segment in split_fenced_code(markdown):
        if is_code:
            spans.append((offset, offset + len(segment)))
        else:
            spans.extend((offset + m.start(), offset + m.end()) for m in INLINE_CODE_RE.finditer(segment))
        offset += len(segment)
    return spans


def strip_speaker_notes(markdown: str) -> str:
    """Strip speaker notes (from a line containing only ??? onward) from a markdown block."""
    markdown = separate_fences_from_directives(markdown)
    offset = 0
    for is_code, segment in split_fenced_code(markdown):
        if not is_code:
            line_offset = offset
            for line in segment.splitlines(keepends=True):
                if SPEAKER_NOTES_RE.match(line):
                    return markdown[:line_offset].rstrip()
                line_offset += len(line)
        offset += len(segment)
    return markdown


def create_slides_link(topic_id: str) -> str:
    """Create link to view topic as training slides.

    Args:
        topic_id: Topic identifier (e.g., 'dependency-injection')

    Returns:
        Markdown formatted link string
    """
    return f'> 📊 <a href="{topic_id}/slides.html">View as slides</a>'


def _extract_directive_content(content: str, start_pos: int, directive_name: str) -> tuple[str, int]:
    """Extract content from a Remark.js directive using bracket counting.

    Args:
        content: Full markdown content
        start_pos: Position of the opening bracket after directive name
        directive_name: Name of directive (for error messages)

    Returns:
        (extracted_content, end_position) or (None, -1) if bracket mismatch
    """
    bracket_count = 0
    pos = start_pos

    while pos < len(content):
        if content[pos] == '[':
            bracket_count += 1
        elif content[pos] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                return content[start_pos + 1:pos], pos + 1
        pos += 1

    return None, -1


def _process_pull_directives(markdown: str) -> str:
    """Convert .pull-left and .pull-right to side-by-side layout.

    Extracts both directives and formats them as:
    LEFT_CONTENT | RIGHT_CONTENT
    """
    # Look for .pull-left[ and .pull-right[ patterns
    left_match = re.search(r'\.pull-left\[', markdown)
    right_match = re.search(r'\.pull-right\[', markdown)

    if not left_match or not right_match:
        # No pull directives, return as-is
        return markdown

    # Extract left content
    left_start = left_match.start()
    left_bracket_pos = left_match.end() - 1
    left_content, left_end = _extract_directive_content(markdown, left_bracket_pos, 'pull-left')

    if left_content is None:
        return markdown

    # Extract right content
    right_start = right_match.start()
    right_bracket_pos = right_match.end() - 1
    right_content, right_end = _extract_directive_content(markdown, right_bracket_pos, 'pull-right')

    if right_content is None:
        return markdown

    # Build replacement: left and right side-by-side with a divider
    # Determine which comes first
    if left_start < right_start:
        # .pull-left comes before .pull-right
        before = markdown[:left_start]
        between = markdown[left_end:right_start]
        after = markdown[right_end:]
        replacement = f"{left_content.strip()}\n\n---\n\n{right_content.strip()}"
    else:
        # .pull-right comes before .pull-left
        before = markdown[:right_start]
        between = markdown[right_end:left_start]
        after = markdown[left_end:]
        replacement = f"{right_content.strip()}\n\n---\n\n{left_content.strip()}"

    return before + replacement + after


def _next_directive_outside_code(markdown: str) -> Optional[re.Match]:
    spans = code_spans(markdown)
    for match in re.finditer(r'\.(\w+)\[', markdown):
        if not any(start <= match.start() < end for start, end in spans):
            return match
    return None


def _render_directive(name: str, content: str) -> str:
    if name == "strike":
        if "\n" in content.strip():
            return f"\n:::{{admonition}} Deprecated\n:class: warning\n\n{content.strip()}\n:::\n"
        return f"<del>{content}</del>"
    # Undo the line breaks added by separate_fences_from_directives
    content = re.sub(r'^\n(?=[ \t]*(?:`{3,}|~{3,}))', '', content)
    return re.sub(r'((?:`{3,}|~{3,}))\n$', r'\1', content)


def _unwrap_remark_directives(markdown: str) -> str:
    """Unwrap remaining Remark.js directives like .code[...], .reduce70[...], etc.

    Uses bracket counting to handle multi-line content and nested brackets.
    Directive-like text inside code (e.g. ``foo.bar[0]``) is left alone.
    """
    markdown = separate_fences_from_directives(markdown)

    while True:
        # Find the next directive
        match = _next_directive_outside_code(markdown)
        if not match:
            break

        directive_start = match.start()
        bracket_pos = match.end() - 1

        # Extract content using bracket counting
        content, end_pos = _extract_directive_content(markdown, bracket_pos, match.group(1))

        if content is None:
            # Malformed directive, skip it
            break

        # Replace directive with its rendered content
        markdown = markdown[:directive_start] + _render_directive(match.group(1), content) + markdown[end_pos:]

    return markdown


def process_markdown_for_sphinx(markdown: str, topic_id: str) -> str:
    """Process markdown for Sphinx compatibility.

    - Unwrap Remark.js class directives (.code[...], .reduce70[...], etc.)
    - Convert .pull-left/.pull-right to side-by-side columns
    - Fix image paths (../../images/ -> ../_images/)
    - Fix asset paths ({{ site.baseurl }}/assets/ -> ../_images/)
    - Convert bare URLs to markdown links

    Note: Speaker notes should be stripped per-block before this is called.
    """
    # Handle .pull-left and .pull-right directives specially
    # Convert them to a two-column layout for Sphinx
    markdown = _process_pull_directives(markdown)

    # Unwrap remaining Remark.js class directives like .code[...], .reduce90[...], etc.
    # These are used in Remark.js for styling but not valid in Sphinx markdown
    # Use bracket counting to handle multi-line content
    markdown = _unwrap_remark_directives(markdown)

    # Fix image paths: ../../images/ becomes ../_images/
    # This assumes doc/source/architecture/ and images at doc/source/_images/
    markdown = markdown.replace("../../images/", "../_images/")

    # Fix asset paths: {{ site.baseurl }}/assets/images/ becomes ../_images/
    markdown = markdown.replace("{{ site.baseurl }}/assets/images/", "../_images/")

    # Resolve GTN Liquid links to absolute training-material URLs
    markdown = map_outside_code(markdown, resolve_liquid_links)

    # Convert bare URLs (outside code and existing links) to markdown links
    return map_outside_code(markdown, linkify_bare_urls)


def resolve_liquid_links(text: str) -> str:
    """Replace ``{% link topics/... %}`` with the absolute GTN URL."""
    return LIQUID_LINK_RE.sub(lambda m: GTN_BASE_URL + m.group(1).lstrip("/"), text)


def _linkify(text: str) -> str:
    def replace(match: re.Match) -> str:
        url = match.group()
        stripped = url.rstrip(URL_TRAILING_PUNCTUATION)
        return f"[{stripped}]({stripped}){url[len(stripped):]}"

    return BARE_URL_RE.sub(replace, text)


def linkify_bare_urls(text: str) -> str:
    """Convert bare URLs to markdown links, leaving existing markdown links alone."""
    parts = []
    pos = 0
    for match in MARKDOWN_LINK_RE.finditer(text):
        parts.append(_linkify(text[pos:match.start()]))
        parts.append(match.group())
        pos = match.end()
    parts.append(_linkify(text[pos:]))
    return "".join(parts)


def rewrite_image_paths_for_sphinx(markdown: str) -> str:
    """Rewrite image paths to work in Sphinx documentation context.

    Converts:
    - ../../../../shared/images/ → ../../images/ (shared images)
    - ../../images/ → ../../images/ (dev images)
    - ../../../../images/ → ../../images/ (generic images)

    All images are copied to doc/build/html/images/ so relative paths
    need to point there. From doc/source/architecture/*, we need ../../ to reach images/.

    Sphinx preserves relative markdown links, so:
    - Markdown: doc/source/architecture/file.md with ![](../../images/img.svg)
    - Builds to: doc/build/html/architecture/file.html with src="../../images/img.svg"
    - Resolves to: doc/build/html/images/img.svg ✓
    """
    # Handle shared images: ../../../../shared/images/ → ../../images/
    markdown = re.sub(
        r'(\[.*?\])\(../../../../shared/images/',
        r'\1(../../images/',
        markdown
    )

    # Handle dev images: ../../images/ → ../../images/ (already correct, but ensure)
    markdown = re.sub(
        r'(\[.*?\])\((?!https?://)(?!data:)../../images/',
        r'\1(../../images/',
        markdown
    )

    # Handle generic 4-level paths: ../../../../images/ → ../../images/
    markdown = re.sub(
        r'(\[.*?\])\(../../../../images/',
        r'\1(../../images/',
        markdown
    )

    return markdown


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

    # Add link to view as training slides
    lines.append(create_slides_link(topic_id))
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
        # Check if doc rendering is explicitly disabled
        if block.doc and block.doc.render is False:
            continue

        # Check if block should render in docs based on smart defaults
        # Slides: render in docs by default
        # Prose: render in docs by default
        if block.type == ContentBlockType.SLIDE:
            # Include slides in docs (default behavior)
            pass
        elif block.type == ContentBlockType.PROSE:
            # Include prose blocks in docs (default behavior)
            pass
        else:
            # Unknown block type, skip
            continue

        # Get block content
        block_content = get_block_content(block, topic_dir)

        # Strip speaker notes from block content
        block_content = strip_speaker_notes(block_content)

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

    # Build final markdown and rewrite image paths for Sphinx context
    markdown = "\n".join(lines)
    markdown = rewrite_image_paths_for_sphinx(markdown)

    return markdown


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
    import shutil
    topics_dir = Path("topics")
    outputs_dir = Path("outputs/sphinx-docs/generated/architecture")
    doc_arch_dir = Path("doc/source/architecture")
    doc_images_dir = Path("doc/source/_images")

    # Create output directories
    outputs_dir.mkdir(parents=True, exist_ok=True)
    doc_arch_dir.mkdir(parents=True, exist_ok=True)
    doc_images_dir.mkdir(parents=True, exist_ok=True)

    # Copy assets if they exist
    if Path("assets").exists():
        for asset_file in Path("assets").iterdir():
            if asset_file.is_file():
                shutil.copy2(asset_file, doc_images_dir / asset_file.name)

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

    Topics are ordered by following the continues_to chain, starting from
    the topic that has no previous_to.

    Args:
        topics_to_include: List of topic IDs to include
    """
    from models import load_metadata

    index_file = Path("doc/source/architecture/index.md")
    topics_dir = Path("topics")

    # Load metadata for all topics to build the chain
    topic_metadata = {}
    for topic_id in topics_to_include:
        try:
            topic_metadata[topic_id] = load_metadata(topic_id)
        except Exception:
            pass

    # Find the starting topic (one with no previous_to)
    ordered_topics = []
    current_id = None

    for topic_id in topic_metadata:
        if not topic_metadata[topic_id].training.previous_to:
            current_id = topic_id
            break

    # Follow the chain using continues_to
    if current_id:
        visited = set()
        while current_id and current_id not in visited:
            ordered_topics.append(current_id)
            visited.add(current_id)
            next_id = topic_metadata[current_id].training.continues_to if current_id in topic_metadata else None
            # Only continue if next topic exists in available topics
            if next_id and next_id in topic_metadata:
                current_id = next_id
            else:
                current_id = None

    # Add any remaining topics not in the chain (in sorted order)
    for topic_id in sorted(topics_to_include):
        if topic_id not in ordered_topics:
            ordered_topics.append(topic_id)

    # Fall back to sorted list if chain failed to start
    if not ordered_topics:
        ordered_topics = sorted(topics_to_include)

    # Build toctree
    toctree_items = "\n".join(ordered_topics)

    content = f"""# Architecture Topics

Core documentation about Galaxy's internal architecture and design.

```{{toctree}}
:maxdepth: 1
:caption: Architecture Topics

{toctree_items}
```
"""

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
