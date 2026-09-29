#!/usr/bin/env python3
"""Check that Galaxy code referenced in Mermaid diagrams exists in a Galaxy checkout.

Checks hand-written images/*.mmd (generated *.mindmap.mmd are covered by
check_mindmap_paths.py):
- repo paths (lib/..., test/..., client/...) exist
- dotted names (galaxy.structured_app.StructuredApp) resolve to a module and a
  top-level name in it
- classDiagram namespaces named galaxy_* resolve to a package, and their classes
  are defined in it (a dotted label like "posix.PosixFilesSource" is relative
  to the namespace)

Usage:
    GALAXY_ROOT=~/src/galaxy uv run python scripts/check_diagram_refs.py
    uv run python scripts/check_diagram_refs.py --galaxy-root ~/src/galaxy
"""

import argparse
import ast
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Optional

from repo_roots import RepoRootError, resolve_galaxy_root

PATH_RE = re.compile(r"(?<![\w./-])((?:lib|client|test|config|doc|scripts|packages)/[\w./-]*)")
DOTTED_RE = re.compile(r"(?<![\w./-])((?:galaxy|galaxy_test|tool_shed)(?:\.\w+)+)")
NAMESPACE_RE = re.compile(r"^\s*namespace\s+(\w+)")
CLASS_RE = re.compile(r'^\s*class\s+(\w+)(?:\["([^"]*)"\])?')
DOTTED_LABEL_RE = re.compile(r"^\w+(\.\w+)+$")
# Dotted file names (galaxy.yml) are not module references
FILE_SUFFIXES = {"py", "yml", "yaml", "xml", "ini", "json", "txt", "sample", "org"}


def diagram_refs(text: str) -> list[tuple[str, object]]:
    """References in diagram order, as (kind, value); kind is path, dotted, namespace or namespaced."""
    refs: list[tuple[str, object]] = []
    namespace = None
    depth = 0
    for line in text.splitlines():
        if match := NAMESPACE_RE.match(line):
            name = match.group(1)
            namespace = name if name.startswith("galaxy_") else None
            depth = line.count("{") - line.count("}")
            if namespace:
                refs.append(("namespace", namespace))
            continue
        if depth > 0:
            depth += line.count("{") - line.count("}")
            match = CLASS_RE.match(line)
            if namespace and match:
                class_id, label = match.groups()
                name = label if label and DOTTED_LABEL_RE.match(label) else class_id
                refs.append(("namespaced", (namespace, name)))
                continue
            if depth <= 0:
                namespace = None
        for dotted in DOTTED_RE.findall(line):
            if dotted.rsplit(".", 1)[1] not in FILE_SUFFIXES:
                refs.append(("dotted", dotted))
        refs.extend(("path", path) for path in PATH_RE.findall(line))
    return refs


@lru_cache(maxsize=None)
def _top_level_names(module_file: Path) -> frozenset:
    names = set()
    for node in ast.parse(module_file.read_text()).body:
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update((a.asname or a.name).split(".")[0] for a in node.names)
    return frozenset(names)


def _module_file(lib: Path, parts: list[str]) -> Optional[Path]:
    base = lib.joinpath(*parts)
    for candidate in (base.with_suffix(".py"), base / "__init__.py"):
        if candidate.is_file():
            return candidate
    return None


def resolves(dotted: str, lib: Path) -> bool:
    """Longest module prefix of dotted exists and the next part is a top-level name in it."""
    parts = dotted.split(".")
    for i in range(len(parts), 0, -1):
        module_file = _module_file(lib, parts[:i])
        if module_file:
            return i == len(parts) or parts[i] in _top_level_names(module_file)
    return False


def namespace_package(namespace: str, lib: Path) -> Optional[str]:
    """Map galaxy_files_sources to galaxy.files.sources, keeping underscores that are part of a name."""
    tokens = namespace.split("_")
    path: list[str] = []
    start = 0
    while start < len(tokens):
        for end in range(len(tokens), start, -1):
            segment = "_".join(tokens[start:end])
            candidate = lib.joinpath(*path, segment)
            if candidate.is_dir() or candidate.with_suffix(".py").is_file():
                path.append(segment)
                start = end
                break
        else:
            return None
    return ".".join(path)


def _defines_class(package: str, class_name: str, lib: Path) -> bool:
    base = lib.joinpath(*package.split("."))
    files = sorted(base.rglob("*.py")) if base.is_dir() else [base.with_suffix(".py")]
    pattern = re.compile(rf"^\s*class\s+{class_name}\b", re.M)
    return any(pattern.search(f.read_text()) for f in files)


def missing_refs(text: str, galaxy_root: Path) -> list[str]:
    """References in text that don't exist in galaxy_root, in diagram order."""
    lib = galaxy_root / "lib"
    missing: list[str] = []
    packages: dict[str, Optional[str]] = {}
    for kind, value in diagram_refs(text):
        if kind == "path":
            gone = None if (galaxy_root / value).exists() else value
        elif kind == "dotted":
            gone = None if resolves(value, lib) else value
        elif kind == "namespace":
            packages[value] = namespace_package(value, lib)
            gone = None if packages[value] else value
        else:
            namespace, name = value
            package = packages[namespace]
            if package is None:
                continue
            if "." in name:
                relative = f"{package}.{name}"
                gone = None if resolves(relative, lib) or resolves(name, lib) else relative
            else:
                gone = None if _defines_class(package, name, lib) else f"{package}.{name}"
        if gone and gone not in missing:
            missing.append(gone)
    return missing


def check_diagrams(images_dir: Path, galaxy_root: Path) -> dict[str, list[str]]:
    """Map each hand-written diagram name to the references missing from galaxy_root."""
    missing = {}
    for diagram in sorted(images_dir.glob("*.mmd")):
        if diagram.name.endswith(".mindmap.mmd"):
            continue
        gone = missing_refs(diagram.read_text(), galaxy_root)
        if gone:
            missing[diagram.name] = gone
    return missing


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--images-dir', type=Path, default=Path('images'))
    parser.add_argument('--galaxy-root', type=Path, help='Galaxy checkout (default: $GALAXY_ROOT)')
    args = parser.parse_args()

    try:
        galaxy_root = resolve_galaxy_root(args.galaxy_root)
    except RepoRootError as e:
        print(f"❌ {e}")
        sys.exit(1)

    missing = check_diagrams(args.images_dir, galaxy_root)
    for name, refs in missing.items():
        print(f"{name}:")
        for ref in refs:
            print(f"  ⚠️  Not found: {ref}")
    if missing:
        sys.exit(1)
    print(f"✓ All diagram references exist in {galaxy_root}")


if __name__ == "__main__":
    main()
