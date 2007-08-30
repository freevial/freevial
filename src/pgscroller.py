#!/usr/bin/python
# -*- coding: utf-8 -*-
 
#
# Freevial - Superseded Component
# Iterador de fons mentre el concursant pensa la pregunta
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

import sys, random, pygame

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
		if event.type == pygame.KEYUP and event.key == pygame.K_LEFT: image = getImage( currentImage - 1 )
		if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT: image = getImage( currentImage + 1 )
	
	if nomove == 0:
		Scroll( pantalla, 0, 0, mida_pantalla_x, mida_pantalla_y, 0, 1 )
		
		for num in range(100, mida_pantalla_y / 2, 30):
			Scroll( pantalla, 0, num, mida_pantalla_x, mida_pantalla_y - num * 2, 0, 1 )
	
	ypos = ypos + 1	
	if ypos >= mida_pantalla_y: ypos = 0
	
	pantalla.blit( image, (0, 0), (0, (mida_pantalla_y-1)-ypos, mida_pantalla_x, 1) )
	
	pygame.display.flip()
