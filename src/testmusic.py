#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import pygame

pygame.display.set_mode( (640, 480), 0, 32)

pygame.mixer.pre_init(44100,-16,2, 1024 * 3)
pygame.mixer.init()

pygame.mixer.music.load( "../data/sounds/ma1.ogg" )

pygame.mixer.music.play(-1)


while ( 1 ):

			
	for event in pygame.event.get():
		if event.type == pygame.QUIT or ( event.type == pygame.KEYUP and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE) ): sys.exit()
	
	#limitem els FPS
	pygame.time.Clock().tick( 25 )
