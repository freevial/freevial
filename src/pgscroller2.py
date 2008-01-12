#!/usr/bin/python
# -*- coding: utf-8 -*-
 
##########################################
#
# Iterador de fons mentre el concursant 
# pensa la pregunta
# 
# Cal sobreposar la pregunta i les respostes
#
# Carles 22/08/2007
# RainCT 27/08/2007
#

import sys, random, pygame
import math

pantalla = pygame.display.set_mode( ( 1024, 768), 0, 32)

mida_pantalla_x = 1024
mida_pantalla_y = 768

ypos = 0
nomove = 0	

i = 1	
image = pygame.image.load('../data/images/categoria' + str(i) + '.png').convert_alpha()

def Scroll( surface, x, y, w, h, dx, dy ):
	surface.blit( surface, (x + dx, y + dy), (x, y, w - dx , h - dy) )

pantalla = pygame.display.set_mode((mida_pantalla_x, mida_pantalla_y))


pantalla.blit( image, (0,ypos) )

while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT or ( event.type == pygame.KEYUP and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE) ): sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN: nomove = 1
		if event.type == pygame.MOUSEBUTTONUP: nomove = 0
		if event.type == pygame.KEYUP and ( event.key == pygame.K_f or event.key == pygame.K_F11 ): pygame.display.toggle_fullscreen()

	

	ypos += 1	
	#if ypos >= mida_pantalla_y: ypos = 0
		

	for compta in range(0, 768):
		print compta
		pantalla.blit( image, (0, compta), (0, compta/((800-compta)/10), 1024, 1) )
	
	pygame.display.flip()
