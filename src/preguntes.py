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
import csv
import gettext

from common.freevialglob import *
from common.uncompress import Uncompressor
from common.globals import GlobalVar, Global
from common.database import Database


class LoadDatabase:
	
	def __init__(self, directory):
		""" Load a question database (directory or compressed file). """
		
		try:
			self.files = self._csv_in_path(self._get_real_path(directory))
		
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
	
	
	def _csv_in_path(self, directory):
		
		files = []
		
		for file in self._files_in_path(directory):
			if file[-4:] == '.csv': files.append(file)
		
		return files
	
	
	def _files_in_path(self, directory):
		""" Returns a list with the name of all the files in the given directory. """
		
		for files in (files for dirpath, dirnames, files in os.walk(directory)):
			return [ '%s' % os.path.abspath(os.path.join(directory, file)) for file in files ]


def GetDatabase( num, csvFile ):
	""" Returns a Database instance with the questions from a CSV file. """
	
	csv_read = csv.reader( open( csvFile ) )
	
	comptaline  = 0
	error_count = 0
	
	for line in csv_read:
		
		comptaline += 1
		
		if comptaline > 16:
			
			if len(line) < 9:
				print 'Error in database file «%s», line %d: expected %d values, found %d.' % (os.path.basename(csvFile), comptaline, 10, len(line))
				error_count += 1
				
				if error_count < 3:
					continue
				else:
					print 'Found 3 problems, this will abort the game.'
					sys.exit(1)
			elif len(line) == 9:
				line.append('')
			
			for num in range(0, 10):
				line[ num ] = unicode(line[ num ], 'utf-8')
			
			for num in (5, 8):
				try:
					line[ num ] = int(line[ num ])
				except ValueError:
					line[ num ] = 0
			
			database.addQuestion(
				question = line[1],
				answ1 = line[1 + line[5]],
				answ2 = line[3] if line[5] != 2 else line[2],
				answ3 = line[4] if line[5] != 3 else line[2],
				author = line[6],
				comments = line[9],
				)
		
		# Get information from the header lines
		elif comptaline == 1: continue
		elif comptaline == 2: name = unicode( line[1], 'utf-8' )
		elif comptaline == 3: time = [ unicode( line[1], 'utf-8' ) ]
		elif comptaline == 4: time.append( unicode( line[1], 'utf-8' ) )
		elif comptaline == 5: authors = unicode( line[1], 'utf-8' )
		elif comptaline == 6: description = unicode( line[1], 'utf-8' )			
		elif comptaline == 7: players = unicode( line[1], 'utf-8' )
		elif comptaline == 8: language = unicode( line[1], 'utf-8' )
		elif comptaline == 9: image = unicode( line[1], 'utf-8' )
		elif comptaline == 10:
			sound = unicode( line[1], 'utf-8' )
			database = Database( num, name, language, description, players, authors, time, image, sound )
	
	return database

###########################################

categoriespreguntes = []
arxius_de_preguntes = LoadDatabase(Global.database).get()

for num in range(0, len(arxius_de_preguntes) ):
	try:
		cat = GetDatabase( num + 1, os.path.join(Global.database, arxius_de_preguntes[num]) )
		categoriespreguntes.append( cat )
	except ValueError:
		print 'Error with «%s».' % arxius_de_preguntes[num]

def textCategoria( ncat ):

	return categoriespreguntes[ncat].name

def preguntes_autors():

	llista = []

	for num in range(0, 6):	
		llista.append( categoriespreguntes[num].name + ": " + categoriespreguntes[num].authors )
	
	return llista

def nomImatgeCategoria( ncat ):

	return categoriespreguntes[ncat].image

def soCategoria( ncat ):

	return categoriespreguntes[ncat].sound

def get_categoriespreguntes( ):

	return categoriespreguntes
