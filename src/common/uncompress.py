# -*- coding: utf-8 -*-

#
# Freevial
# Compressed Files Extractor
#
# Copyright (C) 2007, 2008 The Freevial Team
#
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

class Uncompressor:
	""" Provides an interface to handle files compressed with both, tar and zip format, the same way.\n """
	
	def __init__(self, filename, mode='r'):
		
		self._open(filename, mode)
	
	
	def _detect(self, filename):
		""" Detect which type of compression the given filename indicates.\n """
		
		ext = os.path.splitext(filename)[1][1:]	# Get the extension
		
		if ext in ('gz', 'bz2'):
			return 'tar'
		
		elif ext == 'zip':
			return 'zip'
		
		else:
			raise ValueError, 'Unsuported file format, expected .tar.gz, .tar.bz or .zip.'
	
	
	def _unzip_all(self, directory):
		""" Extract all members of the current zip file to the given directory. """
		
		for name in self.fileobj.namelist():
			
			if name.endswith('/'):
				os.mkdir(os.path.join(directory, name))
			
			else:
				outfile = open(os.path.join(directory, name), 'wb')
				outfile.write(self.fileobj.read(name))
				outfile.close()

		print "DIRECTORY: ", directory
		return directory
	
	
	def _open(self, filename, mode='r'):
		""" Open a compressed file for reading, writing or appending. """
		
		self.type = self._detect(filename)
		
		if self.type == 'tar':
			import tarfile
			self.fileobj = tarfile.open(filename, mode)
		
		elif self.type == 'zip':
			import zipfile
			self.fileobj = zipfile.ZipFile(filename, mode)
	
	
	def extractall(self, directory='./'):
		"""Extract all members from the archive to the given directory."""
		
		if self.type == 'tar':
			return self.fileobj.extractall(directory)
		
		elif self.type == 'zip':
			return self._unzip_all(directory)



