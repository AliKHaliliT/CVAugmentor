# Minimal makefile for Sphinx documentation

SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = docs

.PHONY: help clean html

help:
	@$(SPHINXBUILD) -M help $(SOURCEDIR) $(BUILDDIR)

clean:
	rm -rf $(BUILDDIR)/*

html:
	@$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)
