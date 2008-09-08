#! /usr/bin/env python

from distutils.core import setup

import freevial.freevial AS src
version = src.VERSION

setup(
	# Basic Information
	name = 'Freevial',
	version = version,
	description = 'Trivia platform for community events',
	author = 'The Freevial Team',
	author_email = 'freevial-dev@eurion.net',
	url = 'https://launchpad.net/freevial',
	download_url = 'https://launchpad.net/freevial/+download',
	
	# Classifiers
	classifiers = [
		'License :: OSI-Approved :: GNU General Public License (GPL)',
		'Intended Audience :: End USers/Desktop',
		'Development Status :: 5 - Production/Stable',
		'Topic :: Games/Entertainment',
		'Programming Language :: Python',
		'Database Environment :: Database API :: XML-based'
		]
	
	# File installation
	# TODO: The executable should be installed into /usr/games, not /usr/bin
	scripts = ['freevial'],
	packages = ['src', 'src.common'],
	data_files = [
		('games/freevial', ['data']),
		# ...
		]
	)
