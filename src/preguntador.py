# -*- coding: utf-8 -*-
 
#
# Freevial
# Questions Asker
#
# Copyright (C) 2007, 2008 The Freevial Team
#
# By Carles Oriol i Margarit <carles@kumbaworld.com>
# By Siegfried-Angel Gevatter Pujals <siggi.gevatter@gmail.com>
# By Nil Oriol <nil@kumbaworld.com>
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
import time
import pygame
from math import *

from common.freevialglob import *
from common.events import EventHandle
from questions import get_databases
from skiner import Skin


class Preguntador:

	def __init__( self, game ):
		
		self.game = game
		self.skin = Skin('preguntador')
		
		self.color_de_fons_red = self.skin.configGetInt('color_de_fons_red')
		self.color_de_fons_green = self.skin.configGetInt('color_de_fons_green')
		self.color_de_fons_blue = self.skin.configGetInt('color_de_fons_blue')
		self.color_de_text_red = self.skin.configGetInt('color_de_text_red')
		self.color_de_text_green = self.skin.configGetInt('color_de_text_green')
		self.color_de_text_blue = self.skin.configGetInt('color_de_text_blue')
		self.color_de_fons = (self.color_de_fons_red, self.color_de_fons_green, self.color_de_fons_blue)
		self.color_de_text = (self.color_de_text_red, self.color_de_text_green, self.color_de_text_blue)
		
		self.mida_font = self.skin.configGetInt('mida_font')
		self.altlinies = self.mida_font + 5
		self.postextx= self.skin.configGetInt('postextx')
		self.postexty = self.skin.configGetInt('postexty')
		self.mascara_de_fons = self.skin.configGet('mascara_de_fons')
		self.retalla_sel = self.skin.configGet('retalla_sel')
		
		self.solucio_ok = self.skin.configGet('solucio_ok')
		self.solucio_nook = self.skin.configGet('solucio_nook')
		
		self.lletraA = self.skin.configGet('lletraA')
		self.lletraB = self.skin.configGet('lletraB')
		self.lletraC = self.skin.configGet('lletraC')
		self.lletraAoff = self.skin.configGet('lletraAoff')
		self.lletraBoff = self.skin.configGet('lletraBoff')
		self.lletraCoff = self.skin.configGet('lletraCoff')
		
		self.itr1 = self.skin.configGet('itr1')
		self.itr2 = self.skin.configGet('itr2')
		
		self.so_ticking2 = self.skin.configGet( 'so_ticking2')
		self.so_ticking2_vol = self.skin.configGet( 'so_ticking2_vol')
		self.mostra_punt_de_categoria = self.skin.configGetBool( 'mostra_punt_de_categoria')
		self.so_drum2 = self.skin.configGet( 'so_drum2')
		self.so_drum2_vol = self.skin.configGet( 'so_drum2_vol')
		
		self.so_sub = self.skin.configGet( 'so_sub')
		self.so_sub_vol = self.skin.configGet( 'so_sub_vol')
		
		self.so_ok = self.skin.configGet( 'so_ok')
		self.so_ok_vol = self.skin.configGet( 'so_ok_vol')
		
		self.so_nook = self.skin.configGet( 'so_nook')
		self.so_nook_vol = self.skin.configGet( 'so_nook_vol')
		
		self.mostranpregunta = self.skin.configGet( 'mostranpregunta')
		
		self.preguntadorYpos = 190
		self.ypos = 0
		self.mou_fons = 0
		
		self.color_de_fons = self.color_de_fons
		self.color_de_text = self.color_de_text
		
		self.mida_font = self.mida_font
		self.altlinies = self.altlinies
		self.postextx = self.postextx
		self.postexty = self.postexty
		
		self.mascara_de_fons = self.skin.LoadImage( 'mascara_de_fons' )
		self.retalla_sel = self.skin.LoadImage( 'retalla_sel' )
		
		self.solucio_ok = self.skin.LoadImage( 'solucio_ok' )
		self.solucio_nook = self.skin.LoadImage( 'solucio_nook' )
		
		self.fons = range(0, 6)
		for num in range(0, 6):
			self.fons[num] = loadImage(get_databases( num ).image)
			sfcmask = loadImage( 'filtre_c' + str(num+1) + '.png' )
			self.fons[num].blit( sfcmask, (0,0))
		
		self.mascara = pygame.Surface((655, 150), pygame.SRCALPHA, 32)
		
		self.lletres = [
							[ self.skin.LoadImage( 'lletraA'), self.skin.LoadImage( 'lletraAoff') ], 
							[ self.skin.LoadImage( 'lletraB'), self.skin.LoadImage( 'lletraBoff') ], 				
							[ self.skin.LoadImage( 'lletraC'), self.skin.LoadImage( 'lletraCoff') ],
						]
		
		self.info = [ self.skin.LoadImage( 'itr1'), self.skin.LoadImage( 'itr2') ]	
		
		self.so_ticking2 = self.skin.LoadSound( 'so_ticking2', 'so_ticking2_vol')
		self.so_drum2 = self.skin.LoadSound( 'so_drum2', 'so_drum2_vol')
		self.so_sub = self.skin.LoadSound( 'so_sub', 'so_sub_vol')
		self.so_ok = self.skin.LoadSound( 'so_ok', 'so_ok_vol')
		self.so_nook = self.skin.LoadSound( 'so_nook', 'so_nook_vol')
		
		self.nom_equip_sfc = self.skin.render_text( game.teams[game.current_team].nom, (64,64,64), 30, 1 )	
		self.nom_equip_sfc = pygame.transform.rotate ( self.nom_equip_sfc, 90 )
		self.nom_equip_sfc.set_alpha( 64 )

		self.compos = 768
		
