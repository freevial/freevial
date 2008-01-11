# -*- coding: utf-8 -*-
 
#
# Freevial
# Questions Asker
#
# Copyright (C) 2007, 2008 The Freevial Team
#
# By Carles Oriol i Margarit <carles@kumbaworld.com>
# By Siegfried-Angel Gevatter Pujals <siggi.gevatter@gmail.com>
#
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
import time
import pygame
import copy
import math
from math import *

from common.freevialglob import *
from common.events import EventHandle
from questions import get_databases
from skiner import Skin


##################################################
#
# Empaquetat en una classe del preguntador
#

class Preguntador:

	###########################################
	#
	def __init__( self, joc ):
		
		self.joc = joc
		self.skin = Skin()
		self.skin.preguntadorCarrega( self.joc )	
		
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
		self.current_question = categoriespreguntes[self.categoria].question()
		self.num_asked_questions += 1
		
		self.selected = 0
		
		self.skin.preguntadorInicialitza_pregunta( self.current_question, self.num_asked_questions )	


	###########################################
	#
	# Bucle principal del programa
	#
	def juguem( self , selcat):
		
		self.help_on_screen.sec_timeout = 10

		self.frate = frameRate( Global.fps_limit )

		self.atzar( selcat )

		if not Global.SOUND_MUTE: pygame.time.wait( 2500 )
		loadSound('preguntador.ogg', volume = 0.4, music = 1).play(1)
		
		mostra_ajuda = mostra_credits = 0

		self.joc.screen.fill( (0,0,0,0) )

		# remaining seconds until end of answer time
		self.segons = 61


		if (self.joc.teams[self.joc.current_team].figureta & bitCategoria( selcat )) == 0:
			self.skin.preguntadorCarregaFiguretes( self.joc, selcat )

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
					screenshot(self.joc.screen)
				
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
						self.skin.so_sub_play()
					
					if eventhandle.keyUp('b', 'o'):	
						if eventhandle.isKey('b'): acaba = 1
						self.selected = 2
						self.skin.so_sub_play()
					
					if eventhandle.keyUp('c', 'p'):	
						if eventhandle.isKey('c'): acaba = 1
						self.selected = 3
						self.skin.so_sub_play()
					
					if eventhandle.keyUp('DOWN', 'TAB'): 
						self.selected += 1
						if self.selected == 4:
							self.selected = 1
						self.skin.so_sub_play()
					
					if eventhandle.keyUp(event, 'UP'): 
						self.selected -= 1
						if self.selected <= 0:
							self.selected = 3	
						self.skin.so_sub_play()
				
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
						self.skin.so_ok_play()
					else:
						self.skin.so_nook_play()
					
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
			
 			self.skin.preguntadorPinta( self.joc, self.categoria, self.selected, mostra_comentaris )
 			
 			self.help_on_screen.draw( self.joc.screen, (350, 740), HOS_PREGUNTADOR_END if self.show_answers else HOS_PREGUNTADOR_RUN )
			
			if mostra_ajuda: self.joc.screen.blit( self.help_overlay, (0,0))
			if mostra_credits: self.joc.screen.blit( self.joc.sfc_credits, (0,0))
			
			self.frate.next( self.joc.screen )
			
			#intercanviem els buffers de self.joc.screen
			pygame.display.flip()
			
		return 0
