"""Locate external repository checkouts (Galaxy, training-material).

Explicit paths win; otherwise GALAXY_ROOT / GTN_ROOT environment variables.
"""

import os
from pathlib import Path
from typing import Optional

GALAXY_ROOT_ENV = "GALAXY_ROOT"
GTN_ROOT_ENV = "GTN_ROOT"


class RepoRootError(Exception):
    """Raised when a required checkout can't be located."""


def resolve_repo_root(explicit: Optional[Path], env_var: str, description: str) -> Path:
    """Return the explicit path, else $env_var; error if neither is a directory."""
    if explicit is not None:
        root = Path(explicit).expanduser()
    else:
        value = os.environ.get(env_var)
        if not value:
            raise RepoRootError(
                f"{env_var} is not set - point it at a {description} checkout"
            )
        root = Path(value).expanduser()
    if not root.is_dir():
        raise RepoRootError(f"{description} checkout not found: {root}")
    return root


def resolve_galaxy_root(explicit: Optional[Path] = None) -> Path:
    return resolve_repo_root(explicit, GALAXY_ROOT_ENV, "galaxyproject/galaxy")


def resolve_gtn_root(explicit: Optional[Path] = None) -> Path:
    return resolve_repo_root(explicit, GTN_ROOT_ENV, "galaxyproject/training-material")