#		self.color_de_fons = (0, 0, 0)
#		self.color_de_text = (255, 255, 255)
		
#		self.mida_font = 40
#		self.altlinies = self.mida_font + 5
#		self.postextx= 80
#		self.postexty = 40
		
		self.categoria = None
		self.current_question = None
		self.num_asked_questions = 0
		self.show_answers = 0
		self.selected = 0
		
		# Load images
#		self.fons = range(0, 6)
#		for num in range(0, 6):
#			self.fons[num] = loadImage( get_databases(num).image )
#			sfcmask = loadImage( 'filtre_c' + str(num+1) + '.png' )
#			self.fons[num].blit( sfcmask, (0,0))
		
#		self.mascara_de_fons = loadImage('mascara_de_fons.png')
#		self.retalla_sel = loadImage('retalla_sel.png')
		
#		self.solucio_ok = loadImage('ok.png')

#		self.solucio_nook = loadImage('nook.png')
		
#		self.mascara = pygame.Surface((655, 150), pygame.SRCALPHA, 32)
		
#		self.lletres = [
#								[ loadImage('lletraA.png'), loadImage('lletraA_off.png') ], 
#								[ loadImage('lletraB.png'), loadImage('lletraB_off.png') ], 				
#								[ loadImage('lletraC.png'), loadImage('lletraC_off.png') ],
#							]
		
#		self.info = [ loadImage('itr1.png'), loadImage('itr2.png') ]	
		

		# carreguem els arxius de so
#		self.so_ticking2 = loadSound('ticking2.ogg')
#		self.so_drum2 = loadSound('drum2.ogg')
#		self.so_sub = loadSound('sub.ogg', volume = 0.1)
#		self.so_ok = loadSound('cheer.ogg')
#		self.so_nook = loadSound('crboo.ogg')
		
		# mostra nombre de pregunta i autor?
