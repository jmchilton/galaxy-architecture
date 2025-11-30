# Research Topic for Content Generation

Research a topic using its metadata to prepare for content.yaml generation.

## Usage

```
/research-topic <topic-id>
```

## Arguments

- **topic-id**: Topic identifier (e.g., "dependency-injection", "startup")

## Examples

```
/research-topic dependency-injection
/research-topic startup
/research-topic production
```

## What it does

1. Loads `topics/<topic-id>/metadata.yaml`
2. Creates `topics/<topic-id>/notes/` directory
3. For each `related_code_paths` entry:
   - Examines the code path (understanding both string and object formats)
   - Summarizes implementation details tailored for documentation
   - Writes to `topics/<topic-id>/notes/path_<rel_path_with_slashes_replaced_with_dashes>.md`
4. For each `related_pull_requests` entry:
   - Fetches PR details from GitHub (understanding both string and object formats)
   - Downloads PR diff using `gh pr diff`
   - Summarizes changes/rationale tailored for documentation
   - Writes to `topics/<topic-id>/notes/pr_<github_org>_<github_repo>_<pr_number>.md`
   - Writes diff to `topics/<topic-id>/notes/pr_<github_org>_<github_repo>_<pr_number>.diff`

## Format handling

Supports both string and object formats:

**Code paths:**
- String: `"lib/galaxy/di/"` → `path_lib_galaxy_di.md`
- Object: `{path: "lib/galaxy/app.py", note: "Main application"}` → `path_lib_galaxy_app.py.md` (uses note to guide summary)

**Pull requests:**
- String: `"12345"` → `pr_galaxyproject_galaxy_12345.md` (assumes galaxyproject/galaxy)
- String URL: `"https://github.com/galaxyproject/galaxy/pull/12345"` → `pr_galaxyproject_galaxy_12345.md`
- Object: `{pull_request: "12345", note: "Adds DI support"}` → `pr_galaxyproject_galaxy_12345.md` (uses note to guide summary)

## Summary content

Each file contains analysis tailored for documentation:
- **Code path summaries**: What the code does, key patterns, examples to highlight
- **PR summaries**: What changed, why it changed, architectural implications

Summaries focus on information needed to write effective training/documentation.

## Implementation

- Uses Task tool with Explore agent for code investigation
- Uses GitHub CLI (`gh pr view`) to fetch PR details
- Uses GitHub CLI (`gh pr diff`) to download PR diffs
- Each code path/PR analyzed independently
- Summaries structured for content generation use

## Requirements

- Topic metadata.yaml must exist with related_code_paths and/or related_pull_requests
- For code paths: paths should exist in Galaxy codebase
- For PRs: GitHub CLI must be available for fetching PR details
