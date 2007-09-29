# -*- coding: utf-8 -*-

#
# Freevial
# Global Data used all over Freevial
#
# Copyright (C) 2007 The Freevial Team
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

import os.path
import random
import pygame
import gettext

gettext.install('freevial', '/usr/share/locale', unicode=1)


class Global:
	
	def __init__( self ):
		
		self.elements = {}
	
	
	def __contains__( self, var ):
		
		if not var in self.elements:
			raise KeyError, _('There is no program-wide variable called «%s».' % var)
		
		return True
	
	
	def __getitem__( self, var ):
		
		if self.__contains__(var):
			return self.elements[var]
	
	
	def __setitem__( self, var, val ):
		
		self.elements[var] = val
	
	
	def __iter__( self ):
		
		for var in elements:
			yield var
	
	
	def __repr__( self ):
		
		return 'Global() instance holding %d program-wide variables.' % len(self.elements)
	
	
	def __str__( self ):
		
		string = self.__repr__() + '\n'
		
		for var in self.elements:
			string += '\n%s -> %s' % (var, self.elements[var])
		
		return string
	
	
	def extend( self, list ):
		
		self.elements.extend(list)
