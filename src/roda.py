# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Selector de categories
#
# Carles 22/8/2007
#

import sys, pygame
import random
import os

import freevialglob
from freevialglob import Freevial_globals


##################################################
#
# Empaquetat en una classe del selector
#
# Carles 27/08/2007
# RainCT 26/08/2007
#

class Roda:

	def __init__( self, carpeta_dades ):

		self.carpeta_imatges = os.path.join(carpeta_dades, 'images') 
		self.carpeta_sons = os.path.join(carpeta_dades, 'sounds') 
		self.carpeta_fonts = os.path.join(carpeta_dades, 'fonts') 

		self.fons = pygame.image.load( os.path.join(self.carpeta_imatges, 'ruleta_fons.png' ))
		self.front = pygame.image.load( os.path.join(self.carpeta_imatges, 'ruleta_front.png' ))
		self.paper = pygame.image.load( os.path.join(self.carpeta_imatges, 'ruleta_paper.png' ))

		self.so_dot = pygame.mixer.Sound( os.path.join(self.carpeta_sons, 'dot.ogg' ))
		self.so_cher = pygame.mixer.Sound( os.path.join(self.carpeta_sons, 'cheer.ogg' ))

		self.so_cat = range(0,6)
		for compta in range(0,6):
			self.so_cat[compta] = pygame.mixer.Sound( os.path.join(self.carpeta_sons, 'c'+str( compta + 1)+'.ogg' ))


	def juguem( self, joc ):

		velocitat = 0
		deceleracio = 6

		pos = 0
		pos_fons = 0
		rodant = 0

		joc.pantalla.blit( self.fons, (0,0) )		

		while 1:

			for event in pygame.event.get():
				if event.type == pygame.QUIT: return -1
				if event.type == pygame.KEYUP and ( event.key == pygame.K_q or event.key == pygame.K_ESCAPE): return -1

				if event.type == pygame.MOUSEBUTTONUP and rodant == 0:
					self.so_cher.stop()
					self.so_dot.play(100)
					velocitat = 100.0 + random.random() * 300.0
					deceleracio = int(5 + random.random() * 4)
					rodant = 1
					pos = -random.random() * 1200

				if event.type == pygame.KEYUP and (event.key == pygame.K_f or event.key == pygame.K_F11): pygame.display.toggle_fullscreen()

			# decelerem
			velocitat -= deceleracio
			if velocitat < 0: velocitat = 0

			# Si ja hem acabat de rodar afinem la selecció
			# a l'element més proper

			rpos = pos + 100
			if ( velocitat == 0 and rodant != 0 ) :
				offset = int(rpos) % 200
				if (offset != 0): 
					if (offset > 100): 
						pos += deceleracio if ( offset < (200 - deceleracio)) else 1

					elif (offset <= 100 ): 
						pos -= deceleracio if ( offset > deceleracio) else 1

						if( pos <= -1200): pos += 1200

				else:
					cat = 1 + int( ( ( - ( pos - 1550 ) / 200 ) ) % 6)
					self.so_dot.stop()
					self.so_cat[ cat - 1].play()
					self.so_cher.play()
					rodant = 0

			if rodant == 1:
				pos_fons += velocitat * 2
				if pos_fons >= 768:	pos_fons -= 768
				
				pos -= velocitat
				if( pos <= -1200): pos += 1200

			#pintem el paper freevial
			joc.pantalla.blit( self.fons, ( 0, pos_fons ) )
			joc.pantalla.blit( self.fons, ( 0, - 768 + pos_fons ) )

			#pintem el paper d'impressora
			joc.pantalla.blit( self.paper, ( 178, pos ) )
			joc.pantalla.blit( self.paper, ( 178, pos + 1200 ) )
	
			#pintem els marges vermells i degradats 
			joc.pantalla.blit( self.front, (0,0) )	

			#intercanviem els buffers de joc.pantalla		
			pygame.display.flip()

			#limitem els FPS			
			pygame.time.Clock().tick( joc.Limit_FPS )
