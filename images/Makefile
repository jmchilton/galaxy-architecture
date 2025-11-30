.PHONY: all clean check-mermaid

# PlantUML sources and outputs
MINDMAPS := $(wildcard *.mindmap.yml)
MINDMAP_INPUTS := $(MINDMAPS:.mindmap.yml=.mindmap.plantuml.txt)
OTHER_PLANTUML_INPUTS := $(filter-out %.mindmap.plantuml.txt, $(wildcard *.plantuml.txt))
ALL_PLANTUML_INPUTS := $(MINDMAP_INPUTS) $(OTHER_PLANTUML_INPUTS)
PLANTUML_OUTPUTS := $(ALL_PLANTUML_INPUTS:.txt=.svg)

# Mermaid sources and outputs
MERMAID_INPUTS := $(wildcard *.mermaid.txt)
MERMAID_OUTPUTS := $(MERMAID_INPUTS:.txt=.svg)

# Combined outputs
ALL_OUTPUTS := $(PLANTUML_OUTPUTS) $(MERMAID_OUTPUTS)

all: plantuml.jar check-mermaid $(ALL_OUTPUTS)

# PlantUML targets
$(MINDMAP_INPUTS): $(MINDMAPS)
	uv run python mindmap_yaml_to_plantuml.py $(MINDMAPS)

$(PLANTUML_OUTPUTS): $(ALL_PLANTUML_INPUTS)
	java -jar plantuml.jar -c plantuml_options.txt -tsvg $(ALL_PLANTUML_INPUTS)

plantuml.jar:
	wget http://jaist.dl.sourceforge.net/project/plantuml/plantuml.jar || curl --output plantuml.jar http://jaist.dl.sourceforge.net/project/plantuml/plantuml.jar

# Mermaid targets
# Prefer local node_modules install, fall back to global
MMDC := $(shell command -v ../node_modules/.bin/mmdc 2>/dev/null || command -v mmdc 2>/dev/null)

check-mermaid:
	@if [ -n "$(MERMAID_INPUTS)" ]; then \
		if [ -z "$(MMDC)" ]; then \
			echo "Warning: mermaid-cli not found."; \
			echo "Install with: npm install (uses package.json) or npm install -g @mermaid-js/mermaid-cli"; \
			echo "Skipping Mermaid diagram generation."; \
			exit 0; \
		fi \
	fi

$(MERMAID_OUTPUTS): %.mermaid.svg: %.mermaid.txt
	@if [ -n "$(MMDC)" ]; then \
		$(MMDC) -i $< -o $@ -b transparent; \
	else \
		echo "Skipping $@ (mermaid-cli not installed)"; \
	fi

clean:
	rm -f *.plantuml.svg
	rm -f *.mermaid.svg
	rm -f *.mindmap.plantuml.txt
