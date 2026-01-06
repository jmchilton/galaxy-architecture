# Galaxy Markdown Architecture - Claude Context

You are an expert on Galaxy's markdown system for portable, reproducible documentation.

## Core Concepts

- Galaxy Markdown enables **portable documentation** with embedded Galaxy objects
- **Contextual addressing** allows multiple formats to converge to internal IDs
- Uses **handler pattern** for lazy (frontend) vs eager (PDF) export
- **27+ directives** for embedding datasets, workflows, jobs, and metadata

## Key Files to Reference

Backend:
- `lib/galaxy/managers/markdown_parse.py` - Pure parsing, no Galaxy deps (reusable in gxformat2)
- `lib/galaxy/managers/markdown_util.py` - Galaxy integration, ID resolution, rendering

Frontend:
- `client/src/components/Markdown/Markdown.vue` - Main rendering component
- `client/src/components/Markdown/parse.ts` - Section parsing
- `client/src/components/Markdown/Sections/MarkdownGalaxy.vue` - Galaxy directive processing
- `client/src/components/Markdown/Sections/Elements/` - 21+ specialized renderers
- `client/src/components/Markdown/MarkdownEditor.vue` - Dual-mode editor
- `client/src/components/Markdown/directives.yml` - Directive metadata for editor UI

## Architecture Pattern

```
Contextual Format → markdown_parse.py → markdown_util.py → Handler → Output
                        (validate)        (resolve IDs)     (export)

Context Sources:
- Workflow Markdown (step/output labels)
- Tool Output Markdown (output references)  
- Page API (encoded IDs)
- History Markdown (future: history-relative)

All converge to Internal Galaxy Markdown with numeric IDs.
```

## Directive Syntax

```markdown
Block directive:
```galaxy
history_dataset_as_table(history_dataset_id=12345, title="Results")
```

Inline directive:
Text with ${galaxy history_dataset_name(output="results")} embedded.
```

## Directive Categories

- **Dataset:** display, as_image, as_table, peek, info, link, name, type
- **Workflow:** display, image, license, invocation_inputs/outputs
- **Job:** parameters, metrics, tool_stdout/stderr
- **Meta:** generate_time, generate_galaxy_version, invocation_time
- **Instance:** 6 instance_*_link variants

## Handler Pattern

```python
GalaxyInternalMarkdownDirectiveHandler (abstract)
├── ReadyForExportMarkdownDirectiveHandler
│   └── Lazy: collects metadata, preserves directives (frontend)
└── ToBasicMarkdownDirectiveHandler
    └── Eager: fully expands to standard markdown (PDF)
```

## Frontend Component Tree

```
Markdown.vue
├── parseMarkdown() → Section[]
└── SectionWrapper (dispatcher)
    ├── MarkdownDefault (standard MD + KaTeX)
    ├── MarkdownGalaxy (Galaxy directives)
    ├── MarkdownVega (Vega-Lite specs)
    ├── MarkdownVisualization (Galaxy viz plugins)
    └── MarkdownVitessce (spatial data)
```

## Three Document Types

| Type | Editable | Scope | Use Case |
|------|----------|-------|----------|
| Reports | No | Invocation | Workflow output docs |
| Pages | Yes | Any | User documentation |
| Tool Output | No | Job | Tool-generated reports |

## When Updating This Topic

1. **Verify examples** against current Galaxy codebase
2. **Check** if directive list has changed
3. **Update** `related_code_paths` in metadata.yaml if new files are relevant
4. **Regenerate** all outputs: `/sync-slides markdown`
5. **Run validation**: `/validate-topic markdown`

## Common Questions

**Q: Why Galaxy Markdown instead of HTML?**
A: HTML embeds instance-specific URLs. Galaxy Markdown uses contextual references that resolve at runtime, making docs portable.

**Q: How do I add a new directive?**
A: 1) Add to ALLOWED_ARGUMENTS in markdown_parse.py, 2) Add handler method in markdown_util.py, 3) Create Element component in frontend, 4) Add to directives.yml.

**Q: What's the difference between page and report mode?**
A: Pages can reference any object in the instance. Reports reference "this" invocation using step/output labels.

**Q: How does PDF export work?**
A: ToBasicMarkdownDirectiveHandler expands all directives to standard markdown, then markdown→HTML→WeasyPrint→PDF.

**Q: How does the frontend cache data?**
A: Element components use Pinia stores (invocationStore, workflowStore, datasetStore) which cache API responses and share across multiple elements.
