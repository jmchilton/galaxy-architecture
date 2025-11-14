.PHONY: help validate validate-files build-slides build-sphinx build clean view-sphinx lint-sphinx images

help:
	@echo "Galaxy Architecture Documentation - Build Targets"
	@echo ""
	@echo "Verification:"
	@echo "  make validate          Validate all topics (metadata.yaml, content.yaml)"
	@echo "  make validate-files    Verify file references in mindmaps exist in ~/workspace/galaxy"
	@echo "  make lint-sphinx       Check Sphinx build for broken image references"
	@echo ""
	@echo "Build:"
	@echo "  make build             Build all output formats (slides + sphinx)"
	@echo "  make build-slides      Generate training slides for GTN"
	@echo "  make build-sphinx      Generate Sphinx documentation"
	@echo ""
	@echo "Development:"
	@echo "  make view-sphinx       Build and open Sphinx docs in browser"
	@echo "  make clean             Remove all generated files"
	@echo ""
	@echo "Examples:"
	@echo "  make validate          # Validate all topics"
	@echo "  make build             # Build everything"
	@echo "  make view-sphinx       # Build and view HTML docs"

validate:
	@echo "Validating topics..."
	uv run python scripts/validate.py

validate-files:
	@echo "Validating file references in mindmaps..."
	uv run python scripts/generate_files_prose.py images/ topics/files/fragments/

lint-sphinx:
	@echo "Linting Sphinx output for broken images..."
	uv run python scripts/sphinx_image_linter.py

build-slides:
	@echo "Building training slides..."
	@for topic in $$(ls -d topics/*/metadata.yaml 2>/dev/null | xargs -I {} dirname {} | xargs basename -a); do \
		echo "  Generating slides for: $$topic"; \
		uv run python outputs/training-slides/build.py $$topic || exit 1; \
	done
	@echo "✓ Training slides built"

build-sphinx: images
	@echo "Building Sphinx documentation..."
	uv run python outputs/sphinx-docs/build.py all
	@echo "Building HTML..."
	uv run --extra docs sphinx-build -b html doc/source doc/build/html
	@echo "Copying images for slide support..."
	@mkdir -p doc/build/html/images
	@cp images/*.png images/*.svg doc/build/html/images/ 2>/dev/null || true
	@echo "✓ Sphinx documentation built"

images:
	@echo "Building PlantUML diagrams..."
	@make -C images all

build: validate build-slides build-sphinx
	@echo ""
	@echo "✓ All artifacts built successfully"

view-sphinx: build-sphinx
	@echo "Opening Sphinx documentation in browser..."
	@if command -v open >/dev/null 2>&1; then \
		open doc/build/html/index.html; \
	elif command -v xdg-open >/dev/null 2>&1; then \
		xdg-open doc/build/html/index.html; \
	else \
		echo "Open doc/build/html/index.html in your browser"; \
	fi

clean:
	@echo "Cleaning generated files..."
	rm -rf doc/build
	rm -rf outputs/training-slides/generated
	rm -rf outputs/sphinx-docs/generated
	rm -f images/*.svg
	@echo "✓ Cleaned"
