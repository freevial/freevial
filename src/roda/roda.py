#!/usr/bin/python
# -*- coding: utf-8 -*-
 
##########################################
#
# Selector de categories
#
# Carles 22/8/2007
#



import sys, pygame
import random

mida_pantalla_x = 1024
mida_pantalla_y = 768
Limit_FPS = 60


velocitat = 0
deceleracio = 6

#pantalla = pygame.display.set_mode((mida_pantalla_x,mida_pantalla_y))
pantalla = pygame.display.set_mode( (mida_pantalla_x,mida_pantalla_y), pygame.HWSURFACE | pygame.DOUBLEBUF, 32 )


pygame.display.toggle_fullscreen()
pygame.mixer.init()

fons = pygame.image.load('imatges/ruleta_fons.png')
front = pygame.image.load('imatges/ruleta_front.png')
paper = pygame.image.load('imatges/ruleta_paper.png')

so_dot = pygame.mixer.Sound( "sons/dot.ogg" )
so_cher = pygame.mixer.Sound( "sons/cheer.ogg" )

so_cat = range(0,6)
so_cat[0] = pygame.mixer.Sound( "sons/c1.ogg" )
so_cat[1] = pygame.mixer.Sound( "sons/c2.ogg" )
so_cat[2] = pygame.mixer.Sound( "sons/c3.ogg" )
so_cat[3] = pygame.mixer.Sound( "sons/c4.ogg" )
so_cat[4] = pygame.mixer.Sound( "sons/c5.ogg" )
so_cat[5] = pygame.mixer.Sound( "sons/c6.ogg" )

pos = 0
pos_fons = 0
rodant = 0

def Scroll( surface, x, y, w, h, dx, dy ):

	surface.blit( surface, (x + dx, y + dy), (x, y, w - dx , h - dy) )

pantalla.blit( fons, (0,0) )		

while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYUP and event.key == pygame.K_q: sys.exit()

		if event.type == pygame.MOUSEBUTTONUP and rodant == 0:
			so_cher.stop()
			so_dot.play(100)
			velocitat = 100.0 + random.random() * 300.0
			deceleracio = int(5 + random.random() * 4)
			#print velocitat
			rodant = 1
			pos = -random.random() * 1200
		if event.type == pygame.KEYUP and event.key == pygame.K_f: pygame.display.toggle_fullscreen()

		
	#pos = pos + velocitat / 10
	velocitat = velocitat - deceleracio
	if velocitat < 0: 
		velocitat = 0

	rpos = pos + 100
	if velocitat == 0 and rodant != 0:
		offset = int(rpos) % 200
		if (offset != 0): 
			if (offset > 100): 
				if( offset < (200 - deceleracio)):
					pos = pos + deceleracio
				else:
					pos = pos + 1
			
				#print "menys"
			elif (offset <= 100 ): 
				if( offset > deceleracio):
					pos -= deceleracio
				else:
					pos = pos - 1

				if( pos <= -1200): pos += 1200
				#print "més"
			#print "acabant"
		else:
			#print "FI"
			print pos
			#print pos + (768 / 2) 
			cat = 1 + int(((-(pos-1550)/200)) % 6)
			print cat
			so_dot.stop()
			so_cat[ cat - 1].play()
			so_cher.play()
			rodant = 0


	#if pos >= 360: pos -= 360
	#mostra = int(pos/pasos_rotacio)

	#pantalla.blit( roda[mostra], (260-(roda[mostra].get_width() / 2), 300-(roda[mostra].get_height() / 2)) )		
	#pantalla.blit( sobre, (0,0) )	

	if rodant == 1:
		pos_fons += velocitat * 2
		if pos_fons >= 768:	pos_fons -= 768
		
		pos -= velocitat
		if( pos <= -1200): pos += 1200
		


	pantalla.blit( fons, (0, pos_fons) )
	pantalla.blit( fons, (0,-768 + pos_fons) )

	pantalla.blit( paper, (178, pos) )
	pantalla.blit( paper, (178, pos + 1200) )


	pantalla.blit( front, (0,0) )	

	pygame.display.flip()

	#pygame.time.Clock().tick( Limit_FPS )

	
	
