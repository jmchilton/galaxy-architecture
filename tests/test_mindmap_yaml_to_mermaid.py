#!/usr/bin/env python3
"""Tests for converting mindmap YAML to Mermaid."""

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent / "images"))

from mindmap_yaml_to_mermaid import main, to_mermaid


def convert(text):
    return to_mermaid(yaml.safe_load(text), "x.mindmap.yml").splitlines()


def test_path_root_becomes_tree_view_without_duplicate_root():
    lines = convert("label: /\nitems:\n- label: lib/\n  doc: backend\n  items:\n  - galaxy/\n- client/\n")
    assert lines == [
        "treeView-beta",
        "%% DO NOT EDIT: auto-generated from x.mindmap.yml",
        '    "lib/  —  backend"',
        '        "galaxy/"',
        '    "client/"',
    ]


def test_sub_path_root_is_single_tree_entry():
    lines = convert("label: /lib/galaxy/managers\nitems:\n- base.py\n")
    assert lines[2:] == ['    "lib/galaxy/managers/"', '        "base.py"']


def test_concept_root_becomes_tidy_tree_mindmap():
    lines = convert("label: Plugins\nitems:\n- label: custom\n  doc: custom loading\n")
    assert lines[:6] == [
        "---",
        "config:",
        "  layout: tidy-tree",
        "---",
        "mindmap",
        "%% DO NOT EDIT: auto-generated from x.mindmap.yml",
    ]
    assert lines[6:] == ['  n0["**Plugins**"]', '    n1["**custom**<br>custom loading"]']


def test_diagram_flowchart_keeps_order_with_elk():
    lines = convert("label: Branches\ndiagram: flowchart\nitems:\n- dev\n- master\n")
    assert "  layout: elk" in lines
    assert lines[4:6] == ["flowchart LR", "%% DO NOT EDIT: auto-generated from x.mindmap.yml"]
    assert lines[6:] == [
        '    n0["`**Branches**`"]',
        '    n1["`**dev**`"]',
        "    n0 --- n1",
        '    n2["`**master**`"]',
        "    n0 --- n2",
    ]


def test_escapes_quotes_and_asterisks_and_strips_boxless_prefix():
    lines = convert('label: Plugins\nitems:\n- _tool linters*\n- say "hi"\n')
    assert lines[7] == '    n1["**tool linters#42;**"]'
    assert lines[8] == '    n2["**say #quot;hi#quot;**"]'


def test_main_writes_mmd_next_to_yaml(tmp_path, monkeypatch):
    source = tmp_path / "tree.mindmap.yml"
    source.write_text("label: /\nitems:\n- lib/\n")
    monkeypatch.setattr(sys, "argv", ["prog", str(source)])
    main()
    assert (tmp_path / "tree.mindmap.mmd").read_text().startswith("treeView-beta\n")