#		self.mostranpregunta = 1
		
		self.help_overlay = createHelpScreen( 'preguntador' )
		
		self.help_on_screen = helpOnScreen( HOS_PREGUNTADOR_RUN )
		self.help_on_screen.sec_timeout = 10

	###########################################
	#
	# Funció per veure el nombre de linies que té una frase a mostrar
	# basant-nos en que el separador és el caracter #
	def numlinies( self, cadena ):
		
		return cadena.count('#')

	###########################################
	#
	# Cercador de preguntes a l'atzar
	# si la categoria és 0 no té en compte el valor
	def atzar( self, categoria ):
		
		self.categoria = categoria - 1
		self.current_question = get_databases(self.categoria).question()
		self.num_asked_questions += 1
		
		self.selected = 0
		self.initialize_question()
	
	###########################################
	#
	# Inicialitzador de nova pregunta
	#
	def initialize_question( self ):
		
		self.sfc_pregunta  = self.preguntadorPintatext( self.current_question['text'], 1024 - 175 )

		self.sfc_resposta = range(0, 3)
		for num in xrange(0, 3):
			self.sfc_resposta[ num ] = self.preguntadorPintatext( self.current_question[ 'opt' + str(num + 1) ], 1024 - 260 )

		self.sfc_npregunta = self.skin.render_text( str(self.num_asked_questions), (255,255,255), 100 )
		self.sfc_npregunta.set_alpha( 64 )

		self.sfc_apregunta = self.skin.render_text( str(self.current_question['author']), (255,255,255), 16 )
		self.sfc_apregunta.set_alpha( 64 )	

		self.temps_inici_pregunta = time.time()
		self.segons = 61
		self.so_drum2.play()
		self.so_drum2.stop()

		self.show_answers = 0

	###########################################
	#
	# Funció per pintar el text i les preguntes sobre una nova superficie
	# usant el color del text i el sobrejat
	def preguntadorPintatext( self, textapintar, maxample = 0 ):

		nalt = 0

		cadenes = textapintar.split('#')
		sfc_pregunta = range(0, len(cadenes) )
		sfc_shad = range(0, len(cadenes) )

		nlinia = 0

		for cadena in cadenes:
			sfc_pregunta[nlinia] = self.skin.render_text( cadena if cadena != "" else " ", self.color_de_text, self.mida_font, 1, '', maxample - 2)
			sfc_shad[nlinia] = self.skin.render_text( cadena if cadena != "" else " ", self.color_de_fons, self.mida_font, 1, '', maxample - 2)
			nalt += sfc_pregunta[nlinia].get_height() + 2				     
			nlinia += 1
		
		sfc = pygame.Surface( ( 1024 if maxample == 0 else maxample, nalt ), pygame.SRCALPHA, 32 )

		nalt = 0
		nlinia = 0
		for cadena in cadenes:
			sfc.blit( sfc_shad[nlinia], (0 + 2, nalt + 2))
			sfc.blit( sfc_pregunta[nlinia], (0, nalt ))
			nalt += sfc_pregunta[nlinia].get_height() + 2
			nlinia += 1
			
		return sfc

	###########################################
	#
	# Bucle principal del programa
	#
	def juguem( self , selcat):
		
		self.help_on_screen.sec_timeout = 10

		self.frate = frameRate( Global.fps_limit )

		self.atzar( selcat )

		if not Global.SOUND_MUTE: pygame.time.wait( 2500 )
		self.skin.LoadSound( 'so_fons', 'so_fons_vol', 1).play(1)

		mostra_ajuda = mostra_credits = 0

		self.game.screen.fill( (0,0,0,0) )

		# remaining seconds until end of answer time
		self.segons = 61

		if (self.game.teams[self.game.current_team].figureta & bitCategoria( selcat )) == 0:
			self.skin.preguntadorCarregaFiguretes( self.game, selcat )

		mostra_comentaris = False
		sfc_comentaris = None

		self.help_on_screen.activitat( )
	
		while 1:
			
			acaba = 0
			
			# Iterador d'events
			for event in pygame.event.get():
				
				eventhandle = EventHandle(event)
				
				self.help_on_screen.activitat(event)
				
				if event.type == pygame.JOYBUTTONDOWN:
					translateJoystickEvent(event)
				
				if eventhandle.isQuit():
					sys.exit()
				
				if eventhandle.keyDown('PRINT'):
					screenshot(self.game.screen)
				
				if eventhandle.keyUp('f', 'F11'):
					pygame.display.toggle_fullscreen()
				
				if eventhandle.keyUp('q', 'ESCAPE') and not Global.LOCKED_MODE:
					if not mostra_ajuda and not mostra_credits:
						if not (Global.SOUND_MUTE or Global.MUSIC_MUTE):
							pygame.mixer.fadeout(500)
						if self.show_answers == 0:
							self.show_answers = 1
							self.selected = 0
						acaba = 1
					else:
						mostra_ajuda = mostra_credits = 0
				
				if eventhandle.keyUp('F1', 'h'):
					mostra_ajuda ^= 1
					mostra_credits = 0

				if eventhandle.keyUp('F2'):
					mostra_ajuda = 0
					mostra_credits ^= 1
				
				if self.show_answers == 0:
					if eventhandle.keyUp('a', 'i'):
						if eventhandle.isKey('a'): acaba = 1	
						self.selected = 1
						self.so_sub.play()
					
					if eventhandle.keyUp('b', 'o'):	
						if eventhandle.isKey('b'): acaba = 1
						self.selected = 2
						self.so_sub.play()
					
					if eventhandle.keyUp('c', 'p'):	
						if eventhandle.isKey('c'): acaba = 1
						self.selected = 3
						self.so_sub.play()
					
					if eventhandle.keyUp('DOWN', 'TAB'): 
						self.selected += 1
						if self.selected == 4:
							self.selected = 1
						self.so_sub.play()
					
					if eventhandle.keyUp(event, 'UP'): 
						self.selected -= 1
						if self.selected <= 0:
							self.selected = 3	
						self.so_sub.play()
				
				if eventhandle.keyUp('z'):	
					self.mostranpregunta ^= 1
				
				for num in range(1, 7):
					if eventhandle.keyUp(str(num), 'KP' + str(num)):
						self.atzar( num )
				
				if eventhandle.isRelease('primary') or eventhandle.keyUp('RETURN', 'SPACE', 'KP_ENTER'):
					if self.selected != 0:
						acaba = 1
				
				if eventhandle.keyUp('F3') and self.show_answers == 3 and len(self.current_question['comment']) > 5:	
					mostra_comentaris ^= 1

			# Si hem premut a return o s'ha acabat el temps finalitzem
			if acaba == 1 or self.segons <= 0:
				if not Global.MUSIC_MUTE:
					pygame.mixer.music.fadeout(2500)
				self.help_on_screen.sec_timeout = 3
				if self.show_answers == 0:
					self.show_answers = 3
					if self.current_question['answer'] == self.selected:
						self.so_ok.play()
					else:
						self.so_nook.play()
					
					notes = self.current_question['comment'].split('#') if self.current_question['comment'] != "" else "."
					sfc_comentaris = createTextSurface( notes, (128,255,255), 25 )
				elif acaba == 1:
					if not Global.LOCKED_MODE or mostra_comentaris == True or len( self.current_question['comment'] ) <= 5:
						if not (Global.MUSIC_MUTE or Global.SOUND_MUTE):
							pygame.mixer.fadeout(2500)
						return self.categoria if ( self.current_question['answer'] == self.selected) else 0
					else:
						compos = 768
						mostra_comentaris = True;

 			# Animem el fons
			self.ypos += 2
			if self.ypos >= Global.screen_y: self.ypos %= Global.screen_y
				
			# Pintem el fons animat
			self.game.screen.blit( self.fons[self.categoria - 1], (0,0), (0, (768 - self.ypos), Global.screen_x, min(200, self.ypos)))
			if self.ypos < 200:
				self.game.screen.blit( self.fons[self.categoria - 1], (0, min( 200, self.ypos)), (0, 0, Global.screen_x, 200 - min( 200, self.ypos)))
			
			# i el sombrejem per fer l'efecte de desapariió
			# també pintem el logotip del peu a l'hora que esborrem el fons de self.game.screen
			self.game.screen.blit( self.mascara_de_fons, (0, 0) )
			
			# preparem el sobrejat de l'opció seleccionada
			ympos = self.ypos + 300
			ympos %= 768
			self.mascara.blit( self.fons[ self.categoria - 1], (0,0), (0, (768 - ympos), Global.screen_x, min( 200, ympos )))
			
			if ympos < 200: 
				self.mascara.blit( self.fons[ self.categoria - 1], (0, min( 200, ympos)), (0, 0, Global.screen_x, 200 - min( 200, ympos)))
			
			# i el mesclem amb la mascara per donar-li forma
			self.mascara.blit( self.retalla_sel, (0,0))
				
			# pintem l'ombrejat on correspongui	
			if self.selected == 1: self.game.screen.blit( self.mascara, ( self.postextx, 260))
			if self.selected == 2: self.game.screen.blit( self.mascara, ( self.postextx, 260+150))
			if self.selected == 3: self.game.screen.blit( self.mascara, ( self.postextx, 260+300))
			
			# mostrem l'autor i el nombre de pregunta
			if self.mostranpregunta != 'False' :
				self.game.screen.blit( self.sfc_npregunta, (1024 - ( self.sfc_npregunta.get_width() + 25), 0) )
				self.game.screen.blit( self.sfc_apregunta, (1024 - ( self.sfc_apregunta.get_width() + 25), 94) )
				
			# mostrem la pregunta
			self.game.screen.blit( self.sfc_pregunta, (self.postextx, self.postexty) )	
				
			# i les solucions			
			linia_act = 270
				
			for num in range(0, 3):
				self.game.screen.blit( self.lletres[num][(self.selected != num + 1)], ( self.postextx, linia_act + (150 * num)) )
				self.game.screen.blit( self.sfc_resposta[ num ], (self.postextx + 180 , linia_act + 20 + (150 * num)) )		
				
			# comprovem l'estat del temps
			segons_act = 60 - int( (time.time() - self.temps_inici_pregunta) )
			if segons_act < 0: 
				segons_act = 0
				self.segons = 0
				
			# si no estem en l'estat de mostrar les soŀlucions mostrem el temps restant
			if self.show_answers == 0:
				if self.segons != segons_act:
					# el segon actual ha canviat
					self.segons = segons_act 
					self.pinta_segons = self.skin.render_text( str( self.segons ).zfill(2), (255,255,255), 600)
					# s'acaba el temps indiquem'ho amb so
					if self.segons < 20:
						self.so_ticking2.set_volume( (20 - float( self.segons )) / 20.0  ) 
						self.so_ticking2.play()
				
					# pintem els segons que queden, posant-los cada cop menys transparents
				self.pinta_segons.set_alpha( (60 - segons_act) )
				self.game.screen.blit( self.pinta_segons, ( 300 , 150) )
			
			# Pintem les solucions
			linia_act = 270
			posn = 700
			posnook = 700 + cos(time.time()) * 25
			posok = 700 + cos(time.time() * 2) * 50
			
			if self.show_answers > 0:
					
				for num in range (0, 3):
					if self.current_question['answer'] == (num + 1):
						if self.selected != (num + 1):	
							self.game.screen.blit( self.solucio_ok, (posnook, linia_act + (150 * num)) )
						else:
							self.game.screen.blit( self.solucio_ok, (posok, linia_act + (150 * num)) )
						
					else:
						if self.selected == (num + 1):
							self.game.screen.blit( self.solucio_nook, (posnook, linia_act + (150 * num)) )
					
				if len( self.current_question['comment'] ) > 5:
					self.game.screen.blit( self.info[0] if (int(time.time() * 3) % 3) == 0 else self.info[1], (self.postextx, 150) )
				
			if self.mostra_punt_de_categoria:
				if self.match_point:
					t = time.time()
					for compta in range( 0, 16 ) :
						self.game.screen.blit( self.figureta_no if (int(time.time() * 2) % 2) == 0 else self.figureta_si, (500 + cos(t+(float(compta)/15)) * 400, 110 + sin((t + (float(compta)/10)) * 2) * 25) )
				else:
					self.game.screen.blit( self.figureta_no if (int(time.time() * 2) % 2) == 0 else self.figureta_si, (880, 130) )

			self.game.screen.blit( self.nom_equip_sfc, (20, 748 - self.nom_equip_sfc.get_height()))

			if mostra_comentaris and sfc_comentaris is not None:
				if self.compos > 0: self.compos -= 100
				self.game.screen.blit( sfc_comentaris, (0, self.compos))
			elif sfc_comentaris is not None:
				if self.compos < 768: 
					self.compos += 100
					self.game.screen.blit( sfc_comentaris, (0, self.compos))
 			
 			self.help_on_screen.draw( self.game.screen, (350, 740), HOS_PREGUNTADOR_END if self.show_answers else HOS_PREGUNTADOR_RUN )
			
			if mostra_ajuda: self.game.screen.blit( self.help_overlay, (0,0))
			if mostra_credits: self.game.screen.blit( self.game.sfc_credits, (0,0))
			
			self.frate.next( self.game.screen )
			
			# Exchange self.game.screen buffers
			pygame.display.flip()
		
		pygame.mixer.music.stop()

		return 0
