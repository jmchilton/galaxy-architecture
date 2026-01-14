# PR #16681: Implement Galaxy Markdown directive history_dataset_as_table

**Author:** jmchilton
**Merged:** 2023-12-23
**URL:** https://github.com/galaxyproject/galaxy/pull/16681

## Summary

Added `history_dataset_as_table` directive for embedding tabular data as formatted tables in reports.

## Key Changes

**New Directive:** `history_dataset_as_table` - Renders tabular datasets as HTML tables

**Display Options:**
- Can show entire table or preview
- Handles various tabular formats
- Formatted display suitable for reports and pages

**Use Cases:**
- Embedding sample data in workflow reports
- Showing summary statistics tables
- Displaying results in structured format

## Architectural Implications

**Rich Data Display:** Moves beyond peek/info to actual formatted presentation of tabular data.

**Format Awareness:** Directive understands tabular formats and renders appropriately, rather than just showing raw text.

## Documentation Focus

- Show examples with different table types (simple, multi-column)
- Demonstrate preview vs full table display
- Explain when to use vs peek/info directives
