# -*- coding: utf-8 -*-

#
# Freevial
# Common event-related classes and functions
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

import sys
import re
import pygame

from freevialglob import screenshot


mouseButtons = {
		'primary': 1,
		'secondary': 2,
		'middle': 3,
	}

# Aliases for PS2 remotes
joystick_aliases = {
		0: pygame.K_RETURN,
		1: pygame.K_ESCAPE,
		2: pygame.K_RETURN,
		3: pygame.K_s,
		4: pygame.K_F2,
		5: pygame.K_a,
		6: pygame.K_F1,
		7: pygame.K_F3,
		8: pygame.K_SPACE,
		9: pygame.K_ESCAPE,
		12: pygame.K_UP,
		13: pygame.K_RIGHT,
		14: pygame.K_DOWN,
		15: pygame.K_LEFT,
	}

class EventHandle:
	
	global mouseButtons
	
	
	def __init__( self, event, do_base_actions = True ):
		
		if event.type == pygame.JOYBUTTONDOWN:
			event = self._convert_joystick_event(event)
		
		self.event = event
		self.handled = False
		
		if do_base_actions and self.base_actions():
			self.handled = True
	
	
	def _convert_joystick_event( self, event ):
		
		if joystick_aliases.get( event.button ):
			return pygame.event.Event( pygame.KEYUP, { 'key': joystick_aliases[ event.button ], 'unicode': u's', 'mod': 0 } )
	
	
	def _getKey( self, key ):
		
		if type(key) is str:
			
			if key[:2] != 'K_':
				key = 'K_' + key
			
			key = getattr(pygame, key)
		
		return key
	
	
	def _isKeyEvent( self ):
		
		return hasattr(self.event, 'key') 
	
	
	def _isStateEvent( self ):
		
		return hasattr(self.event, 'state') 
	
	
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
		
		return self._hasKey(keynames)
	
	
	def isUp( self ):
		
		return self.event.type == pygame.KEYUP 
	
	
	def isDown( self ):

		return self.event.type == pygame.KEYDOWN
	
	
	def isClick( self, request = 0 ):
		
		if type(request) is not int:
			request = mouseButtons[ request ]
		
		return self.event.type == pygame.MOUSEBUTTONDOWN and (self.event.button == request or request == 0) 
	
	
	def isRelease( self, request = 0 ):
		
		if type(request) is not int:
			request = mouseButtons[ request ]
		
		return self.event.type == pygame.MOUSEBUTTONUP and (self.event.button == request or request == 0) 
		
	
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
	
	
	def isWindowMinimize( self ):
		
		return self._isStateEvent() and self.event.state == 6 and self.event.gain == 0
	
	def isWindowRestore( self ):
		
		return self._isStateEvent() and self.event.state == 4 and self.event.gain == 1
	
	def isWindowFocusLose( self ):
		
		return self._isStateEvent() and self.event.state == 1 and self.event.gain == 0
	
	def isWindowFocusGain( self ):
		
		return self._isStateEvent() and self.event.state == 1 and self.event.gain == 1
	
	def isQuit( self ):
		
		return  self.event.type == pygame.QUIT
	
	
	def str( self ):
		
		return printKey(self.event.key) if self._isKeyEvent() else ''
		
	
	def base_actions( self ):
		
		if self.isQuit():
			sys.exit()
		
		elif self.keyDown('PRINT'):
			screenshot(pygame.display.get_surface())
			return True
		
		elif self.isWindowFocusLose() or self.isWindowFocusGain():
			# Those aren't interesting, skip them.
			# We could also do some CPU saving here, but this would produce
			# bad synchronization between the music and the images.
			return True
		
		elif self.keyUp('F11'):
			pygame.display.toggle_fullscreen()
			return True
		
		elif self.isWindowMinimize():
			pauseGameUntilRestore()
			return True
		
		else:
			return False


def waitForMouseRelease( ):

	while pygame.mouse.get_pressed()[0] + pygame.mouse.get_pressed()[1] + pygame.mouse.get_pressed()[2] != 0:
		pygame.event.wait() 


def pauseGameUntilRestore( ):
	
	while True:
		for event in pygame.event.get():
			if EventHandle(event).isWindowRestore():
				return False
		
		# Sleep for 10 milliseconds.
		# This has no visible effect but will drastically reduce CPU usage.
		pygame.time.wait(10)


aobert = atancat = adieresi = acirc = False
accents = [u"aeiou", u"àèìòù", u"áéíóú", u"äëïöü", u"âêîôû" ]

def printKey( tecla ):
	""" Translates a pygame Key object for on-game printing of it's value. """

	global aobert, atancat, adieresi, acirc, accents
	
	keyname = pygame.key.name(tecla)
	
	if keyname == 'space': 
		return ' '
	
	if keyname == 'world 71':
		return u'Ç' if pygame.key.get_mods() & pygame.KMOD_SHIFT else u'ç'
		
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
