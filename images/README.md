# Images Directory

This directory contains images used in architecture documentation slides.

## Image Sources

All images are sourced from the Galaxy Training Network (GTN) repository:
- Source: `training-material/topics/dev/images/`
- Images are shared across all architecture topics (not topic-specific)

## PlantUML Diagrams

The following PlantUML diagrams are used in the dependency-injection topic:

- `app_py2.plantuml.txt` / `app_py2.plantuml.svg` - Python 2 era app structure
- `app_types_no_interface.plantuml.txt` / `app_types_no_interface.plantuml.svg` - Typed app without interface
- `app_types.plantuml.txt` / `app_types.plantuml.svg` - Typed app with StructuredApp interface
- `app_decomposed.plantuml.txt` / `app_decomposed.plantuml.svg` - Decomposed app structure

## Other Images

- `lagom_ss.png` - Screenshot of Lagom website

## Building PlantUML Diagrams

To regenerate SVG files from PlantUML source:

### Prerequisites

Install PlantUML:
```bash
# macOS
brew install plantuml

# Or use Docker
docker run -v $(pwd):/work plantuml/plantuml -tsvg /work/images/*.txt
```

### Build Commands

```bash
# Build all PlantUML diagrams
cd images
plantuml -tsvg *.txt

# Or build individually
plantuml -tsvg app_py2.plantuml.txt
plantuml -tsvg app_types_no_interface.plantuml.txt
plantuml -tsvg app_types.plantuml.txt
plantuml -tsvg app_decomposed.plantuml.txt
```

### Using Docker

```bash
docker run --rm -v "$(pwd)/images:/work" plantuml/plantuml -tsvg /work/*.txt
```

## Image Paths in Slides

Images are referenced in slides using relative paths:
- From `topics/<topic>/`: `../../images/<image-name>`
- This matches the GTN structure where images are shared across topics

