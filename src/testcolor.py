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
import time

pantalla = pygame.display.set_mode( ( 1024, 768), 0, 32)


image = pygame.image.load('../data/images/categoria_mc.png').convert_alpha()
image2 = pygame.transform.scale(pygame.image.load('../data/images/filtre_c5.png').convert_alpha(), (1024,768)) 
image.blit( image2, (0,0))


pantalla.blit( image, (0,0) )

while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT or ( event.type == pygame.KEYUP and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE) ): sys.exit()
		if event.type == pygame.MOUSEBUTTONDOWN: nomove = 1
		if event.type == pygame.MOUSEBUTTONUP: nomove = 0
		if event.type == pygame.KEYUP and ( event.key == pygame.K_f or event.key == pygame.K_F11 ): pygame.display.toggle_fullscreen()

	pantalla.blit( image, (0,0) )
	
	pygame.display.flip()



