#!/usr/bin/python
# -*- coding: utf-8 -*-
 
##########################################
#
# Iterador de fons mentre el concursant 
# pensa la pregunta
# 
# Cal sobreposar la pregunta i les respostes
#
# Carles 22/8/2007
#



import sys, pygame

mida_pantalla_x = 1024
mida_pantalla_y = 768


pantalla = pygame.display.set_mode((mida_pantalla_x,mida_pantalla_y))
nil = pygame.image.load('categoria2.png').convert()

ypos = 0

nomove = 0	

def Scroll( surface, x, y, w, h, dx, dy ):

	surface.blit( surface, (x + dx, y + dy), (x, y, w - dx , h - dy) )

pantalla.blit( nil, (0,ypos) )		

while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN: nomove = 1
		if event.type == pygame.MOUSEBUTTONUP: nomove = 0
		if event.type == pygame.KEYUP and event.key == pygame.K_f: pygame.display.toggle_fullscreen()

	
	if( nomove == 0 ):
		Scroll( pantalla, 0, 0, mida_pantalla_x, mida_pantalla_y, 0, 1 )

		for compta in range(100, mida_pantalla_y / 2, 30):
			Scroll( pantalla, 0, compta, mida_pantalla_x, mida_pantalla_y - compta * 2, 0, 1 )
		
	ypos = ypos + 1	
	if ypos >= mida_pantalla_y: ypos = 0


	pantalla.blit( nil, (0, 0), (0, (mida_pantalla_y-1)-ypos, mida_pantalla_x, 1) )

	pygame.display.flip()

	
	
