#!/usr/bin/env python3
"""Tests for the GTN training slides builder."""

import importlib.util
from pathlib import Path

BUILD_PY = Path(__file__).parent.parent / "outputs" / "training-slides" / "build.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("training_slides_build", BUILD_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_block_template_emitted_as_remark_template():
    load_builder().generate_slides("frameworks")
    slides_md = Path("outputs/training-slides/generated/architecture-frameworks/slides.md").read_text()
    assert "template: left-aligned" in slides_md
    assert "layout: left-aligned" not in slides_md
