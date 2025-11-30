# Find Code Paths from PR Research

Extract relevant code paths from PR diffs and add to topic metadata.

## Usage

```
/research-find-code-paths <topic-id>
```

## Arguments

- **topic-id**: Topic identifier (e.g., "dependency-injection", "markdown")

## Examples

```
/research-find-code-paths markdown
/research-find-code-paths dependency-injection
/research-find-code-paths production
```

## What it does

1. Reads all `.diff` files from `topics/<topic-id>/notes/`
2. Extracts modified file paths from the diffs
3. Identifies 8-12 most architecturally significant paths:
   - Core processing/manager classes
   - Main API endpoints
   - Key frontend components
   - Important utilities
4. Verifies each path exists in `~/workspace/galaxy`
5. Adds verified paths to `related_code_paths` in `metadata.yaml` (appends, doesn't replace existing)

## Path selection criteria

Focus on:
- Backend managers and core processing logic
- API endpoints
- Main frontend components (not individual sub-components)
- Configuration and schemas
- Key utilities

Avoid:
- Test files
- Build/config files (package.json, etc.)
- Very granular sub-components unless architecturally significant

## Output format

Each code path added includes:
- `path`: Relative path from Galaxy root
- `note`: Brief description of what it does/why it's relevant

## Requirements

- Topic must have been researched with `/research-topic` (needs `.diff` files)
- Galaxy repository must exist at `~/workspace/galaxy`
