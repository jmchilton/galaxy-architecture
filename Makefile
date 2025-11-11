.PHONY: help validate build-slides build-sphinx build clean view-sphinx

help:
	@echo "Galaxy Architecture Documentation - Build Targets"
	@echo ""
	@echo "Verification:"
	@echo "  make validate          Validate all topics (metadata.yaml, content.yaml)"
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

build-slides:
	@echo "Building training slides..."
	@for topic in $$(ls -d topics/*/metadata.yaml 2>/dev/null | xargs -I {} dirname {} | xargs basename -a); do \
		echo "  Generating slides for: $$topic"; \
		uv run python outputs/training-slides/build.py $$topic || exit 1; \
	done
	@echo "✓ Training slides built"

build-sphinx:
	@echo "Building Sphinx documentation..."
	uv run python outputs/sphinx-docs/build.py all
	@echo "Building HTML..."
	cd doc && uv run sphinx-build -b html source build/html
	@echo "✓ Sphinx documentation built"

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
	@echo "✓ Cleaned"
