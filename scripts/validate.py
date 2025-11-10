#!/usr/bin/env python3
"""
Validate all topics for completeness and correctness.

Checks:
- metadata.yaml has all required fields
- All referenced files exist
- Internal topic references are valid
- Markdown is well-formed
- No broken code paths
- Content quality (minimum length, structure)
- Image references are valid
- Code path references are documented
"""

import sys
import re
import yaml
from pathlib import Path

REQUIRED_METADATA_FIELDS = [
    'topic_id', 'title', 'status',
    'training.questions', 'training.objectives',
    'training.key_points', 'training.time_estimation',
]

VALID_STATUS_VALUES = ['draft', 'stable', 'deprecated']


def get_nested_value(data, keys):
    """Get nested value from dict using dot-separated keys."""
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key, {})
        else:
            return None
    return value


def validate_topic(topic_dir):
    """Validate a single topic directory."""
    errors = []
    warnings = []

    # Check metadata exists
    metadata_file = topic_dir / "metadata.yaml"
    if not metadata_file.exists():
        errors.append("Missing metadata.yaml")
        return errors, warnings

    # Load and validate metadata
    try:
        with open(metadata_file) as f:
            metadata = yaml.safe_load(f)
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in metadata.yaml: {e}")
        return errors, warnings

    if not isinstance(metadata, dict):
        errors.append("metadata.yaml must contain a YAML object/dictionary")
        return errors, warnings

    # Check required fields
    for field in REQUIRED_METADATA_FIELDS:
        keys = field.split('.')
        value = get_nested_value(metadata, keys)
        if not value:
            errors.append(f"Missing required field: {field}")

    # Validate topic_id matches directory name
    if 'topic_id' in metadata:
        if metadata['topic_id'] != topic_dir.name:
            errors.append(
                f"topic_id '{metadata['topic_id']}' does not match directory name '{topic_dir.name}'"
            )

    # Validate status enum
    if 'status' in metadata:
        if metadata['status'] not in VALID_STATUS_VALUES:
            errors.append(
                f"Invalid status '{metadata['status']}'. Must be one of: {', '.join(VALID_STATUS_VALUES)}"
            )

    # Validate training fields are lists
    if 'training' in metadata:
        training = metadata['training']
        for field in ['questions', 'objectives', 'key_points']:
            if field in training and not isinstance(training[field], list):
                errors.append(f"training.{field} must be a list")

    # Check content files exist
    if not (topic_dir / "overview.md").exists():
        warnings.append("Missing overview.md")

    # Check Claude context
    if not (topic_dir / ".claude" / "CLAUDE.md").exists():
        warnings.append("Missing .claude/CLAUDE.md")

    # Check related topics are valid
    if 'related_topics' in metadata:
        if not isinstance(metadata['related_topics'], list):
            errors.append("related_topics must be a list")
        else:
            topics_dir = topic_dir.parent
            for related in metadata['related_topics']:
                related_dir = topics_dir / related
                if not related_dir.exists():
                    errors.append(f"Related topic not found: {related}")

    # Validate images referenced in metadata
    if 'images' in metadata:
        if not isinstance(metadata['images'], list):
            errors.append("images must be a list")
        else:
            repo_root = topic_dir.parent.parent
            for img in metadata['images']:
                if not isinstance(img, dict):
                    errors.append("Each image entry must be a dictionary")
                    continue
                if 'path' in img:
                    # Handle paths like ../../images/file.svg
                    img_path_str = img['path'].lstrip('/')
                    if img_path_str.startswith('../../images/'):
                        img_path_str = img_path_str.replace('../../', '')
                    img_path = repo_root / img_path_str
                    if not img_path.exists():
                        warnings.append(f"Image file not found: {img['path']}")
                if 'source' in img:
                    source_path = repo_root / img['source'].lstrip('/')
                    if not source_path.exists():
                        warnings.append(f"Image source file not found: {img['source']}")

    # Validate markdown content files
    for md_file in topic_dir.glob("*.md"):
        if md_file.parent.name == ".claude":
            continue
        md_errors, md_warnings = validate_markdown_file(md_file, topic_dir, metadata)
        errors.extend(md_errors)
        warnings.extend(md_warnings)

    # Content quality checks
    overview_file = topic_dir / "overview.md"
    if overview_file.exists():
        content = overview_file.read_text()
        quality_errors, quality_warnings = validate_content_quality(content, overview_file.name)
        errors.extend(quality_errors)
        warnings.extend(quality_warnings)

    # Validate related_code_paths (if provided, should be documented)
    if 'related_code_paths' in metadata:
        if not isinstance(metadata['related_code_paths'], list):
            errors.append("related_code_paths must be a list")
        else:
            # Check that code paths are mentioned in content
            all_content = ""
            for md_file in topic_dir.glob("*.md"):
                if md_file.parent.name != ".claude":
                    all_content += md_file.read_text() + "\n"
            
            for code_path in metadata['related_code_paths']:
                # Check if code path is mentioned in content (basic check)
                if code_path not in all_content and code_path.split('/')[-1] not in all_content:
                    warnings.append(f"Code path '{code_path}' not mentioned in content files")

    return errors, warnings


