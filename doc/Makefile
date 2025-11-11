# Makefile for Sphinx documentation
# Uses uv to run sphinx-build

SPHINXOPTS    ?=
PAPER         ?=
BUILDDIR      ?= build

# Internal variables
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) source
ALLSPHINXOPTS   += --keep-going

.PHONY: help Makefile clean html

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  clean      to remove build files"

clean:
	rm -rf $(BUILDDIR)/*

html:
	uv run sphinx-build -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML files are in $(BUILDDIR)/html/"
