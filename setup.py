#!/usr/bin/env python3

import os

from setuptools import find_packages, setup

base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, 'src', 'audio_metadata', '__about__.py')) as f:
	exec(f.read(), about)

setup(
	name=about['__title__'],
	version=about['__version__'],
	description=about['__summary__'],
	url=about['__url__'],
	license=about['__license__'],
	author=about['__author__'],
	author_email=about['__author_email__'],

	keywords=[],
	classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],

	install_requires=[
		'attrs>=18.2',
		'bidict>=0.17',
		'bitstruct >=6.0',
		'more-itertools>=4.0',
		'pprintpp>=0.4'
	],

	extras_require={
		'doc': ['sphinx'],
		'lint': [
			'flake8',
			'flake8-builtins',
			'flake8-import-order',
			'flake8-import-order-tbm'
		],
	},

	packages=find_packages('src'),
	package_dir={
		'': 'src'
	},

	zip_safe=False
)
