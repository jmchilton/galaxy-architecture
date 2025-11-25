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

from validate import validate_topic, validate_all


class TestMetadataValidation:
    """Test metadata validation logic."""

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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

