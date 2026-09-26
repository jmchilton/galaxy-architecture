#!/usr/bin/env python3
"""Tests for checking mindmap file references against a Galaxy checkout."""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_mindmap_paths import check_mindmaps, mindmap_paths

MINDMAP = """\
label: /lib/galaxy
items:
  - label: managers
    doc: Business logic
    items:
      - label: base.py
        doc: Base classes
  - label: gone.py
    doc: Removed long ago
  - label: undocumented.py
  - bare_string.py
  - label: "..."
"""


def test_mindmap_paths_joins_labels_under_root():
    paths = sorted(mindmap_paths(yaml.safe_load(MINDMAP)))
    assert paths == [
        "lib/galaxy/bare_string.py",
        "lib/galaxy/gone.py",
        "lib/galaxy/managers",
        "lib/galaxy/managers/base.py",
        "lib/galaxy/undocumented.py",
    ]


def test_check_mindmaps_reports_missing(tmp_path):
    images = tmp_path / "images"
    images.mkdir()
    (images / "core_files_x.mindmap.yml").write_text(MINDMAP)
    (images / "concept.mindmap.yml").write_text("label: /nowhere\nitems:\n  - label: x\n    doc: y\n")
    galaxy = tmp_path / "galaxy"
    (galaxy / "lib/galaxy/managers").mkdir(parents=True)
    (galaxy / "lib/galaxy/managers/base.py").write_text("")
    (galaxy / "lib/galaxy/undocumented.py").write_text("")
    (galaxy / "lib/galaxy/bare_string.py").write_text("")

    missing = check_mindmaps(images, galaxy)

    assert missing == {"core_files_x.mindmap.yml": ["lib/galaxy/gone.py"]}


def test_check_mindmaps_writes_nothing(tmp_path):
    images = tmp_path / "images"
    images.mkdir()
    (images / "core_files_x.mindmap.yml").write_text(MINDMAP)
    before = sorted(p.relative_to(tmp_path) for p in tmp_path.rglob("*"))
    check_mindmaps(images, tmp_path)
    assert sorted(p.relative_to(tmp_path) for p in tmp_path.rglob("*")) == before
