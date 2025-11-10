#!/usr/bin/env python3
"""
Unit tests for validation script.

Tests:
- Metadata validation
- Content quality checks
- Image validation
- Cross-reference validation
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import yaml
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate import (
    validate_topic,
    validate_markdown_file,
    validate_content_quality,
    get_nested_value,
)


class TestMetadataValidation:
    """Test metadata validation logic."""

    def test_get_nested_value(self):
        """Test nested value extraction."""
        data = {
            'training': {
                'questions': ['Q1', 'Q2'],
                'objectives': ['O1']
            }
        }
        assert get_nested_value(data, ['training', 'questions']) == ['Q1', 'Q2']
        assert get_nested_value(data, ['training', 'objectives']) == ['O1']
        assert get_nested_value(data, ['training', 'missing']) == {}
        assert get_nested_value(data, ['missing']) == {}  # Returns {} for missing top-level keys

    def test_validate_topic_missing_metadata(self):
        """Test validation with missing metadata.yaml."""
        with tempfile.TemporaryDirectory() as tmpdir:
            topic_dir = Path(tmpdir) / "test-topic"
            topic_dir.mkdir()
            
            errors, warnings = validate_topic(topic_dir)
            assert len(errors) > 0
            assert any("Missing metadata.yaml" in e for e in errors)

    def test_validate_topic_valid_metadata(self):
        """Test validation with valid metadata."""
        with tempfile.TemporaryDirectory() as tmpdir:
            topic_dir = Path(tmpdir) / "test-topic"
            topic_dir.mkdir()
            (topic_dir / ".claude").mkdir()
            
            metadata = {
                'topic_id': 'test-topic',
                'title': 'Test Topic',
                'status': 'draft',
                'training': {
                    'questions': ['Q1'],
                    'objectives': ['O1'],
                    'key_points': ['K1'],
                    'time_estimation': '15m',
                }
            }
            
            with open(topic_dir / "metadata.yaml", 'w') as f:
                yaml.dump(metadata, f)
            
            (topic_dir / "overview.md").write_text("# Test\n\nContent here.")
            (topic_dir / ".claude" / "CLAUDE.md").write_text("# Context")
            
            errors, warnings = validate_topic(topic_dir)
            # Should have no errors, only warnings if any
            assert len([e for e in errors if "Missing" in e]) == 0

    def test_validate_topic_missing_required_fields(self):
        """Test validation detects missing required fields."""
        with tempfile.TemporaryDirectory() as tmpdir:
            topic_dir = Path(tmpdir) / "test-topic"
            topic_dir.mkdir()
            
            metadata = {
                'topic_id': 'test-topic',
                'title': 'Test Topic',
                # Missing status and training fields
            }
            
            with open(topic_dir / "metadata.yaml", 'w') as f:
                yaml.dump(metadata, f)
            
            errors, warnings = validate_topic(topic_dir)
            assert len(errors) > 0
            assert any("Missing required field" in e for e in errors)

    def test_validate_topic_topic_id_mismatch(self):
        """Test validation detects topic_id mismatch."""
        with tempfile.TemporaryDirectory() as tmpdir:
            topic_dir = Path(tmpdir) / "test-topic"
            topic_dir.mkdir()
            
            metadata = {
                'topic_id': 'wrong-id',  # Doesn't match directory name
                'title': 'Test Topic',
                'status': 'draft',
                'training': {
                    'questions': ['Q1'],
                    'objectives': ['O1'],
                    'key_points': ['K1'],
                    'time_estimation': '15m',
                }
            }
            
            with open(topic_dir / "metadata.yaml", 'w') as f:
                yaml.dump(metadata, f)
            
            errors, warnings = validate_topic(topic_dir)
            assert any("topic_id" in e and "does not match" in e for e in errors)


class TestContentQuality:
    """Test content quality validation."""

    def test_validate_content_quality_short_content(self):
        """Test short content warning."""
        content = "Short"
        errors, warnings = validate_content_quality(content, "test.md")
        assert len(warnings) > 0
        assert any("short" in w.lower() for w in warnings)

    def test_validate_content_quality_heading_hierarchy(self):
        """Test heading hierarchy validation."""
        content = """# H1
## H2
#### H4
"""
        errors, warnings = validate_content_quality(content, "test.md")
        assert any("skipped" in w.lower() for w in warnings)

    def test_validate_content_quality_code_blocks(self):
        """Test code block language specification."""
        content = """```python
code
```
```
no language
```
"""
        errors, warnings = validate_content_quality(content, "test.md")
        assert any("language" in w.lower() for w in warnings)

    def test_validate_content_quality_valid(self):
        """Test valid content passes."""
        content = """# Title

## Section 1

Some content here with enough text to pass minimum length requirements.
This should be at least 500 characters long to avoid warnings.

```python
def example():
    pass
```

More content here.
"""
        errors, warnings = validate_content_quality(content, "test.md")
        # Should have minimal warnings for valid content
        assert len(errors) == 0


class TestMarkdownValidation:
    """Test markdown file validation."""

    def test_validate_markdown_unclosed_code_block(self):
        """Test detection of unclosed code blocks."""
        with tempfile.TemporaryDirectory() as tmpdir:
            topic_dir = Path(tmpdir) / "test-topic"
            topic_dir.mkdir()
            
            md_file = topic_dir / "test.md"
            md_file.write_text("```python\ncode\n")
            
            metadata = {}
            errors, warnings = validate_markdown_file(md_file, topic_dir, metadata)
            assert any("Unclosed code block" in e for e in errors)

    def test_validate_markdown_image_validation(self):
        """Test image reference validation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            topic_dir = repo_root / "topics" / "test-topic"
            topic_dir.mkdir(parents=True)
            images_dir = repo_root / "images"
            images_dir.mkdir()
            
            # Create a test image
            (images_dir / "test.png").write_text("fake image")
            
            md_file = topic_dir / "test.md"
            md_file.write_text("![Alt](../../images/test.png)")
            
            metadata = {}
            errors, warnings = validate_markdown_file(md_file, topic_dir, metadata)
            # Should not error for existing image
            assert not any("Image not found" in e for e in errors)
            
            # Test missing image
            md_file.write_text("![Alt](../../images/missing.png)")
            errors, warnings = validate_markdown_file(md_file, topic_dir, metadata)
            assert any("Image not found" in e for e in errors)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

