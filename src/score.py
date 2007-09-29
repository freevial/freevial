# -*- coding: utf-8 -*-
 
#
# Freevial
# Teams and Puntuation
#
# Copyright (C) 2007 The Freevial Team
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

##################################################
#
# Empaquetat en una classe del selector d'teams
#

class Score:

	###########################################
	#
	def __init__( self, joc ):
		
		self.joc = joc
		
		self.mascara_de_fons = loadImage('fons_score.png')
		self.fons = loadImage('score_fons.png')

		self.element_score = loadImage('element_score.png')
		self.seleccio_score = loadImage('seleccio_score.png')

		self.figureta = range(0,64)
		for num in range(0, 64):
			self.figureta[num] = loadImage('points/freevial_tot' + str( num ).zfill(2) + '.png')	

		self.sfc_cursor = render_text( "_", (0,0,0), 30, 1)

		self.so_sub = loadSound('sub.ogg', volume = 0.1)
		self.so_sub2 = loadSound('sub2.ogg', volume = 0.4)

		self.help_overlay = createHelpScreen( 'score' )

		self.so_ok = loadSound('cheer.ogg')

		self.help_on_screen = helpOnScreen( HOS_SCORE_MODE0 )

		self.sfc_llum = loadImage( 'llum.png' )

	def barra_pos( self, total, posicio, color, ample, alt ):

		sfc = pygame.Surface( ( ample, alt), pygame.SRCALPHA, 32 )
		pygame.draw.rect(sfc, color, (0,0,ample-1,alt-1), 2)

		ample_rect = ample - 8

		pygame.draw.rect(sfc, (color[0], color[1], color[2], 64), (4, 4, ample_rect, alt - 8))
		if total != 0 and posicio != 0: 
			pos_ample = ( posicio * ample_rect ) / total 
			pygame.draw.rect(sfc, color, (4, 4, pos_ample, alt - 8))

		return sfc
	
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
		
		# Estats: 0 (triant teams), 1 (jugant),  2 (final)
		estat = 1
		
		if nou_grup: estat = 0
		if teamsGuanyador( self.joc.teams ) != -1: 
			estat = 2
			mostra_estad = 1
			element_seleccionat = teamsGuanyador( self.joc.teams )
			self.so_ok.play()
		else:
			loadSound( 'score.ogg', volume = 0.6, music = 1).play( -1 )
		
		surten = 0
		mostrada_victoria = False
		
		self.help_on_screen.activitat()
		
		while 1:
			
			if estat == 2:
				if frate.segons() < 4.1 and int(frate.segons()) > surten:
					surten = int( frate.segons() )
					self.so_ok.play()
				if frate.segons() > 4.1 and not mostrada_victoria:
					visca = Visca( self.joc )
					resultat = visca.juguem( self.joc, self.joc.teams[teamsGuanyador( self.joc.teams )].nom )
					mostrada_victoria = True
					loadSound( 'score.ogg', volume = 0.6, music = 1).play( -1 )
			
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
						newname = None
						
						if eventhandle.isKey('BACKSPACE'):
							if len(self.joc.teams[element_seleccionat].nom) > 0:
								newname = self.joc.teams[element_seleccionat].nom[:-1]
						else:
							newname = self.joc.teams[element_seleccionat].nom + eventhandle.str()
						
						if newname != None:
							sfc = render_text( newname, (0,0,0), 30, 1)
							if sfc.get_width() < 340:
								# Name isn't too long, accept the new character
								self.joc.teams[element_seleccionat].nom = newname
								self.joc.teams[element_seleccionat].sfc_nom = sfc
					
				else:
					
					if eventhandle.keyUp('q', 'ESCAPE'):
						if not mostra_ajuda and not mostra_credits:
							if not Global.LOCKED_MODE:
								if fesPregunta( self.joc.screen , valorText( HOS_QUIT ), (valorText( HOS_YES ), valorText( HOS_NO ))) == 0:
									pygame.mixer.music.fadeout( 500 )
									pygame.time.wait( 500 )
									return -1
						else:
							mostra_ajuda = mostra_credits = 0
					
					if estat == 0:
						
						if eventhandle.keyUp('RIGHT', 'LEFT'):
							element_seleccionat += +1 if (0 == (element_seleccionat % 2)) else -1 
							self.so_sub.play() 
						
						if eventhandle.keyUp('DOWN'): 
							element_seleccionat = (element_seleccionat + 2) % 6
							self.so_sub.play() 
						
						if eventhandle.keyUp('UP'): 
							element_seleccionat = (element_seleccionat - 2) % 6
							self.so_sub.play() 
						
						if eventhandle.keyUp('a'):
							nou_grup = 1
						
						if eventhandle.keyUp('n'):
							if self.joc.teams[element_seleccionat].actiu:
								escriu ^= 1
							else:
								nou_grup = 1
						
						if eventhandle.keyUp('PAGEDOWN') and teamsActius( self.joc.teams ) >= 1:
							element_seleccionat = seguentEquipActiu( self.joc.teams, element_seleccionat )
							self.so_sub.play() 
						
						if eventhandle.keyUp('PAGEUP') and teamsActius( self.joc.teams ) >= 1:
							element_seleccionat = anteriorEquipActiu( self.joc.teams, element_seleccionat )
							self.so_sub.play() 
						
						if eventhandle.keyUp('r') and teamsActius( self.joc.teams ) > 0:
							atzar = 30 + int( random.randint(0, 30) )
							estat = 1
					
					if eventhandle.keyUp('z'): 
						if self.joc.teams[element_seleccionat].actiu:
							self.joc.teams[element_seleccionat].punts += 1
					
					if eventhandle.keyUp('x'): 
						if self.joc.teams[element_seleccionat].actiu and self.joc.teams[element_seleccionat].punts > 0:
							self.joc.teams[element_seleccionat].punts -= 1
					
					if self.joc.teams[element_seleccionat].actiu:
						for num in range(1, 7):
							if eventhandle.keyUp(str(num), 'KP' + str(num)):
								self.joc.teams[element_seleccionat].canviaCategoria( str(num) )
					
					if eventhandle.isClick('primary') or eventhandle.keyUp('RETURN', 'SPACE', 'KP_ENTER'):

						if estat == 1:
							if not Global.MUSIC_MUTE:
								pygame.mixer.music.fadeout( 2000 )
							return element_seleccionat

						elif estat == 0:
							if self.joc.teams[element_seleccionat].actiu and eventhandle.keyUp('SPACE') :
								atzar = 30 + int( random.randint(0, 30) )
								estat = 1
							else:
								if self.joc.teams[element_seleccionat].actiu: escriu ^= 1
								else: nou_grup = 1
						else:
							if fesPregunta( self.joc.screen , valorText( HOS_NEW_GAME ), (valorText( HOS_YES ), valorText( HOS_NO ))) == 0:
								estat = 0
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
						estat = replaceModes[ estat ]

					if eventhandle.keyUp('e'):
						self.so_ok.play()
						visca = Visca( self.joc )
						resultat = visca.juguem( self.joc, self.joc.teams[element_seleccionat].nom )
						mostrada_victoria = True
						loadSound( 'score.ogg', volume = 0.6, music = 1).play( -1 )
					
					if eventhandle.keyUp('l'): 
						Global.LOCKED_MODE = (not Global.LOCKED_MODE)

					if eventhandle.keyUp('k', 'F3', 'F5'):
						selcat = SelCat( self.joc )
						selcat.juguem( estat )

			if nou_grup == 1:
				self.so_sub2.play()
				nou_grup = 0
				self.joc.teams[element_seleccionat].actiu ^= 1
				if self.joc.teams[element_seleccionat].actiu and self.joc.teams[element_seleccionat].nom == "": escriu ^= 1

			if atzar != 0 and teamsActius( self.joc.teams ) >= 2:
				element_seleccionat = seguentEquipActiu( self.joc.teams, element_seleccionat )
				atzar -= 1
				self.so_sub.play()
			else:
				atzar = 0
		
			# Animem el fons
			ypos += 1
			ypos %= Global.screen_y

			# Pintem el fons animat
			mou_fons += 8
			for num in range(0, 768):
				self.joc.screen.blit( self.fons, (cos((float(mou_fons +num)) / 100.0) * 20, num), (0, (ypos + num) % 768, 1024, 1) )

			self.joc.screen.blit( self.mascara_de_fons, (0, 0) )

			# pintem les puntuacions
			for num in range(0, 6):
				ycaixa = (int(num / 2) * 200) + 135
				xcaixa = 75 if ((num % 2) == 0) else 515

				if element_seleccionat == num:
					for compta in range( 0, self.seleccio_score.get_height() ):
						desp = 0 if not estat else ( cos( frate.segons() * 10.0 + (float(compta)/10.0) ) * 2.0 )
						self.joc.screen.blit( self.seleccio_score, (xcaixa - 58 + desp, ycaixa - 36 + compta), (0,compta, self.seleccio_score.get_width(),1) )


				
				if self.joc.teams[num].actiu:
	
					self.joc.screen.blit( self.element_score, (xcaixa, ycaixa ) )
					self.joc.screen.blit( self.figureta[self.joc.teams[num].figureta], (xcaixa + 15, ycaixa  ) )

					if self.joc.teams[num].sfc_nom:
						self.joc.screen.blit( self.joc.teams[num].sfc_nom, (xcaixa + 25 , ycaixa + 125 ) )
					ampletext = self.joc.teams[num].sfc_nom.get_width() if self.joc.teams[num].sfc_nom else 0
					if escriu and num == element_seleccionat:
						if (int(time.time() * 4) % 2) == 0: 
							self.joc.screen.blit( self.sfc_cursor, (xcaixa + 25 + ampletext, ycaixa + 125 )) 

					color = (128,0,0) if (maxPunts( self.joc.teams) > self.joc.teams[num].punts ) else (0,128,0)
					pinta = render_text( str(self.joc.teams[num].punts).zfill(2), color, 150, 1)
					self.joc.screen.blit( pinta, (xcaixa + 200, ycaixa - 15) )

					if mostra_estad:
						for cat in range(0,6):
							self.joc.screen.blit( self.barra_pos( self.joc.teams[num].preguntes_tot[cat], self.joc.teams[num].preguntes_ok[cat],  colorsCategories()[cat], 50, 14 ), (xcaixa + 140, ycaixa + 21 + cat * 16) )

			if mostra_ajuda: self.joc.screen.blit( self.help_overlay, (0,0))
			if mostra_credits: self.joc.screen.blit( self.joc.sfc_credits, (0,0))

			if Global.LOCKED_MODE: self.joc.screen.blit( self.sfc_llum, (0, 0) )
			
			self.help_on_screen.draw( self.joc.screen, (350, 740), HOS_SCORE_MODEW if escriu else estat)
			
			frate.next( self.joc.screen )
			
			# intercanviem els buffers de self.joc.screen
			pygame.display.flip()

		return 0
