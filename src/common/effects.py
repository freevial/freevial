# -*- coding: utf-8 -*-

#
# Freevial
# Commonly used stuff
#
# Copyright (C) 2008 The Freevial Team
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

import pygame

from common.freevialglob import *


class BigLetter:
	
	frames_total = 9
	alpha_mul = 20
	pos_x = 800
	pos_y = 550
	
	def __init__( self ):
		
		self.screen = pygame.display.get_surface()
		self.sfc_character = None
		
		self.frames_left = 0
		self.mode = 0
	
	def frame( self ):
		
		if not self.frames_left:
			return False
		
		if self.frames_left > (self.frames_total / 2):
			alpha = self.alpha_mul * abs(self.frames_left - (self.frames_total+1))
		else:
			alpha = (self.alpha_mul * (self.frames_total / 2)) - self.alpha_mul * ((self.frames_total / 2) - self.frames_left)
		
		sfc_copy = self.sfc_character
		sfc_copy.set_alpha(alpha)
		self.screen.blit(sfc_copy, (self.pos_x, self.pos_y))
		self.frames_left -= 1
	
	def switch_mode( self, mode ):
		
		self.mode = mode
		self.sfc_character = render_text( str(mode), (200,200,200), 150, 0 )
		self.frames_left = self.frames_total
