# -*- coding: utf-8 -*-

#
# Freevial
# Common event-related classes and functions
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
#GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import re
import pygame


mouseButtons = {
		'primary': 1,
		'secondary': 2,
		'middle': 3,
	}

class EventHandle:
	
	global mouseButtons
	
	
	def __init__( self, event ):
		
		self.event = event
	
	
	def _getKey( self, key ):
		
		if type(key) is str:
			
			if key[:2] != 'K_':
				key = 'K_' + key
			
			key = getattr(pygame, key)
		
		return key
	
	
	def _isKeyEvent( self ):
		
		return True if hasattr(self.event, 'key') else False
	
	
	def _hasKey( self, keynames ):
		
		if not self._isKeyEvent():
			return False
		
		if len(keynames) == 1 and type(keynames[0]) is tuple:
			keynames = keynames[0]
		
		for key in keynames:
			
			if self.event.key == self._getKey(key):
				return True
		
		return False
	
	
	def isKey( self, *keynames ):
		
		return True if self._hasKey(keynames) else False
	
	
	def isUp( self ):
		
		return True if self.event.type == pygame.KEYUP else False
	
	
	def isDown( self ):
		
		return True if self.event.type != pygame.KEYDOWN else False
	
	
	def isClick( self, request = 0 ):
		
		if type(request) is not int:
			request = mouseButtons[ request ]
		
		return True if self.event.type == pygame.MOUSEBUTTONDOWN and (self.event.button == request or request == 0) else False
	
	
	def isRelease( self, request = 0 ):
		
		if type(request) is not int:
			request = mouseButtons[ request ]
		
		return True if self.event.type == pygame.MOUSEBUTTONUP and (self.event.button == request or request == 0) else False
	
	
	def keyUp( self, *keynames ):
		
		if not self.isUp():
			return False
		
		if len(keynames) == 0:
			return True
		
		return self.isKey(*keynames)
	
	
	def keyDown( self, *keynames ):
		
		if not self.isDown():
			return False
		
		if len(keynames) == 0:
			return True
		
		return self.isKey(keynames)
	
	
	def isQuit( self, quitKeys = 'ESCAPE' ):
		
		if self.event.type == pygame.QUIT:
			return True
		
		return False
	
	
	def str( self ):
		
		if not self._isKeyEvent():
			return ''
		
		return printKey(self.event.key)


aobert = atancat = adieresi = acirc = False
accents = [u"aeiou", u"àèìòù", u"áéíóú", u"äëïöü", u"âêîôû" ]

def printKey( tecla ):
	""" Translates a pygame Key object for on-game printing of it's value. """

	global aobert, atancat, adieresi, acirc, accents
	
	keyname = pygame.key.name(tecla)
	
	if keyname == 'space': 
		return ' '
	
	if keyname == 'world 71':
		return u'ç'
	
	if keyname == 'tab':
		return '    '
	
	if len(keyname) == 3 and keyname[:1] == '[' and keyname[2:] == ']':
		keyname = keyname[1:2]
	
	pos = accents[0].find( keyname )
	if pos != -1:
		if aobert: keyname = accents[1][pos]
		if atancat: keyname = accents[2][pos]
		if adieresi: keyname = accents[3][pos]
		if acirc: keyname = accents[4][pos]
	
	if pygame.key.get_mods() & pygame.KMOD_SHIFT:
		keyname = keyname.upper()
	
	if tecla == 314:
		if pygame.key.get_mods() & pygame.KMOD_SHIFT:
			atancat = True
		elif pygame.key.get_mods() & pygame.KMOD_CTRL:
			adieresi = True
		elif pygame.key.get_mods() & pygame.KMOD_ALT:
			acirc = True
		else:
			aobert = True
	else:
		aobert = atancat = adieresi = acirc = False
	
	if not re.search(u"^[a-zA-Z0-9,.+'-/*àèìòùáéíóúäëïöüâêîôû ]$", keyname):
		return ''
	
	return keyname
