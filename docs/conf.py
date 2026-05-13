# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'montecarlo'
copyright = '2026, ANuj'
author = 'ANuj'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser',]
source_suffix = {
'.rst': 'restructuredtext',
'.md': 'markdown',
}
# Set the master toctree document to index.md
master_doc = 'index'

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

import os
import sys
# Add the project's src directory to sys.path so Sphinx can import montecarlo.
sys.path.insert(0, os.path.abspath('../src'))
extensions = [
'sphinx.ext.autodoc',
'sphinx.ext.autosummary',
'myst_parser',
]
autosummary_generate = True
autodoc_default_options = {
'members': True,
'imported-members': True,
'undoc-members': True,
'show-inheritance': True,
}
autodoc_mock_imports = ['numpy']