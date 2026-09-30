#!/usr/bin/env python3
"""Tests for checking Galaxy references in Mermaid diagrams against a Galaxy checkout."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_diagram_refs import check_diagrams, diagram_refs, missing_refs


@pytest.fixture
def galaxy(tmp_path):
    root = tmp_path / "galaxy"
    sources = root / "lib/galaxy/files/sources"
    sources.mkdir(parents=True)
    (root / "lib/galaxy/__init__.py").write_text("")
    (root / "lib/galaxy/files/__init__.py").write_text("")
    (sources / "__init__.py").write_text("from .base import BaseFilesSource\n\nclass FilesSource:\n    pass\n")
    (sources / "base.py").write_text("class BaseFilesSource:\n    pass\n")
    (sources / "posix.py").write_text("class PosixFilesSource:\n    pass\n\nDEFAULT = 1\n")
    (root / "lib/galaxy/structured_app").mkdir()
    (root / "lib/galaxy/structured_app/__init__.py").write_text("class StructuredApp:\n    pass\n")
    (root / "test/unit").mkdir(parents=True)
    return root


def test_diagram_refs_collects_paths_dotted_names_and_namespaced_classes():
    text = """\
classDiagram
    namespace galaxy_files_sources {
        class BaseFilesSource {
            <<abstract>>
        }
        class PosixFilesSource["posix.PosixFilesSource"]
    }
    namespace Template_Stage {
        class Conceptual
    }
    class StructuredApp["galaxy.structured_app.StructuredApp"]
    note for StructuredApp "see test/unit/ and lib/galaxy/app/"
"""
    assert diagram_refs(text) == [
        ("namespace", "galaxy_files_sources"),
        ("namespaced", ("galaxy_files_sources", "BaseFilesSource")),
        ("namespaced", ("galaxy_files_sources", "posix.PosixFilesSource")),
        ("dotted", "galaxy.structured_app.StructuredApp"),
        ("path", "test/unit/"),
        ("path", "lib/galaxy/app/"),
    ]


def test_missing_refs_resolves_modules_names_and_paths(galaxy):
    text = """\
classDiagram
    class StructuredApp["galaxy.structured_app.StructuredApp"]
    class BasicApp["galaxy.structured_app.BasicApp"]
    class Gone["galaxy.nowhere.Gone"]
    note for StructuredApp "galaxy.files.sources.posix.DEFAULT test/unit/ test/gone/"
"""
    assert missing_refs(text, galaxy) == [
        "galaxy.structured_app.BasicApp",
        "galaxy.nowhere.Gone",
        "test/gone/",
    ]


def test_missing_refs_resolves_namespaces_with_underscored_segments(galaxy):
    text = """\
classDiagram
    namespace galaxy_files_sources {
        class BaseFilesSource
        class FilesSource
        class PosixFileSource["posix.PosixFileSource"]
        class PosixFilesSource["posix.PosixFilesSource"]
        class Renamed
    }
    namespace galaxy_tools_toolbox {
        class AbstractToolBox
    }
"""
    assert missing_refs(text, galaxy) == [
        "galaxy.files.sources.posix.PosixFileSource",
        "galaxy.files.sources.Renamed",
        "galaxy_tools_toolbox",
    ]


def test_namespaced_dotted_label_prefers_namespace_over_absolute(galaxy):
    (galaxy / "lib/galaxy/files/sources/galaxy.py").write_text("class UserFtpFilesSource:\n    pass\n")
    text = """\
classDiagram
    namespace galaxy_files_sources {
        class UserFtpFilesSource["galaxy.UserFtpFilesSource"]
    }
"""
    assert missing_refs(text, galaxy) == []


def test_check_diagrams_skips_generated_mindmaps(tmp_path, galaxy):
    images = tmp_path / "images"
    images.mkdir()
    (images / "ok.mmd").write_text("flowchart TD\n    a[\"test/unit/\"]\n")
    (images / "stale.mmd").write_text("flowchart TD\n    a[\"galaxy.nowhere\"]\n")
    (images / "tree.mindmap.mmd").write_text('treeView-beta\n    "lib/gone/"\n')
    assert check_diagrams(images, galaxy) == {"stale.mmd": ["galaxy.nowhere"]}
