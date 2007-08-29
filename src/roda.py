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
		self.so_evil = loadSound('evil.ogg')
		
		self.so_cat = range(0, 6)
		for num in range(0, 6):
			self.so_cat[num] = loadSound( 'c' + str(num + 1) + '.ogg' )

		self.so_sub = loadSound('sub.ogg', volume = 0.3)
	
	def juguem( self, joc = '' ):
		
		if joc != '': self.joc = joc
				
		self.so_evil.stop()
		self.so_dot.play(100)

		velocitat = 100
		deceleracio = 0
		
		pos = pos_fons = atura = frenant = time_fi = 0
		rodant = 1
		resultat = -1
		
		self.joc.pantalla.blit( self.fons, (0,0) )

		nom_equip_sfc = render_text( self.joc.equips[self.joc.equip_actual].nom, (255,255,255), 30, 1 )
		nom_equip_sfc = pygame.transform.rotate ( nom_equip_sfc, 90 )
		
		figureta =  loadImage('points/freevial_tot' + str(self.joc.equips[self.joc.equip_actual].figureta).zfill(2) + '.png')

		while 1:
		
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				
				if keyPress(event, ('ESCAPE', 'q')):
					pygame.mixer.fadeout(500)
					return 0
				
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


			#intercanviem els buffers de self.joc.pantalla
			pygame.display.flip()

			
			#limitem els FPS
			pygame.time.Clock().tick( self.joc.Limit_FPS )


