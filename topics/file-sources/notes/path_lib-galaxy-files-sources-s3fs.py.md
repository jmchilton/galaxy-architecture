# lib/galaxy/files/sources/s3fs.py

## S3-Compatible Storage Plugin Summary

The **S3FsFilesSource** class in `lib/galaxy/files/sources/s3fs.py` implements Galaxy's file source abstraction for S3-compatible storage services using the fsspec library as its foundation.

### Base Class Integration

S3FsFilesSource extends `FsspecFilesSource`, which provides a generic fsspec abstraction framework. This inheritance model allows S3FsFilesSource to leverage fsspec's unified filesystem interface while adding S3-specific path handling and configuration management. The plugin declares its dependency on the `s3fs` Python package (wrapping boto3) and validates this dependency at instantiation time.

### Configuration Architecture

Two configuration classes handle template expansion and resolved values:
- **S3FSFileSourceTemplateConfiguration**: Supports dynamic template variables for `endpoint_url`, `bucket`, `key`, and `secret`
- **S3FSFileSourceConfiguration**: Resolved credentials and connection parameters

Configuration options enable:
- **Anonymous access** via `anon` boolean flag
- **Custom endpoints** through `endpoint_url` (supporting MinIO, DigitalOcean Spaces, etc.)
- **AWS credentials** with `key` and `secret` parameters
- **Bucket specification** as configuration or path prefix

### Key Implementation Details

The `_open_fs()` method constructs an S3FileSystem instance, conditionally passing `client_kwargs` with custom endpoint URLs for non-AWS S3-compatible services. Path handling is specialized through `_to_bucket_path()`, which normalizes paths to bucket-prefixed format (e.g., `bucket/path`), supporting both explicit bucket configuration and `s3://` URIs.

URL scoring in `score_url_match()` ensures security by preventing partial bucket name matches (e.g., `s3://bucket-prefix-different` won't match configured `bucket`). Override methods (`_list`, `_realize_to`, `_write_from`) wrap bucket path conversion before delegating to parent fsspec operations, transparently adapting between user-facing paths and S3 storage conventions.
