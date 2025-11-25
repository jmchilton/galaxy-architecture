.PHONY: help validate validate-files build-slides build-sphinx build clean view-sphinx lint-sphinx images watch watch-sphinx watch-images sync-to-training compare-slides validate-sync

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
	@echo "Watch (requires entr: brew install entr):"
	@echo "  make watch             Watch content.yaml files, rebuild sphinx on change"
	@echo "  make watch-images      Watch image sources, rebuild on change"
	@echo ""
	@echo "Sync to training-material:"
	@echo "  make compare-slides    Compare slides with training-material"
	@echo "  make sync-to-training  Sync slides to training-material (dry-run)"
	@echo "  make validate-sync     Validate synced content"
	@echo ""
	@echo "Examples:"
	@echo "  make validate          # Validate all topics"
	@echo "  make build             # Build everything"
	@echo "  make view-sphinx       # Build and view HTML docs"
	@echo "  make compare-slides    # Compare with training-material"

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
	@echo "Copying slides HTML..."
	@for topic in $$(ls -d outputs/training-slides/generated/architecture-*/); do \
		topic_name=$$(basename "$$topic"); \
		topic_id=$${topic_name#architecture-}; \
		mkdir -p doc/build/html/architecture/$$topic_id; \
		cp $$topic/slides.html doc/build/html/architecture/$$topic_id/; \
	done
	@echo "✓ Sphinx documentation built"

images:
	@echo "Building PlantUML diagrams..."
	@make -C images all

build: validate build-slides build-sphinx lint-sphinx
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
	@make -C images clean
	@echo "✓ Cleaned"

# Watch targets (require entr: brew install entr)
watch: watch-sphinx

watch-sphinx:
	@echo "Watching content.yaml files for changes..."
	@echo "Press Ctrl+C to stop"
	find topics -name 'content.yaml' | entr -c make build

watch-images:
	@echo "Watching image sources for changes..."
	@echo "Press Ctrl+C to stop"
	find images -name '*.plantuml.txt' -o -name '*.mindmap.yml' | entr -c make images

# Sync to training-material targets
compare-slides:
	@echo "Comparing slides with training-material..."
	uv run python scripts/compare_slides.py --all

sync-to-training:
	@echo "Syncing to training-material (DRY RUN)..."
	@echo "This will show what would be synced without making changes."
	@echo ""
	uv run python scripts/sync_to_training_material.py --all --dry-run
	@echo ""
	@echo "To actually sync, run:"
	@echo "  uv run python scripts/sync_to_training_material.py --all"

validate-sync:
	@echo "Validating sync to training-material..."
	uv run python scripts/validate_sync.py
