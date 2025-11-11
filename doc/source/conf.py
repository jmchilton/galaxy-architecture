#
# Galaxy Architecture Documentation - Sphinx Configuration
#
# This is a standalone Sphinx configuration for documenting Galaxy's architecture.
# It mirrors Galaxy's setup but is simplified for this documentation project.

import datetime
import os

# -- General configuration ------------------------------------------------

# Sphinx extensions
extensions = [
    "myst_parser",
    "sphinx.ext.intersphinx",
]

# MyST parser configuration - matches Galaxy's setup
myst_enable_extensions = [
    "attrs_block",
    "deflist",
    "substitution",
    "colon_fence",
]
myst_heading_anchors = 5
myst_heading_slug_func = "docutils.nodes.make_id"

# Source file suffixes
source_suffix = [".rst", ".md"]

# Master toctree document
master_doc = "index"

# Project information
project = "Galaxy Architecture Documentation"
copyright = f"{datetime.datetime.now().year}, Galaxy Committers"
author = "Galaxy Committers"

# Version info (simplified for standalone project)
version = "master"
release = "master"

# Exclude patterns
exclude_patterns = ["**/_*.*", "_build"]

# -- HTML output options --------------------------------------------------

# Theme
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "collapse_navigation": False,
    "display_version": True,
    "navigation_depth": 2,
}

html_baseurl = "https://galaxyproject.org/architecture/"

# Templates path
templates_path = ["_templates"]

# Static files path
html_static_path = ["_static"]

# -- Intersphinx configuration --------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}

# -- MyST configuration ---------------------------------------------------

# Allow headings without surrounding blank lines
myst_commonmark_only = False
