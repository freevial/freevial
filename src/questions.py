# -*- coding: utf-8 -*-
 
#
# Freevial
# Questions Importer
#
# Copyright (C) 2007, 2008 The Freevial Team
#
# By Carles Oriol i Margarit <carles@kumbaworld.com>
# By Siegfried-Angel Gevatter Pujals <siggi.gevatter@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
from lxml import etree, objectify
import gettext

from common.freevialglob import *
from common.uncompress import Uncompressor
from common.globals import GlobalVar, Global
from common.database import Database


class LoadDatabase:
	
	def __init__(self, directory):
		""" Load a question database (directory or compressed file). """
		
		try:
			self.files = self._xml_in_path(self._get_real_path(directory))
		
		except IOError:
			print _('Error: Couldn\'t find the current questions database.')
			print _('You can provide the location to that one you want to use by passing the --database option.')
			print _('For example: freevial --database ~/questions.tar.gz')
			sys.exit(1)
	
	def get(self):
		
		return self.files
	
	def _get_real_path(self, directory):
		""" If the given path is directory it is returned as-is, if it's
		is a compressed file the path to a extracted version to it (on a
		temporal directory) is returned. Else ValueError is raised; if
		the directory/file doesn't exist at all, it raises IOError."""
		
		if not os.path.exists(directory):
			raise IOError, _('Indicated directory of file doesn\'t exist or has wrong permissions.')
		
		if os.path.isdir(directory):
			return directory
		
		ext = os.path.splitext(directory)[1][1:]	# Get the extension
		
		if ext in ('gz', 'bz2', 'zip'):
			return self._extract(directory)
		
		raise ValueError, _('Expected a directory or compressed file.')
	
	def _extract(self, directory):
		""" Extracts a compressed file to a temporal directory and returns
		the URL to it. """
		
		file = Uncompressor(directory)
		tempdir = self._get_temp()
		
		file.extractall(tempdir)
		return tempdir
	
	def _get_temp(self):
		""" Creates a temporary directory."""
		
		import tempfile
		return tempfile.mkdtemp('', 'freevial-') + '/'
	
	def _xml_in_path(self, directory):
		
		files = []
		
		for file in self._files_in_path(directory):
			if file[-4:] == '.xml': files.append(file)
		
		return files
	
	def _files_in_path(self, directory):
		""" Returns a list with the name of all the files in the given directory. """
		
		for files in (files for dirpath, dirnames, files in os.walk(directory)):
			return [ '%s' % os.path.abspath(os.path.join(directory, file)) for file in files ]


# Create the XML parser
parser = etree.XMLParser(remove_blank_text = True)
parser.setElementClassLookup(objectify.ObjectifyElementClassLookup())

def GetDatabase( num, xmlFile ):
	""" Returns a Database instance loaded with the questions from a XML file. """
	
	root = etree.parse(xmlFile, parser).getroot()
	
	if float(root.get('version')) != 1.0:
		print >> sys.stderr, _('Warning: «%»: Database\'s version is %s, which is not supported by the installed version of Freevial. It might not work as expected.') % (xmlFile, root.get('version'))
	
	database = Database(
		num,
		root.information.name.text,
		root.get('language'),
		root.information.description.text,
		root.information.destination.text,
		', '.join(["%s" % author.text.split(',')[0] for author in root.information.authors.getchildren()]),
		(int(root.information.timestamp_creation.text), int(root.information.timestamp_modification.text)),
		root.appearance.image.text,
		root.appearance.sound.text,
	)
	
	for question in root.questions.getchildren():
		
		if question.answers.countchildren() != 3:
			print >> sys.stderr, _('Warning: «%»: Found question with an incorrect number of answers; ignoring it.') % xmlFile
			continue
		
		answers = []
		has_correct_answer = False
		
		# Process answers
		for answer in question.answers.getchildren():
			if answer.get('correct') is not None:
				if has_correct_answer:
					print >> sys.stderr, _('Warning: «%»: Found question with two correct answers; ignoring it.') % xmlFile
					continue
				answers.insert(0, answer.text)
				has_correct_answer = True
			else:
				answers.append(answer.text)
		
		if not has_correct_answer:
			print >> sys.stderr, _('Warning: «%»: Found question without any correct answer; ignoring it.') % xmlFile
			continue
		
		try:
			comment = question.comments.text
		except AttributeError:
			comment = ''
		
		database.addQuestion(
			question = question.sentence.text,
			answ1 = answers[0],
			answ2 = answers[1],
			answ3 = answers[2],
			author = question.author.text,
			comment = comment,
		)
	
	return database


alldatabases = []
database_files = LoadDatabase(Global.database).get()

for num in range(0, len(database_files) ):
	try:
		cat = GetDatabase( num + 1, os.path.join(Global.database, database_files[num]) )
		alldatabases.append( cat )
	except ValueError:
		print 'Error with «%s».' % database_files[num]

def shuffle_databases():
	random.shuffle(alldatabases)

def get_databases( database = None ):
	
	if database is not None:
		return alldatabases[database]
	else:
		return alldatabases
