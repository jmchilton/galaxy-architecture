#!/usr/bin/env python3
"""Unit tests for metadata/content models."""

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from models import ContentBlock, TopicMetadata, load_metadata


def test_content_block_rejects_unknown_keys():
    with pytest.raises(ValidationError):
        ContentBlock(type="slide", id="a-slide", content="Hi", templat="left-aligned")


def test_content_block_accepts_template():
    block = ContentBlock(type="slide", id="a-slide", content="Hi", template="left-aligned")
    assert block.template == "left-aligned"


def test_topic_metadata_rejects_unknown_keys():
    data = load_metadata("dependency-injection").model_dump(by_alias=True)
    data["hub"] = {"category": "nope"}
    with pytest.raises(ValidationError):
        TopicMetadata(**data)
