# PR #16675: Implement instance URLs in Galaxy markdown

**Author:** jmchilton
**Merged:** 2023-11-08
**URL:** https://github.com/galaxyproject/galaxy/pull/16675

## Summary

Added directives for embedding Galaxy instance metadata URLs (citation, support, help, organization, etc.) in markdown documents.

## Key Changes

**New Link Directives:**
- `instance_access_link()` - Main Galaxy instance URL (e.g., https://usegalaxy.org)
- `instance_resources_link()` - Learning/resource URL (e.g., galaxyproject.org)
- `instance_citation_link()` - Citation URL
- `instance_support_link()` - Support URL
- `instance_help_link()` - Help site URL
- `instance_terms_link()` - Terms of service URL
- `instance_organization_link()` - Hosting organization URL

**Configuration:**
- New config values: `instance_access_url`, `instance_resource_url`
- Generalized config: `organization_name`, `organization_url` (used by GA4GH and other APIs)
- Reuses existing: `citation_url`, `support_url`, `helpsite_url`, `terms_url`

**UI Integration:** Directives available in toolbox under expandable "Instance Links" section (not expanded by default since they're niche).

## Architectural Implications

**Instance Branding:** Enables reports/pages to reference instance-specific resources while remaining portable across instances.

**Configuration Reuse:** Leverages existing config values where possible, adds minimal new config surface.

**Template Flexibility:** Reports can include footer/header boilerplate with instance-specific links that automatically adjust per deployment.

## Documentation Focus

- Show example footer with citation, support, help links
- Explain configuration values and their defaults
- Demonstrate how to use for branding/attribution
- Note expandable toolbox section for discovery
