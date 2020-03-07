#!/usr/bin/env python3

import os
import sys

import audio_metadata
import sphinx_material

project_dir = os.path.abspath(os.pardir)
sys.path.insert(0, os.path.join(project_dir, 'src'))

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.extlinks',
	'sphinx.ext.intersphinx',
	'sphinx.ext.napoleon',
	'sphinx.ext.viewcode',
	'sphinx_material',
]

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = "any"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = audio_metadata.__title__
copyright = audio_metadata.__copyright__
author = audio_metadata.__author__

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = audio_metadata.__version__
# The full version, including alpha/beta/rc tags.
release = audio_metadata.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = False

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

highlight_language = 'python3'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
	'python': ('https://docs.python.org/3', None),
	'bidict': ('https://bidict.readthedocs.io/en/master/', None),
}

# -- Options for HTML output ----------------------------------------------

html_theme = 'sphinx_material'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
	'nav_title': 'audio-metadata',
	'color_primary': 'blue',
	'color_accent': 'deep-orange',
	'repo_url': 'https://github.com/thebigmunch/audio-metadata',
	'repo_name': 'audio-metadata',
	'globaltoc_includehidden': True,
	'master_doc': False,
}

# Get the them path
html_theme_path = sphinx_material.html_theme_path()
# Register the required helpers for the html context
html_context = sphinx_material.get_html_context()

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

html_sidebars = {
	'**': [
		'globaltoc.html',
		'localtoc.html',
		'searchbox.html',
	]
}
