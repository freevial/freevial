# -*- coding: utf-8 -*-
 
#
# Freevial
# Category selection
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

import sys
import os
import random
import time
import pygame

from common.freevialglob import *
from common.events import EventHandle
from preguntes import *
from skiner import Skin


##################################################
#
# Empaquetat en una classe del selector
#

class Roda:
	
	def __init__( self, joc ):
		
		self.joc = joc
		self.skin = Skin()
		
		self.skin.rodaCarrega()
		
		
		
	
	def juguem( self ):
		
		self.frate = frameRate( Global.fps_limit )
				
		self.skin.rodaSoEvilStop()
		self.skin.rodaSoDot()
		
		velocitat = 75
		deceleracio = 0
		
		pos = pos_fons = atura = frenant = time_fi = mostra_ajuda = mostra_credits = 0
		rodant = 1
		resultat = -1
		
		self.skin.rodaGira( self.joc )
#		velocitat = 75
#		deceleracio = 0
		
#		pos = pos_fons = atura = frenant = time_fi = mostra_ajuda = mostra_credits = 0
#		rodant = 1
#		resultat = -1
		
#		self.joc.screen.blit( self.fons, (0,0) )

#		nom_equip_sfc = render_text( self.joc.teams[self.joc.current_team].nom, (255,255,255), 30, 1 )
#		nom_equip_sfc = pygame.transform.rotate ( nom_equip_sfc, 90 )
		
#		figureta =  loadImage('points/freevial_tot' + str(self.joc.teams[self.joc.current_team].figureta).zfill(2) + '.png')

#		self.help_on_screen.activitat( )

		while 1:

			for event in pygame.event.get():

				eventhandle = EventHandle(event)
				
				#self.help_on_screen.activitat(event)
				
				if event.type == pygame.JOYBUTTONDOWN:
					translateJoystickEvent(event)
				
				if eventhandle.isQuit():
					sys.exit()
				
				if eventhandle.keyDown('PRINT'):
					screenshot(self.joc.screen)
				
				if eventhandle.keyUp('f', 'F11'):
					pygame.display.toggle_fullscreen()
				
				if eventhandle.keyUp('ESCAPE', 'q') and not Global.LOCKED_MODE:
					if not mostra_ajuda and not mostra_credits:
						if not (Global.MUSIC_MUTE or Global.SOUND_MUTE):
							pygame.mixer.fadeout(500)
						return 0
					else:
						mostra_ajuda = mostra_credits = 0
				
				if eventhandle.keyUp('F1', 'h'):
					mostra_ajuda ^= 1	
					mostra_credits = 0			

				if eventhandle.keyUp('F2'):
					mostra_credits ^= 1
					mostra_ajuda = 0
				
				if (eventhandle.isRelease('primary') or eventhandle.keyUp('RETURN', 'SPACE', 'KP_ENTER')) and rodant == 1:
					if resultat == -1: 	
						atura = 1
					else:
						return resultat
			
			if atura == 1:
				atura = 0
				pas = 3
				deceleracio = 20
				time_fi = time.time()
				
				if not frenant:
					frenant = 1
					self.skin.rodaSoSub()

			if time_fi != 0 and time.time() - time_fi > 2.5:
				return resultat

			# decelerem
			velocitat -= deceleracio
			if velocitat < 0: velocitat = 0
			
			# Si ja hem acabat de rodar afinem la selecció
			# a l'element més proper
			rpos = pos + 100
			if velocitat == 0 and rodant != 0:
				offset = int(rpos) % 200
				if offset != 0: 
					if offset > 100:
						pos += deceleracio if ( offset < (200 - deceleracio) ) else 1
					
					elif offset <= 100:
						pos -= deceleracio if ( offset > deceleracio ) else 1
					
						if pos <= -1200: pos += 1200
				
				else:
					resultat = 1 + int( ( ( - ( pos - 1550 ) / 200 ) ) % 6 )
					self.skin.rodaSoDotStop()
					self.skin.rodaSoCat( resultat )
					if not  self.joc.teams[self.joc.current_team].teCategoria( resultat ):
						self.skin.rodaSoEvil()
					rodant = 0
				
			if rodant == 1:
				pos_fons += velocitat * 2
				if pos_fons >= 768:	pos_fons -= 768
				
				pos -= velocitat
				if pos <= -1200: pos += 1200
				
			self.skin.rodaPinta( self.joc, pos_fons, pos )
						
			#intercanviem els buffers de self.joc.screen
			pygame.display.flip()
