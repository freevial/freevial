#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Freevial
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

import sys, os.path, pygame
from math import *

from freevialglob import *
from score import Score
from preguntador import Preguntador
from roda import Roda


##################################################
#
# Classe de control del programa
#

class Freevial:

	###########################################
	#
	def __init__( self ):
	
		self.joc = Freevial_globals()
	
	
	###########################################
	# Iniciem partida
	#
	def inici( self ):
		
		# inicialize presentation surface
		self.joc.pantalla = pygame.display.set_mode( ( self.joc.mida_pantalla_x, self.joc.mida_pantalla_y), HWSURFACE, 32)
		pygame.display.set_caption('Freevial')
		pygame.display.set_icon( pygame.image.load(os.path.join(self.joc.folders['images'], 'logo.png')) )
		
		if not DEBUG_MODE:
			pygame.mouse.set_visible( False )
			pygame.display.toggle_fullscreen()
		
		# inicialize sound and text systems
		if not ismute(): 
			pygame.mixer.pre_init(44100, -16, 2, 2048)
			pygame.mixer.init()

		pygame.font.init()
		
		self.joc.sfc_credits = createHelpScreen( 'credits', alternate_text = True )

		initTextos()
		init_joystick()
	
	###########################################
	#
	# Control principal del programa
	#
	def juguem( self ):
		
		self.inici()
		
		score = roda = fespregunta = None

		while 1:
			
			if not score: score = Score( self.joc )
			
			self.joc.equip_actual = score.juguem( self.joc )
			
			if self.joc.equip_actual != -1:
				
				self.joc.rondes += 1		
				
				if not roda: roda = Roda( self.joc )
				
				resultat = roda.juguem( self.joc )
				
				if resultat != 0:
						
					self.joc.equips[ self.joc.equip_actual].preguntes_tot[resultat-1] += 1		
					
					if not fespregunta:	fespregunta = Preguntador( self.joc )
					
					resultat = fespregunta.juguem( resultat )	
					
					if resultat > 0:
						self.joc.equips[ self.joc.equip_actual].preguntes_ok[resultat-1] += 1
						self.joc.equips[ self.joc.equip_actual].punts += 1
						
						fig_abans = self.joc.equips[ self.joc.equip_actual].figureta
						self.joc.equips[ self.joc.equip_actual].activaCategoria( resultat ) 
						
						if fig_abans != 63 and self.joc.equips[ self.joc.equip_actual].figureta == 63:
							self.joc.equips[ self.joc.equip_actual].punts += 2
						
					self.joc.equip_actual = seguentEquipActiu( self.joc.equips, self.joc.equip_actual )
			else:
				sys.exit()


if '-d' in sys.argv or '--debug' in sys.argv:
	DEBUG_MODE = True

if '--fps' in sys.argv:
	displayFPS( True )

if '-m' in sys.argv or '--mute' in sys.argv:
	mute( sound = True, music = True )

if '--no-sound' in sys.argv:
	mute( sound = True )

if '--no-music' in sys.argv:
	mute( music = True )

try:
	joc = Freevial()
	joc.juguem()
	
except KeyboardInterrupt:
	print 'Manual abort.'
	sys.exit()
