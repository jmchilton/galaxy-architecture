#!/usr/bin/env python3
"""Tests for resolving external repository checkouts (Galaxy, GTN)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from repo_roots import RepoRootError, resolve_galaxy_root, resolve_gtn_root


def test_explicit_path_wins_over_env(tmp_path, monkeypatch):
    other = tmp_path / "other"
    other.mkdir()
    monkeypatch.setenv("GALAXY_ROOT", str(other))
    assert resolve_galaxy_root(tmp_path) == tmp_path


def test_env_var_used_when_no_explicit_path(tmp_path, monkeypatch):
    monkeypatch.setenv("GTN_ROOT", str(tmp_path))
    assert resolve_gtn_root(None) == tmp_path


def test_env_var_expands_user(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    (tmp_path / "galaxy").mkdir()
    monkeypatch.setenv("GALAXY_ROOT", "~/galaxy")
    assert resolve_galaxy_root(None) == tmp_path / "galaxy"


def test_unset_env_var_errors_naming_it(monkeypatch):
    monkeypatch.delenv("GALAXY_ROOT", raising=False)
    with pytest.raises(RepoRootError, match="GALAXY_ROOT"):
        resolve_galaxy_root(None)


def test_missing_directory_errors(tmp_path, monkeypatch):
    monkeypatch.setenv("GTN_ROOT", str(tmp_path / "nope"))
    with pytest.raises(RepoRootError, match="nope"):
        resolve_gtn_root(None)