def validate_markdown_file(md_file, topic_dir, metadata):
    """Validate a markdown file for broken links, images, etc."""
    errors = []
    warnings = []
    content = md_file.read_text()
    repo_root = topic_dir.parent.parent

    # Check for image references
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    for match in re.finditer(image_pattern, content):
        alt_text, img_path = match.groups()
        # Handle relative paths
        if img_path.startswith('../../images/'):
            # Resolve relative to repo root
            # From topics/topic-name/file.md, ../../images/ goes to images/
            relative_path = img_path.replace('../../', '')
            full_path = repo_root / relative_path
            if not full_path.exists():
                errors.append(f"{md_file.name}: Image not found: {img_path}")
        elif img_path.startswith('http'):
            # External URLs - just warn if alt text is missing
            if not alt_text.strip():
                warnings.append(f"{md_file.name}: Image missing alt text: {img_path}")
        else:
            # Relative to topic directory
            full_path = topic_dir / img_path
            if not full_path.exists():
                warnings.append(f"{md_file.name}: Image not found: {img_path}")

    # Check for code block syntax
    code_block_pattern = r'```(\w+)?'
    code_blocks = re.findall(code_block_pattern, content)
    # Basic check - ensure code blocks are properly closed
    if content.count('```') % 2 != 0:
        errors.append(f"{md_file.name}: Unclosed code block detected")

    # Check for broken internal links (markdown links to other topics)
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for match in re.finditer(link_pattern, content):
        link_text, link_path = match.groups()
        # Skip external links
        if link_path.startswith('http'):
            continue
        # Skip anchor links
        if link_path.startswith('#'):
            continue
        # Check for relative topic links (future enhancement)
        # For now, just validate format

    return errors, warnings


def validate_content_quality(content, filename):
    """Validate content quality (length, structure, etc.)."""
    errors = []
    warnings = []

    # Minimum content length check
    MIN_CONTENT_LENGTH = 500  # characters
    if len(content.strip()) < MIN_CONTENT_LENGTH:
        warnings.append(f"{filename}: Content seems short ({len(content)} chars, minimum {MIN_CONTENT_LENGTH})")

    # Check for headings structure
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    headings = []
    for line in content.split('\n'):
        match = re.match(heading_pattern, line)
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append((level, text))

    # Check heading hierarchy (shouldn't skip levels)
    if headings:
        prev_level = 0
        for level, text in headings:
            if level > prev_level + 1 and prev_level > 0:
                warnings.append(f"{filename}: Heading level skipped: '{text}' (h{level} after h{prev_level})")
            prev_level = level

    # Check for at least one h2 heading
    h2_count = sum(1 for level, _ in headings if level == 2)
    if h2_count == 0 and len(headings) > 0:
        warnings.append(f"{filename}: No h2 headings found (consider adding main sections)")

    # Check for code blocks with language specified
    code_block_pattern = r'```(\w+)?\n'
    code_blocks = re.findall(code_block_pattern, content)
    unspecified_blocks = sum(1 for lang in code_blocks if not lang)
    if unspecified_blocks > 0:
        warnings.append(f"{filename}: {unspecified_blocks} code block(s) without language specification")

    return errors, warnings


def validate_all():
    """Validate all topics."""
    topics_dir = Path("topics")
    if not topics_dir.exists():
        print("❌ ERROR: topics/ directory not found")
        return False

    all_errors = {}
    all_warnings = {}

    for topic_dir in topics_dir.iterdir():
        if topic_dir.is_dir() and not topic_dir.name.startswith('.'):
            errors, warnings = validate_topic(topic_dir)
            if errors:
                all_errors[topic_dir.name] = errors
            if warnings:
                all_warnings[topic_dir.name] = warnings

    # Report results
    print(f"\n{'='*60}")
    print("VALIDATION REPORT")
    print(f"{'='*60}\n")

    if all_errors:
        print("❌ ERRORS:\n")
        for topic, errors in all_errors.items():
            print(f"  {topic}:")
            for error in errors:
                print(f"    - {error}")
        print()

    if all_warnings:
        print("⚠️  WARNINGS:\n")
        for topic, warnings in all_warnings.items():
            print(f"  {topic}:")
            for warning in warnings:
                print(f"    - {warning}")
        print()

    if not all_errors and not all_warnings:
        print("✅ All topics valid!")

    return len(all_errors) == 0


def main():
    """Main entry point for the validate-topics script."""
    success = validate_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

