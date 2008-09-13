# -*- coding: utf-8 -*-
 
#
# Freevial
# Questions Importer
#
# Copyright (C) 2007, 2008 The Freevial Team
#
# By Siegfried-Angel Gevatter Pujals <siggi.gevatter@gmail.com>
# By Carles Oriol i Margarit <carles@kumbaworld.com>
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
import gettext
import re
from lxml import etree, objectify

from common.freevialglob import *
from common.uncompress import Uncompressor
from common.globals import GlobalVar, Global
from common.database import Database, Question


class LoadDatabase:
	
	def __init__(self, directory):
		""" Load a question database (directory or compressed file). """

		try:
			dbpath = self._get_real_path(directory)
			Global.databasefolders.append ( dbpath )
			self.files = self._xml_in_path( dbpath )
		
		except IOError:
			print _('Error: Couldn\'t find the current questions database.')
			print _('You can provide the location to that one you want to use by passing the --database option.')
			print _('For example:') + ' freevial --database ~/questions.tar.gz'
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
xsdxml = etree.parse( os.path.join(Global.database, 'freevial-database.xsd') )
xsd = etree.XMLSchema( xsdxml )
parser = etree.XMLParser(remove_blank_text = True, remove_comments = True )
parser.setElementClassLookup(objectify.ObjectifyElementClassLookup())

def filtraText( text ):
    textnet = re.sub('\\s+',' ',text)
    return textnet

def GetDatabase( num, xmlFile ):
	""" Returns a Database instance loaded with the questions from a XML file. """
	
	doc = etree.parse(xmlFile, parser)
	root = doc.getroot()
	
	version = float(root.get('version'))
	
	if str(version) > str(1.2):
		print >> sys.stderr, _(u'Warning: «%(file)s»: Database\'s version is \
%(version)s, which is not supported by the installed version of Freevial. It \
might not work as expected.') % {'file': xmlFile, 'version': root.get('version')}
	else:
		# Validate the file
		xsd.assertValid(doc)	
	
	database = Database(
		num,
		filtraText(root.information.name.text),
		root.get('language'),

		filtraText(root.information.description.text),
		filtraText(root.information.destination.text),
		', '.join(["%s" % filtraText(author.text).split(',')[0] for author in root.information.authors.getchildren()]),

		(int(root.information.timestamp_creation.text), int(root.information.timestamp_modification.text)),
		root.appearance.image.text,
		root.appearance.sound.text,
		version,
	)
	
	for question in root.questions.getchildren():
				
		if question.answers.countchildren() < 3:
			# Support for more than 2 incorrect answers was added in 1.3
			print >> sys.stderr, _(u'Warning: «%s»: Found a question with '
                'less than 3 answers; ignoring it.') % xmlFile
			continue
		
		obj = Question(
			question=question.sentence.text.replace(chr(10), '#'),
			author = question.author.text,
			)
		has_correct_answer = False
		
		# Process answers
		for answer in question.answers.getchildren():
			if answer.get('correct'):
				obj.add_answer(answer.text.replace(chr(10), '#'), True)
				has_correct_answer = True
			else:
				obj.add_answer(answer.text.replace(chr(10), '#'), False)
		
		if not has_correct_answer:
			print >> sys.stderr, _(u'Warning: «%s»: Found a question without '
				'any correct answer; ignoring it.') % xmlFile
			continue
		
		if hasattr(question, 'comments') and question.comments.text is not None:
			obj.comment = question.comments.text
		
		if version >= 1.1:
			# Version 1.1 introduces support for media, more than three answers
			# and different difficulty levels
			if hasattr(question, 'media'):
				obj.mediatype = question.media.get('type')
				obj.media = question.media.text
			difficulty = question.get('difficulty')
			if difficulty:
				difficulty = difficulty.lower().capitalize()
				if difficulty not in ('Easy', 'Medium', 'Hard'):
					print _(u'Warning: «%s»: Found a question with incorrect' +\
						u' difficulty level «%s».') % (xmlFile, difficulty)
				else:
					obj.difficulty = difficulty
		
		if not (Global.DISABLE_MEDIA and obj.mediatype):
			database.add_question(obj)
	
	return database

Global.alldatabases = None

def shuffle_databases():
	
	random.shuffle(Global.alldatabases)

def get_databases( database = None ):
	
	global alldatabases
	
	if not Global.alldatabases:
		
		Global.alldatabases = []
		database_files = LoadDatabase(Global.database).get()
		
		for num in range(0, len(database_files) ):
			try:
				cat = GetDatabase( num + 1, os.path.join(Global.database, database_files[num]) )
			except ValueError:
				print u'Error with «%s».' % database_files[num]
			except etree.DocumentInvalid, e:
				print u'Error with «%s»: %s' % ( database_files[num] , e ) 
			else:
				if len(cat) != 0:
					Global.alldatabases.append( cat )
	
	if database is not None:
		return Global.alldatabases[database]
	else:
		return Global.alldatabases
