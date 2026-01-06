# PR #9938: Implement more Galaxy Markdown components

**Author:** jmchilton
**Merged:** 2020-07-03
**URL:** https://github.com/galaxyproject/galaxy/pull/9938

## Summary

Added metadata-focused directives for embedding contextual information in reports.

## Key Changes

**New Directives:**
- `invocation-time` - ISO timestamp of workflow invocation
- `generate-time` - ISO timestamp of markdown generation
- `generate-galaxy-version` - Galaxy MAJOR_VERSION at generation time
- `dataset-type` - Dataset ext/format/datatype
- `dataset-name` - Dataset name

## Architectural Implications

**Report Context Metadata:** These directives enable reports to document when/where/how they were generated. Critical for reproducibility and understanding report provenance.

**Version Tracking:** Including Galaxy version in reports helps understand compatibility and feature availability.

## Documentation Focus

- Show examples of using metadata directives in report headers/footers
- Explain reproducibility benefits
- Demonstrate combining metadata with dataset displays
