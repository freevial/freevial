# -*- coding: utf-8 -*-
 
#
# Freevial
# Teams and Puntuation
#
# Copyright (C) 2007, 2008 The Freevial Team
#
# By Carles Oriol <carles@kumbaworld.com>
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
import os.path
import random
import pygame
from math import *
from pygame.locals import *

from common.globals import Global
from common.freevialglob import *
from common.events import EventHandle
from common.dialog_question import fesPregunta
from endscreen import Visca
from selcat import *
from skiner import Skin

##################################################
#
# Empaquetat en una classe del selector d'teams
#

class Score:

	###########################################
	#
	def __init__( self, joc ):
		
		self.joc = joc
		self.skin = Skin()
		
		self.skin.scoreCarrega ()


		self.help_overlay = createHelpScreen( 'score' )

		self.help_on_screen = helpOnScreen( HOS_SCORE_MODE0 )

		
	###########################################
	#
	# Bucle principal del programa
	#
	def juguem( self ):


		frate = frameRate( Global.fps_limit )
		
		self.joc.screen.fill( (0,0,0,0) )
		
	
		ypos = escriu = atzar = mou_fons = mostra_ajuda = mostra_credits = mostra_estad = 0
		element_seleccionat = self.joc.current_team
		nou_grup = 1 if ( teamsActius( self.joc.teams ) == 0 ) else 0
		
		# Modes: 0 (choosing teams), 1 (playing),  2 (game ended)
		mode = 1
		
		if nou_grup: mode = 0
		if teamsGuanyador( self.joc.teams ) != -1: 
			mode = 2
			mostra_estad = 1
			element_seleccionat = teamsGuanyador( self.joc.teams )
			self.skin.scoreSoOk()
		else:
			self.skin.scoreSoDeFons ()
		
		surten = 0
		mostrada_victoria = False
		
		self.help_on_screen.activitat()
		
		while 1:
			
			if mode == 2:
				if frate.segons() < 4.1 and int(frate.segons()) > surten:
					surten = int( frate.segons() )
					self.skin.scoreSoOk()
				if frate.segons() > 4.1 and not mostrada_victoria:
					visca = Visca( self.joc )
					resultat = visca.juguem( self.joc, self.joc.teams[teamsGuanyador( self.joc.teams )].nom )
					mostrada_victoria = True
					self.skin.scoreSoDeFons ()
			
			# Event iterator
			for event in pygame.event.get():
				
				eventhandle = EventHandle(event)
				
				self.help_on_screen.activitat(event)
				
				if event.type == pygame.JOYBUTTONDOWN:
					translateJoystickEvent(event)
				
				if eventhandle.isQuit():
					sys.exit()
				
				if eventhandle.keyDown('PRINT'):
					screenshot(self.joc.screen)
				
				if eventhandle.keyUp('F11') or (not escriu and eventhandle.keyUp('f')):
					pygame.display.toggle_fullscreen()
				
				if eventhandle.keyUp('F1') or (not escriu and eventhandle.keyUp('h')):
					mostra_ajuda ^= 1
					mostra_credits = 0
				
				if eventhandle.keyDown('F2'):
					mostra_credits ^= 1
					mostra_ajuda = 0
				
				
				if escriu and not mostra_ajuda and not mostra_credits:


					if eventhandle.keyUp('RETURN', 'ESCAPE', 'KP_ENTER'):
						escriu = 0
						if self.joc.teams[element_seleccionat].nom == '' and eventhandle.isKey('ESCAPE'):
							self.joc.teams[element_seleccionat].actiu = 0
					
					elif eventhandle.isDown():
						
						if eventhandle.isKey('BACKSPACE'):
							if len(self.joc.teams[element_seleccionat].nom) > 0:
								newname = self.joc.teams[element_seleccionat].nom[:-1]
						else:
							newname = self.joc.teams[element_seleccionat].nom + eventhandle.str()
						
						if newname != None:
						
							sfc = self.skin.scoreSfcText( newname )
							
							if sfc.get_width() < 340:
								# Name isn't too long, accept the new character
								self.joc.teams[element_seleccionat].nom = newname
								self.joc.teams[element_seleccionat].sfc_nom = sfc
					
				else:
					
					if eventhandle.keyUp('q', 'ESCAPE'):
						if not mostra_ajuda and not mostra_credits:
							if not Global.LOCKED_MODE:
								if fesPregunta( self.joc.screen , valorText( HOS_QUIT ), (valorText( HOS_YES ), valorText( HOS_NO ))) == 0:
									if not Global.MUSIC_MUTE:
										pygame.mixer.music.fadeout( 500 )
										pygame.time.wait( 500 )
									return -1
						else:
							mostra_ajuda = mostra_credits = 0
					
					if mode == 0:
						
						if eventhandle.keyUp('RIGHT', 'LEFT'):
							element_seleccionat += 1 if (0 == (element_seleccionat % 2)) else -1 
							self.skin.scorePlayClic1() 
						
						if eventhandle.keyUp('DOWN'): 
							element_seleccionat = (element_seleccionat + 2) % 6
							self.skin.scorePlayClic1() 
						
						if eventhandle.keyUp('UP'): 
							element_seleccionat = (element_seleccionat - 2) % 6
							self.skin.scorePlayClic1() 
						
						if eventhandle.keyUp('a'):
							nou_grup = 1
						
						if eventhandle.keyUp('n'):
							if self.joc.teams[element_seleccionat].actiu:
								escriu ^= 1
							else:
								nou_grup = 1
						
						if eventhandle.keyUp('PAGEDOWN') and teamsActius( self.joc.teams ) >= 1:
							element_seleccionat = seguentEquipActiu( self.joc.teams, element_seleccionat )
							self.skin.scorePlayClic1() 
						
						if eventhandle.keyUp('PAGEUP') and teamsActius( self.joc.teams ) >= 1:
							element_seleccionat = anteriorEquipActiu( self.joc.teams, element_seleccionat )
							self.skin.scorePlayClic1()  
						
						if eventhandle.keyUp('r') and teamsActius( self.joc.teams ) > 0:
							atzar = 30 + int( random.randint(0, 30) )
							mode = 1
					
					if eventhandle.keyUp('z'): 
						if self.joc.teams[element_seleccionat].actiu:
							self.joc.teams[element_seleccionat].punts += 1
					
					if eventhandle.keyUp('x'): 
						if self.joc.teams[element_seleccionat].actiu and self.joc.teams[element_seleccionat].punts > 0:
							self.joc.teams[element_seleccionat].punts -= 1
					
					if self.joc.teams[element_seleccionat].actiu:
						for num in range(1, 7):
							if eventhandle.keyUp(str(num), 'KP' + str(num)):
								self.joc.teams[element_seleccionat].canviaCategoria( num )
					
					if eventhandle.isClick('primary') or eventhandle.keyUp('RETURN', 'SPACE', 'KP_ENTER'):

						if mode == 1:
							if not Global.MUSIC_MUTE:
								pygame.mixer.music.fadeout( 2000 )
							return element_seleccionat

						elif mode == 0:
							if self.joc.teams[element_seleccionat].actiu and eventhandle.keyUp('SPACE') :
								atzar = 30 + int( random.randint(0, 30) )
								mode = 1
							else:
								if self.joc.teams[element_seleccionat].actiu: escriu ^= 1
								else: nou_grup = 1
						else:
							if fesPregunta( self.joc.screen , valorText( HOS_NEW_GAME ), (valorText( HOS_YES ), valorText( HOS_NO ))) == 0:
								mode = 0
								mostra_estad = 0 
				
								for equip in self.joc.teams:
									for num in range(0, 6): 
										equip.preguntes_tot[num] = 0
										equip.preguntes_ok[num] = 0
									equip.punts = 0
									equip.figureta = 0				
					
					if eventhandle.keyUp('s'): 
						mostra_estad ^= 1
					
					if eventhandle.keyUp('m'):
						replaceModes = {
								0: 1,
								1: 0,
								2: 1,
							}
						mode = replaceModes[ mode ]

					if eventhandle.keyUp('e') and not Global.LOCKED_MODE :
						self.skin.scoreSoOk()
						visca = Visca( self.joc )
						resultat = visca.juguem( self.joc, self.joc.teams[element_seleccionat].nom )
						mostrada_victoria = True
						self.skin.scoreSoDeFons ()
					
					if eventhandle.keyUp('l'): 
						Global.LOCKED_MODE = (not Global.LOCKED_MODE)

					if eventhandle.keyUp('k', 'F3', 'F5') and mode == 0:
						selcat = SelCat( self.joc )
						selcat.juguem( mode )

			if nou_grup == 1:
				self.skin.scorePlayClic1
				nou_grup = 0
				self.joc.teams[element_seleccionat].actiu ^= 1
				if self.joc.teams[element_seleccionat].actiu and self.joc.teams[element_seleccionat].nom == "": escriu ^= 1

			if atzar != 0 and teamsActius( self.joc.teams ) >= 2:
				element_seleccionat = seguentEquipActiu( self.joc.teams, element_seleccionat )
				atzar -= 1
				self.skin.scorePlayClic2
			else:
				atzar = 0
			
			# Animem el fons
			self.skin.scorePintaFons( self.joc.screen )
			self.skin.scorePintaMascaraDeFons( self.joc.screen )
			self.skin.scorePintaPuntuacions( self.joc.screen, self.joc, element_seleccionat, mode, escriu, mostra_estad, frate )
			self.skin.scorePintaLocked( self.joc.screen )
			
			if mostra_ajuda: self.joc.screen.blit( self.help_overlay, (0,0))
			if mostra_credits: self.joc.screen.blit( self.joc.sfc_credits, (0,0))
			
			self.help_on_screen.draw( self.joc.screen, (350, 740), HOS_SCORE_MODEW if escriu else mode)
			
			frate.next( self.joc.screen )
			
			# Exchange self.joc.screen buffers
			pygame.display.flip()

		return 0
