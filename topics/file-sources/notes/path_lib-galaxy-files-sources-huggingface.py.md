# lib/galaxy/files/sources/huggingface.py

## Hugging Face Hub Integration Summary

**Purpose:**
The Hugging Face Hub file source enables Galaxy users to access AI/ML models, datasets, and other artifacts hosted on Hugging Face Hub. This integration allows seamless browsing and retrieval of public and private repositories for use in Galaxy workflows.

**Hub API Integration:**
The implementation leverages two core Hugging Face components:
- **HfFileSystem** - fsspec-based filesystem abstraction for file operations (reading, listing, metadata)
- **HfApi** - Direct API for querying repositories, with support for search and sorting

The integration uses Galaxy's fsspec-based plugin architecture, inheriting from `FsspecFilesSource` to provide standardized file operations.

**Key Features:**
- **Authentication:** Optional API token support for accessing private repositories; defaults to public access without authentication
- **Custom Endpoints:** Configurable endpoint parameter to support self-hosted or alternative Hugging Face instances
- **Repository Discovery:** Root-level listing uses HfApi to enumerate repositories with search and sorting capabilities (by downloads, likes, creation date, trending score, or modification time)
- **File Metadata:** Extracts timestamps from commit history and SHA-256 hashes for Git LFS-stored files
- **Pagination:** Supports limit/offset for browsing large repository lists (max 1000 repositories)

**Implementation Approach:**
The plugin overrides standard fsspec operations to handle the two-tier structure of Hub (repositories → files). Root directory listing uses HfApi to enumerate repositories, while nested paths use HfFileSystem for file operations. Configuration is template-expandable, allowing dynamic token injection. The design maintains Galaxy's file source abstraction while accommodating Hub-specific API patterns.
