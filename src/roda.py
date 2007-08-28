# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Selector de categories
#
# Carles 27/08/2007
# RainCT 27/08/2007
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
		
		self.so_dot = loadSound('dot.ogg')
		self.so_cher = loadSound('cheer.ogg')
		
		self.so_cat = range(0, 6)
		for num in range(0, 6):
			self.so_cat[num] = loadSound( 'c' + str(num + 1) + '.ogg' )
	
	def juguem( self ):
		
		velocitat = 0
		deceleracio = 6
		
		pos = 0
		pos_fons = 0
		rodant = 0
		
		self.joc.pantalla.blit( self.fons, (0,0) )		

		resultat = 0

		while 1:
		
			for event in pygame.event.get():
				if event.type == pygame.QUIT or keyPress(event, ('ESCAPE', 'q')):
					pygame.mixer.fadeout(500)
					return 0
				
				if ( event.type == pygame.MOUSEBUTTONUP or keyPress(event, ('RETURN', 'SPACE')) ) and rodant == 0:
					if resultat == 0:
						self.so_cher.stop()
						self.so_dot.play(100)
						velocitat = 100.0 + random.random() * 300.0
						deceleracio = int(5 + random.random() * 4)
						rodant = 1
						pos = -random.random() * 1200
					else:
						return resultat
					
				if keyPress(event, ('f', 'F11')): pygame.display.toggle_fullscreen()
			
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
					self.so_cher.play()
					rodant = 0
				
			if rodant == 1:
				pos_fons += velocitat * 2
				if pos_fons >= 768:	pos_fons -= 768
				
				pos -= velocitat
				if( pos <= -1200): pos += 1200
				
			#pintem el paper freevial
			self.joc.pantalla.blit( self.fons, ( 0, pos_fons ) )
			self.joc.pantalla.blit( self.fons, ( 0, - 768 + pos_fons ) )
			
			#pintem el paper d'impressora
			self.joc.pantalla.blit( self.paper, ( 178, pos ) )
			self.joc.pantalla.blit( self.paper, ( 178, pos + 1200 ) )
			
			#pintem els marges vermells i degradats
			self.joc.pantalla.blit( self.front, (0,0) )	
			
			#intercanviem els buffers de self.joc.pantalla
			pygame.display.flip()
			
			#limitem els FPS
			pygame.time.Clock().tick( self.joc.Limit_FPS )


