#!/bin/bash
# Build PlantUML diagrams to SVG

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Building PlantUML diagrams..."

# Check if plantuml is available
if command -v plantuml &> /dev/null; then
    echo "Using local plantuml command"
    plantuml -tsvg *.txt
elif command -v docker &> /dev/null; then
    echo "Using Docker plantuml"
    docker run --rm -v "$SCRIPT_DIR:/work" plantuml/plantuml -tsvg /work/*.txt
else
    echo "Error: Neither plantuml command nor docker found"
    echo "Install plantuml: brew install plantuml"
    echo "Or install docker and use: docker pull plantuml/plantuml"
    exit 1
fi

echo "✓ PlantUML diagrams built successfully"

