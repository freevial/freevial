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

import sys, random, pygame, os





pantalla = pygame.display.set_mode( ( 1024, 768), 0, 32)

while 1:

	for event in pygame.event.get():
		if event.type == pygame.QUIT or ( event.type == pygame.KEYUP and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE) ): sys.exit()

		if event.type == pygame.KEYDOWN:
			print event.key
			print os.system('kbd_mode -s')
	
	pygame.display.flip()
