#!/usr/bin/env python3
"""Sync generated agentic operations to review/generated_commands/ with renaming."""

import shutil
from pathlib import Path

import yaml

REVIEW_DIR = Path(__file__).parent
ROOT_DIR = REVIEW_DIR.parent
SOURCE_DIR = ROOT_DIR / "generated_agentic_operations" / "commands"
TARGET_DIR = REVIEW_DIR / "generated_commands"
MAPPING_FILE = REVIEW_DIR / "generated_commands.yaml"


def main():
    with open(MAPPING_FILE) as f:
        config = yaml.safe_load(f)

    TARGET_DIR.mkdir(exist_ok=True)

    for cmd in config.get("commands", []):
        source = SOURCE_DIR / cmd["source"]
        target = TARGET_DIR / cmd["target"]

        if not source.exists():
            print(f"WARNING: {source} not found, skipping")
            continue

        shutil.copy(source, target)
        print(f"Copied {cmd['source']} -> {cmd['target']}")


if __name__ == "__main__":
    main()
