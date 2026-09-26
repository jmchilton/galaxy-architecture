#!/usr/bin/env python3
"""
Unit tests for validation script.

Tests:
- Metadata validation
- Content quality checks
"""

import pytest
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate import find_missing_images, validate_topic, validate_all


class TestMetadataValidation:
    """Test metadata validation against real topics."""

    def test_validate_existing_topics(self):
        """Test that all existing topics validate successfully."""
        topics_dir = Path("topics")
        assert topics_dir.exists(), "topics/ directory must exist"

        for topic_dir in sorted(topics_dir.iterdir()):
            if not topic_dir.is_dir() or topic_dir.name.startswith('.'):
                continue

            errors, warnings = validate_topic(topic_dir)
            # All topics should be valid
            assert len(errors) == 0, f"{topic_dir.name} has validation errors: {errors}"

    def test_validate_missing_metadata(self):
        """Test validation catches missing metadata.yaml."""
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmpdir:
            topic_dir = Path(tmpdir) / "test-topic"
            topic_dir.mkdir()

            errors, warnings = validate_topic(topic_dir)
            # Should report that metadata.yaml is missing
            assert len(errors) > 0
            assert any("metadata.yaml not found" in e for e in errors)

    def test_validate_all_returns_true(self):
        """Test that validate_all returns True when all topics are valid."""
        result = validate_all()
        assert result is True, "All topics should be valid"


class TestTopicStructure:
    """Test that topics follow expected structure."""

    def test_all_topics_have_metadata(self):
        """Test that all topics have metadata.yaml."""
        topics_dir = Path("topics")
        for topic_dir in sorted(topics_dir.iterdir()):
            if not topic_dir.is_dir() or topic_dir.name.startswith('.'):
                continue
            assert (topic_dir / "metadata.yaml").exists(), f"{topic_dir.name} missing metadata.yaml"

    def test_all_topics_have_content(self):
        """Test that all topics have content.yaml."""
        topics_dir = Path("topics")
        for topic_dir in sorted(topics_dir.iterdir()):
            if not topic_dir.is_dir() or topic_dir.name.startswith('.'):
                continue
            assert (topic_dir / "content.yaml").exists(), f"{topic_dir.name} missing content.yaml"

    def test_all_topics_have_claude_context(self):
        """Test that all topics have .claude/CLAUDE.md."""
        topics_dir = Path("topics")
        missing = []
        for topic_dir in sorted(topics_dir.iterdir()):
            if not topic_dir.is_dir() or topic_dir.name.startswith('.'):
                continue
            if not (topic_dir / ".claude" / "CLAUDE.md").exists():
                missing.append(topic_dir.name)

        # This is a warning, not an error, so we only report if any are missing
        if missing:
            print(f"⚠️  Topics missing .claude/CLAUDE.md: {missing}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])



class TestImageReferences:
    """Test that image references in content resolve to files in images/."""

    def test_reports_missing_image(self, tmp_path):
        (tmp_path / "present.svg").write_text("<svg/>")
        markdown = "![Present](../../images/present.svg)\n![Gone](../../images/gone.png)"
        assert find_missing_images(markdown, tmp_path) == ["../../images/gone.png"]

    def test_resolves_gtn_prefixes_to_images_dir(self, tmp_path):
        (tmp_path / "logo.png").write_text("")
        markdown = (
            "![A](../../images/logo.png) "
            "![B](../../../../shared/images/logo.png) "
            "![C]({{ site.baseurl }}/assets/images/logo.png)"
        )
        assert find_missing_images(markdown, tmp_path) == []

    def test_generated_svg_resolves_to_diagram_source(self, tmp_path):
        (tmp_path / "seq.plantuml.txt").write_text("@startuml\n@enduml")
        (tmp_path / "tree.mindmap.yml").write_text("label: root")
        (tmp_path / "flow.mermaid.txt").write_text("graph TD")
        markdown = (
            "![S](../../images/seq.plantuml.svg) "
            "![T](../../images/tree.mindmap.plantuml.svg) "
            "![F](../../images/flow.mermaid.svg) "
            "![N](../../images/nosource.plantuml.svg)"
        )
        assert find_missing_images(markdown, tmp_path) == ["../../images/nosource.plantuml.svg"]

    def test_ignores_external_urls(self, tmp_path):
        markdown = "![Ext](https://example.org/x.png) ![Data](data:image/png;base64,AA==)"
        assert find_missing_images(markdown, tmp_path) == []

    def test_unrecognized_relative_path_is_missing(self, tmp_path):
        (tmp_path / "x.png").write_text("")
        assert find_missing_images("![X](images/x.png)", tmp_path) == ["images/x.png"]

    def test_existing_topics_have_no_missing_images(self):
        for topic_dir in sorted(Path("topics").iterdir()):
            if not topic_dir.is_dir() or topic_dir.name.startswith('.'):
                continue
            errors, _ = validate_topic(topic_dir)
            assert not [e for e in errors if "Missing image" in e], topic_dir.name
