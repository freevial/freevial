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
#GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, os, random, time, pygame
from freevialglob import *


##################################################
#
# Empaquetat en una classe del selector
#

class Roda:
	
	def __init__( self, joc ):
		
		self.joc = joc
		
		self.fons = loadImage('ruleta_fons.png')
		self.front = loadImage('ruleta_front.png')
		self.paper = loadImage('ruleta_paper.png')

		for compta in range(0,6):
			sfc = render_text( textCategoria(compta), (0,0,0), 50, 1, 'Ubuntu-Title.ttf', 350 );
			self.paper.blit( sfc, (122, 2+(compta * 200) + 100 - sfc.get_height() / 2 ))
			sfc = render_text( textCategoria(compta), colorsCategories()[compta], 50, 1, 'Ubuntu-Title.ttf', 350 );
			self.paper.blit( sfc, (120, (compta * 200) + 100 - sfc.get_height() / 2 ))
		
		self.so_dot = loadSound('dot.ogg')
		self.so_evil = loadSound('evil.ogg')
		
		self.so_cat = range(0, 6)
		for num in range(0, 6):
			self.so_cat[num] = loadSound( 'c' + str(num + 1) + '.ogg' )

		self.so_sub = loadSound('sub.ogg', volume = 0.3)
		
		self.help_overlay = createHelpScreen( 'roda' )

		self.help_on_screen = helpOnScreen( HOS_RODA_ATURA  )
		self.help_on_screen.sec_timeout = 15
	
	def juguem( self, joc = '' ):
		
		if joc != '': self.joc = joc
				
		self.so_evil.stop()
		self.so_dot.play(100)

		velocitat = 100
		deceleracio = 0
		
		pos = pos_fons = atura = frenant = time_fi = mostra_ajuda = mostra_credits = 0
		rodant = 1
		resultat = -1
		
		self.joc.pantalla.blit( self.fons, (0,0) )

		nom_equip_sfc = render_text( self.joc.equips[self.joc.equip_actual].nom, (255,255,255), 30, 1 )
		nom_equip_sfc = pygame.transform.rotate ( nom_equip_sfc, 90 )
		
		figureta =  loadImage('points/freevial_tot' + str(self.joc.equips[self.joc.equip_actual].figureta).zfill(2) + '.png')

		self.help_on_screen.activitat( )

		while 1:
		
			for event in pygame.event.get():

				self.help_on_screen.activitat( event )

				if event.type == pygame.QUIT:
					sys.exit()
				
				if keyPress(event, ('ESCAPE', 'q')):
					if not mostra_ajuda and not mostra_credits:
						if not ismute():
							pygame.mixer.fadeout(500)
						return 0
					else:
						mostra_ajuda = mostra_credits = 0
				
				if keyPress(event, ('PRINT')):
					screenshot( self.joc.pantalla )
				
				if keyPress(event, ('F1')) or keyPress(event, ('h')):
					mostra_ajuda ^= 1	
					mostra_credits = 0			

				if keyPress(event, ('F2')):
					mostra_credits ^= 1
					mostra_ajuda = 0
				
				if ( mouseClick(event, 'primary') or keyPress(event, ('RETURN', 'SPACE', 'KP_ENTER')) ) and rodant == 1:
	
					if resultat == -1: 	
						atura = 1
					else:
						return resultat
					
				if keyPress(event, ('f', 'F11')): pygame.display.toggle_fullscreen()
			
			if atura == 1:
				atura = 0
				pas = 3
				deceleracio = 20
				time_fi = time.time()
				
				if not frenant:
					frenant = 1
					self.so_sub.play()

			if time_fi != 0 and time.time() - time_fi > 5:
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
					self.so_dot.stop()
					self.so_cat[ resultat - 1].play()
					if not  self.joc.equips[self.joc.equip_actual].teCategoria( resultat ):
						self.so_evil.play()
					rodant = 0
				
			if rodant == 1:
				pos_fons += velocitat * 2
				if pos_fons >= 768:	pos_fons -= 768
				
				pos -= velocitat
				if pos <= -1200: pos += 1200
				
			#pintem el paper freevial
			self.joc.pantalla.blit( self.fons, ( 0, pos_fons ) )
			self.joc.pantalla.blit( self.fons, ( 0, - 768 + pos_fons ) )
			
			#pintem el paper d'impressora
			self.joc.pantalla.blit( self.paper, ( 178, pos ) )
			self.joc.pantalla.blit( self.paper, ( 178, pos + 1200 ) )
			
			#pintem els marges vermells i degradats
			self.joc.pantalla.blit( self.front, (0,0) )	
			
			self.joc.pantalla.blit( nom_equip_sfc, (20, 748 - nom_equip_sfc.get_height()))
			self.joc.pantalla.blit( figureta, (70, 630) )

			if mostra_ajuda: self.joc.pantalla.blit( self.help_overlay, (0,0))
			if mostra_credits: self.joc.pantalla.blit( self.joc.sfc_credits, (0,0))

			self.help_on_screen.draw( self.joc.pantalla, (400, 725 ) )

			#intercanviem els buffers de self.joc.pantalla
			pygame.display.flip()

			#limitem els FPS
			pygame.time.Clock().tick( self.joc.Limit_FPS )


