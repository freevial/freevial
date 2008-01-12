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
		
		self.help_overlay = createHelpScreen( 'score' )

		self.help_on_screen = helpOnScreen( HOS_SCORE_MODE0 )
		self.skin_maxim_equips = self.skin.configGetInt( 'game', 'max_teams' )
		
		self.score_color_text_red = self.skin.configGetInt( 'score', 'color_text_red')
		self.score_color_text_green = self.skin.configGetInt( 'score', 'color_text_green')
		self.score_color_text_blue = self.skin.configGetInt( 'score', 'color_text_blue')
		self.score_color_text = (self.score_color_text_red, self.score_color_text_green, self.score_color_text_blue)
		self.score_mida_text = self.skin.configGetInt( 'score', 'mida_text')
		
		self.score_fons = self.skin.configGet( 'score', 'background')
		self.score_mascara_de_fons = self.skin.configGet( 'score', 'background_mask')
		self.score_element = self.skin.configGet( 'score', 'element')
		self.score_element_sel = self.skin.configGet( 'score', 'sel_element')
		self.score_element_sobre = self.skin.configGet( 'score', 'element_sobre')
		self.score_element_sel_offsetx = self.skin.configGetInt( 'score', 'sel_element_offsetx')
		self.score_element_sel_offsety = self.skin.configGetInt( 'score', 'sel_element_offsety')
		self.score_teams_offsetx = self.skin.configGetInt( 'score', 'teams_offsetx')
		self.score_teams_offsety = self.skin.configGetInt( 'score', 'teams_offsety')
		self.score_resultat_visible = self.skin.configGet( 'score', 'resultat_visible')
		self.score_figureta_visible = self.skin.configGet( 'score', 'figureta_visible') 
		self.score_figureta_mode = self.skin.configGet( 'score', 'figureta_mode') # 0 - del 0 al 63 combinacions 1 - del 0 al 5 figures individuals
		self.score_figureta_mascara = self.skin.configGet( 'score', 'figureta_mask')
		
		self.score_figureta_offsetx = self.skin.configGetInt( 'score', 'figureta_offsetx')
		self.score_figureta_offsety = self.skin.configGetInt( 'score', 'figureta_offsety')
		
		self.score_figureta_individual_pos = [[self.skin.configGetInt( 'score', 'figureta_individual_pos_0_X'),self.skin.configGetInt( 'score', 'figureta_individual_pos_0_Y')], [self.skin.configGetInt( 'score', 'figureta_individual_pos_1_X'),self.skin.configGetInt( 'score', 'figureta_individual_pos_1_Y')], [self.skin.configGetInt( 'score', 'figureta_individual_pos_2_X'),self.skin.configGetInt( 'score', 'figureta_individual_pos_2_Y')], [self.skin.configGetInt( 'score', 'figureta_individual_pos_3_X'),self.skin.configGetInt( 'score', 'figureta_individual_pos_3_Y')], [self.skin.configGetInt( 'score', 'figureta_individual_pos_4_X'),self.skin.configGetInt( 'score', 'figureta_individual_pos_4_Y')], [self.skin.configGetInt( 'score', 'figureta_individual_pos_5_X'),self.skin.configGetInt( 'score', 'figureta_individual_pos_5_Y')] ]
		
		self.score_figureta_show_hide = self.skin.configGet( 'score', 'figureta_show_hide') # 0 - Es mostren les parts aconseguides, 1 - S'amaguen les parts aconseguides
		
		self.score_so_sub = self.skin.configGet( 'score', 'sub_sound')
		self.score_so_sub_vol = self.skin.configGet( 'score', 'sub_sound_vol')
		self.score_so_sub2 = self.skin.configGet( 'score', 'sub_sound2')
		self.score_so_sub2_vol = self.skin.configGet( 'score', 'sub_sound2_vol')
		
		self.score_ok = self.skin.configGet( 'score', 'ok')
		self.score_ok_vol = self.skin.configGet( 'score', 'ok_vol')
		
		self.score_locked = self.skin.configGet( 'score', 'locked')
		self.score_locked_pos = (self.skin.configGetInt( 'score', 'locked_pos_X'),self.skin.configGetInt( 'score', 'locked_pos_Y'))
		
		self.score_so_de_fons = self.skin.configGet( 'score', 'background_sound')
		self.score_so_de_fons_vol = self.skin.configGet( 'score', 'background_sound_vol')

		self.score_desplaca_el_fons = self.skin.configGet( 'score', 'move_background') # True o False = no hi ha scroll vertical
		self.score_ones_al_fons = self.skin.configGet( 'score', 'background_waves') # True o False = quiet
		
		self.score_caixes = [self.skin.configGetInt( 'score', 'boxes_0_X'),self.skin.configGetInt( 'score', 'boxes_0_Y')], [self.skin.configGetInt( 'score', 'boxes_1_X'),self.skin.configGetInt( 'score', 'boxes_1_Y')], [self.skin.configGetInt( 'score', 'boxes_2_X'),self.skin.configGetInt( 'score', 'boxes_2_Y')], [self.skin.configGetInt( 'score', 'boxes_3_X'),self.skin.configGetInt( 'score', 'boxes_3_Y')], [self.skin.configGetInt( 'score', 'boxes_4_X'),self.skin.configGetInt( 'score', 'boxes_4_Y')], [self.skin.configGetInt( 'score', 'boxes_5_X'),self.skin.configGetInt( 'score', 'boxes_5_Y')]
		
		#------------------------------------------
		
		self.ypos = 0
		self.mou_fons = 0
		#-----------------------------------------------
		
		
		self.figureta = self.skin.LoadImageRange( "score", "figureta_mask", 64, 2)		
	
		self.mascara_de_fons = self.skin.LoadImage( "score", 'background_mask' )
		self.fons = self.skin.LoadImage( "score", 'background' )
		self.element_score = self.skin.LoadImage( "score", 'element' )
		self.seleccio_score = self.skin.LoadImage( "score", 'sel_element' )
		self.so_sub = self.skin.LoadSound( "score", 'sub_sound', 'sub_sound_vol' )
		self.so_sub2 = self.skin.LoadSound( "score", 'sub_sound2', 'sub_sound2_vol' )
		self.so_ok = self.skin.LoadSound( "score", 'ok', 'ok_vol' )
		self.sfc_llum = self.skin.LoadImage( "score", 'locked' )
		
		self.sfc_cursor = render_text( "_", (self.score_color_text), self.score_mida_text, 1)
		
	
	
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
		
		# Modes: 0 (choosing teams), 1 (playing),  2 (game ended)
		mode = 1
		
		if nou_grup: mode = 0
		if teamsGuanyador( self.joc.teams ) != -1: 
			mode = 2
			mostra_estad = 1
			element_seleccionat = teamsGuanyador( self.joc.teams )
			self.so_ok.play()
		else:
			self.skin.LoadSound( "score", 'background_sound', 'background_sound_vol', 1 ).play( -1 )
		
		surten = 0
		mostrada_victoria = False
		
		self.help_on_screen.activitat()
		
		while 1:
			
			if mode == 2:
				if frate.segons() < 4.1 and int(frate.segons()) > surten:
					surten = int( frate.segons() )
					self.scoreSoOk()
				if frate.segons() > 4.1 and not mostrada_victoria:
					visca = Visca( self.joc )
					resultat = visca.juguem( self.joc, self.joc.teams[teamsGuanyador( self.joc.teams )].nom )
					mostrada_victoria = True
					self.skin.LoadSound( self.score_so_de_fons, self.score_so_de_fons_vol, 'score.ogg', 0.6, music = 1).play( -1 )
			
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
							sfc = render_text( newname, (self.score_color_text), self.score_mida_text, 1)
							
							
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
						self.so_ok.play()
						visca = Visca( self.joc )
						resultat = visca.juguem( self.joc, self.joc.teams[element_seleccionat].nom )
						mostrada_victoria = True
						self.skin.LoadSound( self.score_so_de_fons, self.score_so_de_fons_vol, 'score.ogg', 0.6, music = 1).play( -1 )
					
					if eventhandle.keyUp('l'): 
						Global.LOCKED_MODE = (not Global.LOCKED_MODE)

					if eventhandle.keyUp('k', 'F3', 'F5') and mode == 0:
						selcat = SelCat( self.joc )
						selcat.juguem( mode )

			if nou_grup == 1:
				self.so_sub.play()
				nou_grup = 0
				self.joc.teams[element_seleccionat].actiu ^= 1
				if self.joc.teams[element_seleccionat].actiu and self.joc.teams[element_seleccionat].nom == "": escriu ^= 1

			if atzar != 0 and teamsActius( self.joc.teams ) >= 2:
				element_seleccionat = seguentEquipActiu( self.joc.teams, element_seleccionat )
				atzar -= 1
				self.so_sub2.play()
			else:
				atzar = 0
			
			if self.score_desplaca_el_fons != "False":
				# Animem el fons
				self.ypos += 1
				self.ypos %= Global.screen_y
			
			xpinta = 0
			
			if self.score_ones_al_fons:
				self.mou_fons += 8
				

			# Pintem el fons animat
			for num in range(0, 768):
				
				if self.score_ones_al_fons:
					xpinta = cos((float(self.mou_fons +num)) / 100.0) * 20
			
				self.joc.screen.blit( self.fons, (xpinta, num), (0, (self.ypos + num) % 768, 1024, 1) )
			
			self.joc.screen.blit( self.mascara_de_fons, (0, 0) )
			# pintem les puntuacions
			for num in range(0, self.skin_maxim_equips):
				ycaixa = self.score_caixes[num][1]
				xcaixa = self.score_caixes[num][0]

				if element_seleccionat == num and self.score_element_sobre != "True":
					for compta in range( 0, self.seleccio_score.get_height() ):
						desp = 0 if not mode else ( cos( frate.segons() * 10.0 + (float(compta)/10.0) ) * 2.0 )
						self.joc.screen.blit( self.seleccio_score, (xcaixa + self.score_element_sel_offsetx + desp, ycaixa + self.score_element_sel_offsety + compta), (0,compta, self.seleccio_score.get_width(),1) )

				
				if self.joc.teams[num].actiu:
					
					self.joc.screen.blit( self.element_score, (xcaixa, ycaixa ) )
					
					if self.score_figureta_visible == 'True':
						self.joc.screen.blit( self.figureta[self.joc.teams[num].figureta], (xcaixa + self.score_figureta_offsetx, ycaixa + self.score_figureta_offsety ) )

					if self.joc.teams[num].sfc_nom:
						self.joc.screen.blit( self.joc.teams[num].sfc_nom, (xcaixa + self.score_teams_offsetx , ycaixa + self.score_teams_offsety ) )
					ampletext = self.joc.teams[num].sfc_nom.get_width() if self.joc.teams[num].sfc_nom else 0
					if escriu and num == element_seleccionat:
						if (int(time.time() * 4) % 2) == 0: 
							self.joc.screen.blit( self.sfc_cursor, (xcaixa + 25 + ampletext, ycaixa + 125 )) 
							
					color = (128,0,0) if (maxPunts(self.joc.teams) > self.joc.teams[num].punts ) else (0,128,0)
					pinta = render_text( str(self.joc.teams[num].punts).zfill(2), color, 150, 1)
					if self.score_resultat_visible == 'True':
						self.joc.screen.blit( pinta, (xcaixa + 200, ycaixa - 15) )

					if mostra_estad:
						for cat in range(0,6):
							self.joc.screen.blit( self.barra_pos( self.joc.teams[num].preguntes_tot[cat], self.joc.teams[num].preguntes_ok[cat],  colorsCategories()[cat], 50, 14 ), (xcaixa + 140, ycaixa + 21 + cat * 16) )
				
				
				if element_seleccionat == num and self.score_element_sobre == "True":
					for compta in range( 0, self.seleccio_score.get_height() ):
						desp = 0 if not escriu else ( cos( frate.segons() * 10.0 + (float(compta)/10.0) ) * 2.0 )
						self.joc.screen.blit( self.seleccio_score, (xcaixa + self.score_element_sel_offsetx + desp, ycaixa + self.score_element_sel_offsety + compta), (0,compta, self.seleccio_score.get_width(),1) )
			
			
			if Global.LOCKED_MODE: 
				self.joc.screen.blit( self.sfc_llum, (0, 0) )
			
			if mostra_ajuda: self.joc.screen.blit( self.help_overlay, (0,0))
			if mostra_credits: self.joc.screen.blit( self.joc.sfc_credits, (0,0))
			
			self.help_on_screen.draw( self.joc.screen, (350, 740), HOS_SCORE_MODEW if escriu else mode)
			
			frate.next( self.joc.screen )
			
			# Exchange self.joc.screen buffers
			pygame.display.flip()

		return 0
