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

class GlobalVar:
	
	def __repr__( self ):
		
		return str(vars(self))
	
	
	def __str__( self ):
		
		return self.__repr__()


Global = GlobalVar()

Global.DEBUG_MODE = False
Global.SOUND_MUTE = False
Global.MUSIC_MUTE = False
Global.DISPLAY_FPS = False
Global.LOCKED_MODE = False
Global.FS_MODE = False	# Fullscreen Mode

Global.screen_x = 1024
Global.screen_y = 768
Global.fps_limit = 40

Global.basefolder = '../data'
Global.database = '../questions_db'

Global.folders = {
		'images': os.path.join(Global.basefolder, 'images'),
		'sounds': os.path.join(Global.basefolder, 'sounds'),
		'fonts': os.path.join(Global.basefolder, 'fonts'),
		'help': os.path.join(Global.basefolder, 'help'),
	}


def mute( sound = None, music = None ):
	""" Mute sound or music. """
	
	global SOUND_MUTE, MUSIC_MUTE
	
	if sound: SOUND_MUTE = sound
	if music: MUSIC_MUTE = music
	
	return {
			'sound': SOUND_MUTE,
			'music': MUSIC_MUTE,
		}
