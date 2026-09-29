# Images Directory

Images used in architecture documentation (slides and Sphinx docs). Shared across topics.

- `*.mmd` - Mermaid diagram sources (rendered to `*.mmd.svg`)
- `*.mindmap.yml` - file trees and concept mindmaps (generated to `*.mindmap.mmd`, then `*.mindmap.mmd.svg`)
- `mermaid_config.json` - Galaxy theme applied to every diagram
- Other `*.svg` / `*.png` - hand-drawn images and screenshots, committed as-is (many originally from GTN `training-material/topics/dev/images/`)

## Building

```bash
make images        # from repo root; renders all diagrams
make watch-images  # rebuild on change
```

Rendered SVGs are gitignored and built in CI. See [docs/DIAGRAM_GUIDE.md](../docs/DIAGRAM_GUIDE.md) for diagram types, conventions and examples.

## Image Paths in Content

Reference images from `topics/<topic>/` as `../../images/<image-name>` (e.g. `../../images/asgi_app.mmd.svg`). This matches the GTN structure where images are shared across topics.
