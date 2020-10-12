#!/usr/bin/env python3

import os
import sys

from pathlib import Path


####################
# Project Metadata #
####################

project_dir = Path(os.pardir).resolve()
sys.path.insert(0, project_dir / 'src')


about = {}
about_path = project_dir / 'src' / 'audio_metadata' / '__about__.py'
exec(about_path.read_text(), about)

project = about['__title__']
copyright = about['__copyright__']
author = about['__author__']
version = about['__version__']
release = about['__version__']


##############
# Extensions #
##############

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.extlinks',
	'sphinx.ext.intersphinx',
	'sphinx.ext.napoleon',
	'sphinx.ext.viewcode',
	'myst_parser',
]


##################
# Sphinx Options #
##################

default_role = "any"
templates_path = ['_templates']
source_suffix = '.md'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
add_function_parentheses = False
add_module_names = True
highlight_language = 'python3'
todo_include_todos = True


#######################
# Intersphinx Options #
#######################

intersphinx_mapping = {
	'python': ('https://docs.python.org/3', None),
	'bidict': ('https://bidict.readthedocs.io/en/master/', None),
}


################
# MyST Options #
################

myst_admonition_enable = True
myst_deflist_enable = True


################
# HTML Options #
################

html_show_sourcelink = False
html_show_sphinx = False

html_theme = 'furo'
html_title = 'audio-metadata'
