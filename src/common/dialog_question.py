# -*- coding: utf-8 -*-
 
#
# Freevial
# Question Message
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

import sys
import os
import random
import time
import pygame

from freevialglob import *
from events import EventHandle

class Question:
	
	def ask( self, screen, pregunta, respostes, predeterminat = 0, cancel = -1 ):

		frate = frameRate( 40 )

		seleccio = predeterminat

		sfc_copiascreen = pygame.Surface( ( screen.get_width(), screen.get_height()), pygame.SRCALPHA, 32 )
		sfc_screen2 = pygame.Surface( ( screen.get_width(), screen.get_height()), pygame.SRCALPHA, 32 )

		sfc_copiascreen.blit( screen, (0,0) )

		total_duracio_fadeout = duracio_fadeout = 10
		intensitat_fadeout = 20

		sfc_pregunta = render_text( pregunta, (255,255,255), 50, 1, '', 600 )
		sfc_respostes = []

		espai_entre_respostes = 32
		respostes_ample = 0
		for compta in range(0, len(respostes) ):
			sfc = render_text( respostes[compta], (255,255,255), 50, 1, '', 500 )
			respostes_ample += sfc.get_width()
			if compta: respostes_ample += espai_entre_respostes

			sfc_respostes.append( sfc )

		while 1:

			for event in pygame.event.get():

				eventhandle = EventHandle(event)
				
				if event.type == pygame.JOYBUTTONDOWN:
					translateJoystickEvent(event)
				
				if eventhandle.isQuit():
					sys.exit()
				
				if eventhandle.keyUp('ESCAPE', 'q'):
					return cancel
				
				if eventhandle.keyDown('PRINT'):
					screenshot(self.joc.screen)
				
				if eventhandle.keyUp('f', 'F11'):
					pygame.display.toggle_fullscreen()
				
				if eventhandle.keyUp('RIGHT'):	
					seleccio += 1
					seleccio %= len(respostes)
				
				if eventhandle.keyUp('LEFT'):	
					seleccio -= 1
					seleccio %= len(respostes)
				
				if eventhandle.isRelease('primary') or eventhandle.keyUp('RETURN', 'SPACE', 'KP_ENTER'):
					return seleccio
				
			if duracio_fadeout:
				sfc_screen2.blit( sfc_copiascreen, (0,0) )
				sfc_screen2.fill( (0,0,0, total_duracio_fadeout * intensitat_fadeout - duracio_fadeout * intensitat_fadeout) ) 
	
				duracio_fadeout -= 1
				
			screen.blit( sfc_copiascreen, (0,0) )
			screen.blit( sfc_screen2, (0,0) )

			screen.blit( sfc_pregunta, (screen.get_width() / 2 -sfc_pregunta.get_width() / 2, 300) )

			posx = (screen.get_width() / 2 - respostes_ample / 2 )

			for compta in range(0, len(respostes) ):

				if seleccio == compta:
					for salt in range(0, 25):
						screen.fill( (salt * 10,0,0), (posx - 25 + salt, 450, sfc_respostes[compta].get_width() + 25-salt*2, sfc_respostes[compta].get_height()  ))

				screen.blit( sfc_respostes[compta], (posx, 450) )
				posx += sfc_respostes[compta].get_width() + espai_entre_respostes

			frate.next( screen )

			pygame.display.flip()


def fesPregunta( screen, pregunta, respostes, predeterminat = 0, cancel = -1 ):

	question = Question()

	return question.ask( screen, pregunta, respostes, predeterminat = 0, cancel = -1 )
