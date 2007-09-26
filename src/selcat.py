# -*- coding: utf-8 -*-
 
#
# Freevial
# Game categories selector
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

from common.freevialglob import *
from common.events import EventHandle
from preguntes import *

##################################################
#
# Empaquetat en una classe del selector de categories
#

def FindList ( llista, element ):

	for compta in range( 0, len(llista) ):
		if llista[compta] == element:
			return compta

	return -1

class SelCat:

	###########################################
	#

	def __init__( self, joc ):
		
		self.joc = joc
		
		self.mascara_de_fons = loadImage('fons_score.png')
		self.fons = loadImage('score_fons.png')

		self.sel_quadres = loadImage('sel_quadres.png')
		self.sel_reflexos = loadImage('sel_reflexos.png')

		self.sel_fletxap = loadImage('sel_fletxap.png')
		self.sel_fletxab = loadImage('sel_fletxab.png')

		self.sel_quadre = loadImage('sel_quadre.png')
		self.sel_quadreok = loadImage('sel_quadreok.png')

		self.so_sub = loadSound('sub.ogg', volume = 0.1)
		self.so_sub2 = loadSound('sub2.ogg', volume = 0.4)

		self.help_overlay = createHelpScreen( 'score' )

		self.help_on_screen = helpOnScreen( HOS_SCORE_MODE0 )

		self.cp = get_categoriespreguntes()
		self.sfc_preguntes = range(0, len(self.cp))

		self.reinicia_cats()

		self.sfc_nombres = range(0,6)
		for compta in range(0, 6):
			self.sfc_nombres[compta] = render_text( str(compta+1), colorsCategories()[compta], 35, 1, '', 50 )

	def refa_cats( self ):
		for cat in range(0, 6):
			for compta in range(0, len( self.cp[cat].preguntes) ):
				self.cp[cat].preguntes[compta][0] = cat+1
			for compta in range(0, len( self.cp[cat].preguntes_backup) ):
				self.cp[cat].preguntes_backup[compta][0] = cat+1
	
	def reinicia_cats( self ):
		self.categories_seleccionades = [0,1,2,3,4,5];
	
		# colorsCategories():
		for compta in range(0, len(self.cp)):
			color = (128, 128, 128)
			if compta < 6:
				color = colorsCategories()[compta]
			self.sfc_preguntes[compta] = render_text( self.cp[compta].nom, color, 27, 1, '', 220 )

	def CanviaElements( self, aposar, atreure):

		self.so_sub2.play() 

		if aposar == atreure:
			return

		queda = self.cp[aposar]
		self.cp[aposar] = self.cp[atreure]
		self.cp[atreure] = queda

		self.darrera_info = -1
		self.reinicia_cats( )

	def PosaPrimer( self, seleccio ):

		self.so_sub2.play() 
		if seleccio == 0:
			return

		actual = self.cp[seleccio]
		self.cp.remove( actual )
		self.cp.insert( 0, actual )
		self.darrera_info = -1
		self.reinicia_cats( )

	###########################################
	#
	# Bucle principal del programa
	#
	def juguem( self, estat ):

		# estat 0 = edició, 1/2 = veure categories

		frate = frameRate( self.joc.Limit_FPS )
		
		self.joc.pantalla.fill( (0,0,0,0) )
		
		ypos = mou_fons = mostra_ajuda = mostra_credits = 0

		self.darrera_info = -1

		darrer_element_a_la_vista = 0

		primer_element_a_la_vista = 0

		self.help_on_screen.activitat()
			
		seleccio = 0

		nelements = len(self.cp) if estat == 0 else 6

		while 1:
				
			# Event iterator
			for event in pygame.event.get():

				eventhandle = EventHandle(event)
				
				if event.type == pygame.JOYBUTTONDOWN:
					translateJoystickEvent(event)
				
				if eventhandle.isQuit():
					sys.exit()
				
				if eventhandle.keyDown('PRINT'):
					screenshot(self.joc.pantalla)
				
				if eventhandle.keyUp('f', 'F11'):
					pygame.display.toggle_fullscreen()
				
				if eventhandle.keyUp('q', 'ESCAPE', 'KP_ENTER', 'F3', 'F5'):
					if estat == 0: self.refa_cats();
					return
				
				if eventhandle.keyUp('DOWN'):
					seleccio += 1
					seleccio %=  nelements
					self.so_sub.play() 
				
				if eventhandle.keyUp('UP'):
					seleccio -= 1
					seleccio %=  nelements 
					self.so_sub.play() 
				
				if eventhandle.keyUp('PRINT'):
					screenshot( self.joc.pantalla )
				
				if eventhandle.keyUp('F11', 'f'):
					pygame.display.toggle_fullscreen()

				if estat == 0:

					if eventhandle.keyUp('r'):
						random.shuffle( categoriespreguntes )
						self.reinicia_cats( )
						self.so_sub2.play()
						self.darrera_info = -1

					for num in range(0, 6):
						if eventhandle.keyUp(str(num + 1), 'KP' + str(num + 1)): 	
							self.CanviaElements( seleccio, num )
							seleccio = num

					if eventhandle.keyUp('RETURN'):										
						self.PosaPrimer( seleccio )

				else:
					if eventhandle.keyUp('RETURN'):			
						if estat == 0: self.refa_cats();							
						return
		
			# Animem el fons
			ypos += 1
			ypos %= self.joc.mida_pantalla_y

			# Pintem el fons animat
			mou_fons += 8
			for num in range(0, 768):
				self.joc.pantalla.blit( self.fons, (cos((float(mou_fons +num)) / 100.0) * 20, num), (0, (ypos + num) % 768, 1024, 1) )

			self.joc.pantalla.blit( self.mascara_de_fons, (0, 0) )
			self.joc.pantalla.blit( self.sel_quadres, (0, 0) )


			nelements = len(self.cp) if estat == 0 else 6

			posact= 220
			for compta in range(primer_element_a_la_vista, nelements):	
				if posact + self.sfc_preguntes[compta].get_height() > (768 -80)	:
					break
			
				if compta == seleccio:
					self.joc.pantalla.fill( (64,64,64), (100, posact, 300, self.sfc_preguntes[compta].get_height() +3 ) )

				if compta < 6 :
					self.joc.pantalla.blit( self.sfc_nombres[compta], (120, posact-3) )

				darrer_element_a_la_vista = compta
				self.joc.pantalla.blit( self.sfc_preguntes[compta], ( 160,posact ))	

				posact += self.sfc_preguntes[compta].get_height() + 20

			if( primer_element_a_la_vista > 0 ): 
				self.joc.pantalla.blit( self.sel_fletxap, ( 386,216 + 10 + cos(time.time() * 10) * 10))

			if( darrer_element_a_la_vista < nelements - 1):
				self.joc.pantalla.blit( self.sel_fletxab, ( 386, 651 - 10 - cos(time.time()*10) * 10 ))

			if( darrer_element_a_la_vista < seleccio): 	primer_element_a_la_vista += 1

			if( primer_element_a_la_vista > seleccio): 	primer_element_a_la_vista -= 1

						
			self.joc.pantalla.blit( self.sfc_preguntes[seleccio], ( 475, 220 ))	

			if( seleccio != self.darrera_info): 	
				self.sfc_text_info0 = render_text( self.cp[seleccio].autors, (255,255,255), 14, 1, '', 220 )
				self.sfc_text_info1 = render_text( self.cp[seleccio].descripcio, (255,255,255), 16, 1, '', 350 )
				self.sfc_text_info2 = render_text( self.cp[seleccio].jugadors, (255,255,255), 16, 1, '', 350 )
				self.sfc_text_info3 = render_text( u"N. Pregutes: " + str(len(self.cp[seleccio].preguntes_backup)), (255,255,255), 16, 1, '', 350 )
				self.sfc_text_info4 = render_text( u"Idioma: " + self.cp[compta].idioma, (255,255,255), 16, 1, '', 100 )
				self.sfc_text_info5 = render_text( u"Data creació: " + self.cp[compta].data_creacio , (255,255,255), 16, 1, '', 350 )
				self.sfc_text_info6 = render_text( u"Data darrera modificació: " + self.cp[seleccio].data_revisio, (255,255,255), 16, 1, '', 350 )

				self.sfc_cat = loadImage( self.cp[seleccio].nomimatge )
				if seleccio < 6:
					sfcmask = loadImage( 'filtre_c' + str(seleccio+1) + '.png' )
					self.sfc_cat.blit( sfcmask, (0,0))
				self.sfc_cat = pygame.transform.scale(self.sfc_cat, (184, 138) )

				self.darrera_info = seleccio
			
			self.joc.pantalla.blit( self.sfc_text_info0, ( 475, 305 ))	
			self.joc.pantalla.blit( self.sfc_text_info1, ( 490, 380 ))	
			self.joc.pantalla.blit( self.sfc_text_info2, ( 490, 495 ))	
			self.joc.pantalla.blit( self.sfc_text_info3, ( 490, 606 ))	
			self.joc.pantalla.blit( self.sfc_text_info4, ( 765, 606 ))	
			self.joc.pantalla.blit( self.sfc_text_info5, ( 490, 635 ))	
			self.joc.pantalla.blit( self.sfc_text_info6, ( 490, 655 ))	
	
			self.joc.pantalla.blit( self.sfc_cat, ( 697, 221 ))	
			
			if mostra_ajuda: self.joc.pantalla.blit( self.help_overlay, (0,0))
			if mostra_credits: self.joc.pantalla.blit( self.joc.sfc_credits, (0,0))
			
#			self.help_on_screen.draw( self.joc.pantalla, (350, 740), HOS_SCORE_MODEW if escriu else estat)
			
			self.joc.pantalla.blit( self.sel_reflexos, (0, 0) )

			frate.next( self.joc.pantalla )
			
			# intercanviem els buffers de self.joc.pantalla
			pygame.display.flip()

		return 0
