.PHONY: all clean

MINDMAPS := $(wildcard *.mindmap.yml)
MINDMAP_INPUTS := $(MINDMAPS:.mindmap.yml=.mindmap.plantuml.txt)
OTHER_INPUTS := $(filter-out %.mindmap.plantuml.txt, $(wildcard *.plantuml.txt))
ALL_INPUTS := $(MINDMAP_INPUTS) $(OTHER_INPUTS)
OUTPUTS := $(ALL_INPUTS:.txt=.svg)

all: plantuml.jar $(OUTPUTS)

$(MINDMAP_INPUTS): $(MINDMAPS)
	uv run python mindmap_yaml_to_plantuml.py $(MINDMAPS)

$(OUTPUTS): $(ALL_INPUTS)
	java -jar plantuml.jar -c plantuml_options.txt -tsvg $(ALL_INPUTS)

plantuml.jar:
	wget http://jaist.dl.sourceforge.net/project/plantuml/plantuml.jar || curl --output plantuml.jar http://jaist.dl.sourceforge.net/project/plantuml/plantuml.jar

clean:
	rm -f *.platnuml.svg
	rm -f *.mindmap.plantuml.txt
