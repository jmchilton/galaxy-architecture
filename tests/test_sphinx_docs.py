#!/usr/bin/env python3
"""Tests for the Sphinx docs builder's slide-markup transforms."""

import importlib.util
import sys
from pathlib import Path

import pytest

BUILD_PY = Path(__file__).parent.parent / "outputs" / "sphinx-docs" / "build.py"


@pytest.fixture(scope="module")
def builder():
    sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
    spec = importlib.util.spec_from_file_location("sphinx_docs_build", BUILD_PY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def process(builder, markdown):
    return builder.process_markdown_for_sphinx(markdown, "some-topic")


# Bare-URL linkifier

def test_linkifier_skips_fenced_code(builder):
    markdown = "```bash\n$ git clone https://github.com/galaxyproject/galaxy.git\n```\n"
    assert process(builder, markdown) == markdown


def test_linkifier_skips_inline_code(builder):
    markdown = "Set `url_regex: https://example.org/.*` in the config."
    assert process(builder, markdown) == markdown


def test_linkifier_excludes_trailing_punctuation(builder):
    result = process(builder, "See https://www.sqlalchemy.org/. Also https://fastapi.tiangolo.com, too.")
    assert "[https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)." in result
    assert "[https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)," in result


def test_linkifier_leaves_markdown_links_alone(builder):
    markdown = "Read [https://galaxyproject.org](https://galaxyproject.org) and [docs](https://docs.galaxyproject.org/)."
    assert process(builder, markdown) == markdown


def test_linkifier_links_bare_url(builder):
    assert process(builder, "Go to https://galaxyproject.org now") == (
        "Go to [https://galaxyproject.org](https://galaxyproject.org) now"
    )


# Remark directive unwrapping

def test_unwrap_directive(builder):
    assert process(builder, ".reduce90[Some text]") == "Some text"


def test_unwrap_skips_fenced_code(builder):
    markdown = "```python\nvalue = foo.bar[0]\n```\n"
    assert process(builder, markdown) == markdown


def test_unwrap_skips_inline_code(builder):
    markdown = "Index with `foo.bar[0]` here."
    assert process(builder, markdown) == markdown


def test_strike_block_becomes_deprecated_admonition(builder):
    markdown = ".strike[```python\n>>> fh = open(dataset.file_path, 'w')\n```]\n\nAfter."
    result = process(builder, markdown)
    assert ":::{admonition} Deprecated" in result
    assert ":class: warning" in result
    assert "```python\n>>> fh = open(dataset.file_path, 'w')\n```" in result
    assert ".strike" not in result
    assert result.rstrip().endswith("After.")


# Liquid links

def test_liquid_link_resolved_to_gtn(builder):
    result = process(builder, "See the [training]({% link topics/dev/tutorials/webhooks/slides.html %}).")
    assert "{% link" not in result
    assert (
        "[training](https://training.galaxyproject.org/training-material/topics/dev/tutorials/webhooks/slides.html)"
        in result
    )


# Speaker notes

def test_speaker_notes_stripped_at_marker_line(builder):
    assert builder.strip_speaker_notes("Slide text\n\n???\n\nNotes here") == "Slide text"


def test_speaker_notes_ignore_inline_question_marks(builder):
    markdown = "Is it slow??? Yes."
    assert builder.strip_speaker_notes(markdown) == markdown


def test_speaker_notes_ignore_fenced_marker(builder):
    markdown = "```text\n???\n```\nMore text"
    assert builder.strip_speaker_notes(markdown) == markdown


def test_speaker_notes_after_directive_wrapped_fence(builder):
    markdown = ".code[```\n$ galaxy\n```]\n\n???\n\nNotes here"
    assert builder.strip_speaker_notes(markdown) == ".code[\n```\n$ galaxy\n```\n]"


def test_unwrap_directive_wrapped_fence_adds_no_blank_lines(builder):
    assert process(builder, ".code[```\n$ galaxy\n```]\n\nAfter") == "```\n$ galaxy\n```\n\nAfter"
