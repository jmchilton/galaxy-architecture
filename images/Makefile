.PHONY: all clean check-mermaid

# Mindmap YAML generates an intermediate .mindmap.mmd; hand-written diagrams are *.mmd
MINDMAPS := $(wildcard *.mindmap.yml)
MINDMAP_SOURCES := $(MINDMAPS:.yml=.mmd)
MERMAID_SOURCES := $(sort $(filter-out $(MINDMAP_SOURCES), $(wildcard *.mmd)) $(MINDMAP_SOURCES))
MERMAID_OUTPUTS := $(MERMAID_SOURCES:=.svg)

# Keep generated .mindmap.mmd files (make would otherwise delete intermediates)
.SECONDARY: $(MINDMAP_SOURCES)

# Prefer local node_modules install, fall back to global
MMDC := $(shell command -v ../node_modules/.bin/mmdc 2>/dev/null || command -v mmdc 2>/dev/null)

all: check-mermaid $(MERMAID_OUTPUTS)

check-mermaid:
	@if [ -z "$(MMDC)" ]; then \
		echo "Error: mermaid-cli not found."; \
		echo "Install with: npm install (uses package.json) or npm install -g @mermaid-js/mermaid-cli"; \
		exit 1; \
	fi

%.mindmap.mmd: %.mindmap.yml mindmap_yaml_to_mermaid.py
	uv run python mindmap_yaml_to_mermaid.py $<

%.mmd.svg: %.mmd mermaid_config.json
	$(MMDC) -q -p puppeteer-config.json -c mermaid_config.json -i $< -o $@ -b transparent

clean:
	rm -f *.mmd.svg
	rm -f *.mindmap.mmd
