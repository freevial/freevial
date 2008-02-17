# -*- coding: utf-8 -*-
 
#
# Freevial
# Game categories selector
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

from common.freevialglob import *
from common.events import EventHandle
from questions import shuffle_databases, get_databases
from roda import Roda

def FindList( llista, element ):

	for compta in range( 0, len(llista) ):
		if llista[compta] == element:
			return compta

	return -1

class SelCat:

	def __init__( self, game ):
		
		self.game = game
		game.skin.set_domain( 'selcat' )
		
		self.mascara_de_fons =  game.skin.LoadImage('fons_score')
		self.fons = game.skin.LoadImage('score_fons')

		self.sel_quadres = game.skin.LoadImage('sel_quadres')
		self.sel_reflexos = game.skin.LoadImage('sel_reflexos')

		self.sel_fletxap = game.skin.LoadImage('sel_fletxap')
		self.sel_fletxab = game.skin.LoadImage('sel_fletxab')

		self.sel_quadre = game.skin.LoadImage('sel_quadre')
		self.sel_quadreok = game.skin.LoadImage('sel_quadreok')

		self.so_sub = game.skin.LoadSound( 'so_sub', 'so_sub_vol' )
		self.so_sub2 = game.skin.LoadSound( 'so_sub2', 'so_sub_vol' )

		self.selcat_color_text = game.skin.configGetRGB( 'color_text' )
		
		self.selcat_color_text_nosel = game.skin.configGetRGB( 'color_text_nosel' )

		self.help_overlay = createHelpScreen( 'score' )

		self.help_on_screen = helpOnScreen( HOS_SCORE_MODE0 )

		self.cp = get_databases()
		self.sfc_preguntes = range(0, len(self.cp))

		self.reinicia_cats()

		self.sfc_nombres = range(0,6)
		for compta in range(0, 6):
			self.sfc_nombres[compta] = render_text( str(compta+1), colorsCategories()[compta], 35, 1, '', 50 )

	def refa_cats( self ):
		for cat in range(0, 6):
			self.cp[cat].num = cat+1
	
	def reinicia_cats( self ):
		self.categories_seleccionades = [0,1,2,3,4,5];
	
		for compta in range(0, len(self.cp)):
			color = self.selcat_color_text_nosel
			if compta < 6:
				color = colorsCategories()[compta]
			self.sfc_preguntes[compta] = render_text( self.cp[compta].name, color, 27, 1, '', 220 )

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

	def juguem( self, estat ):
		# estat 0 = edició, 1/2 = veure categories
		
		self.game.skin.set_domain( 'selcat' )
		frate = frameRate( Global.fps_limit )
		
		self.game.screen.fill( (0,0,0,0) )
		
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
				
				if estat == 0:

					if eventhandle.keyUp('r'):
						shuffle_databases()
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
			ypos %= Global.screen_y

			# Pintem el fons animat
			mou_fons += 8
			for num in range(0, 768):
				self.game.screen.blit( self.fons, (cos((float(mou_fons +num)) / 100.0) * 20, num), (0, (ypos + num) % 768, 1024, 1) )

			self.game.screen.blit( self.mascara_de_fons, (0, 0) )
			self.game.screen.blit( self.sel_quadres, (0, 0) )


			nelements = len(self.cp) if estat == 0 else 6

			posact= 220
			for compta in range(primer_element_a_la_vista, nelements):	
				if posact + self.sfc_preguntes[compta].get_height() > (768 -80)	:
					break
			
				if compta == seleccio:
					self.game.screen.fill( (64,64,64), (100, posact, 300, self.sfc_preguntes[compta].get_height() +3 ) )

				if compta < 6 :
					self.game.screen.blit( self.sfc_nombres[compta], (120, posact-3) )

				darrer_element_a_la_vista = compta
				self.game.screen.blit( self.sfc_preguntes[compta], ( 160,posact ))	

				posact += self.sfc_preguntes[compta].get_height() + 20

			if primer_element_a_la_vista > 0: 
				self.game.screen.blit( self.sel_fletxap, ( 386,216 + 10 + cos(time.time() * 10) * 10))

			if darrer_element_a_la_vista < nelements - 1:
				self.game.screen.blit( self.sel_fletxab, ( 386, 651 - 10 - cos(time.time()*10) * 10 ))

			if darrer_element_a_la_vista < seleccio: 	primer_element_a_la_vista += 1

			if primer_element_a_la_vista > seleccio: 	primer_element_a_la_vista -= 1

						
			self.game.screen.blit( self.sfc_preguntes[seleccio], ( 475, 220 ))	

			if seleccio != self.darrera_info: 	
				self.sfc_text_info0 = render_text( self.cp[seleccio].authors, self.selcat_color_text, 14, 1, '', 220 )
				self.sfc_text_info1 = render_text( self.cp[seleccio].description, self.selcat_color_text, 16, 1, '', 350 )
				self.sfc_text_info2 = render_text( self.cp[seleccio].players, self.selcat_color_text, 16, 1, '', 350 )
				self.sfc_text_info3 = render_text( u"N. Pregutes: " + str(len(self.cp[seleccio])), self.selcat_color_text, 16, 1, '', 350 )
				self.sfc_text_info4 = render_text( u"Idioma: " + self.cp[compta].language, self.selcat_color_text, 16, 1, '', 100 )
				self.sfc_text_info5 = render_text( u"Data creació: " + time.strftime('%d/%m/%Y', time.gmtime(self.cp[compta].time[0])), self.selcat_color_text, 16, 1, '', 350 )
				self.sfc_text_info6 = render_text( u"Data darrera modificació: " + time.strftime('%d/%m/%Y', time.gmtime(self.cp[seleccio].time[1])), self.selcat_color_text, 16, 1, '', 350 )

				self.sfc_cat = loadImage( self.cp[seleccio].image )
				if seleccio < 6:
					sfcmask = loadImage( 'filtre_c' + str(seleccio+1) + '.png' )
					self.sfc_cat.blit( sfcmask, (0,0))
				self.sfc_cat = pygame.transform.scale(self.sfc_cat, (184, 138) )

				self.darrera_info = seleccio
			
			self.game.screen.blit( self.sfc_text_info0, ( 475, 305 ))	
			self.game.screen.blit( self.sfc_text_info1, ( 490, 380 ))	
			self.game.screen.blit( self.sfc_text_info2, ( 490, 495 ))	
			self.game.screen.blit( self.sfc_text_info3, ( 490, 606 ))	
			self.game.screen.blit( self.sfc_text_info4, ( 765, 606 ))	
			self.game.screen.blit( self.sfc_text_info5, ( 490, 635 ))	
			self.game.screen.blit( self.sfc_text_info6, ( 490, 655 ))	
	
			self.game.screen.blit( self.sfc_cat, ( 697, 221 ))	
			
			if mostra_ajuda: self.game.screen.blit( self.help_overlay, (0,0))
			if mostra_credits: self.game.screen.blit( self.game.sfc_credits, (0,0))
			
			self.game.screen.blit( self.sel_reflexos, (0, 0) )

			frate.next( self.game.screen )
			
			# intercanviem els buffers de self.game.screen
			pygame.display.flip()


		return 0
