#!/usr/bin/env python3
"""Unit tests for the Sphinx image linter."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import sphinx_image_linter


def run_main(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["sphinx_image_linter.py", *args])
    with pytest.raises(SystemExit) as exc_info:
        sphinx_image_linter.main()
    return exc_info.value.code


def test_missing_html_root_fails(monkeypatch, tmp_path):
    assert run_main(monkeypatch, "--html-dir", str(tmp_path / "missing")) != 0


def test_missing_image_fails(monkeypatch, tmp_path):
    (tmp_path / "index.html").write_text('<html><body><img src="_images/nope.svg"></body></html>')
    assert run_main(monkeypatch, "--html-dir", str(tmp_path)) != 0


def test_present_image_passes(monkeypatch, tmp_path):
    (tmp_path / "_images").mkdir()
    (tmp_path / "_images" / "yes.svg").write_text("<svg/>")
    (tmp_path / "index.html").write_text('<html><body><img src="_images/yes.svg"></body></html>')
    assert run_main(monkeypatch, "--html-dir", str(tmp_path)) == 0
