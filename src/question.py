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

import sys, os, random, time, pygame

from freevialglob import *

class Question:
	
	def ask( self, pantalla, pregunta, respostes, predeterminat = 0, cancel = -1 ):

		frate = frameRate( 40 )

		seleccio = predeterminat

		sfc_copiapantalla = pygame.Surface( ( pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA, 32 )
		sfc_pantalla2 = pygame.Surface( ( pantalla.get_width(), pantalla.get_height()), pygame.SRCALPHA, 32 )

		sfc_copiapantalla.blit( pantalla, (0,0) )

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

				if event.type == pygame.QUIT:
					sys.exit()
				
				if keyPress(event, ('ESCAPE', 'q')):
					return cancel		

				if keyPress(event, ('RIGHT')):	
					seleccio += 1
					seleccio %= len(respostes)

				if keyPress(event, ('LEFT')):	
					seleccio -= 1
					seleccio %= len(respostes)
				
				if ( mouseClick(event, 'primary') or keyPress(event, ('RETURN', 'SPACE', 'KP_ENTER')) ) :
					return seleccio
				
			if duracio_fadeout:
				sfc_pantalla2.blit( sfc_copiapantalla, (0,0) )
				sfc_pantalla2.fill( (0,0,0, total_duracio_fadeout * intensitat_fadeout - duracio_fadeout * intensitat_fadeout) ) 
	
				duracio_fadeout -= 1

#			pantalla.fill( (0,0,0,0) )
						
			pantalla.blit( sfc_copiapantalla, (0,0) )
			pantalla.blit( sfc_pantalla2, (0,0) )

			pantalla.blit( sfc_pregunta, (pantalla.get_width() / 2 -sfc_pregunta.get_width() / 2, 300) )

			posx = (pantalla.get_width() / 2 - respostes_ample / 2 )

			for compta in range(0, len(respostes) ):

				if seleccio == compta:
					for salt in range(0, 25):
						pantalla.fill( (salt * 10,0,0), (posx - 25 + salt, 450, sfc_respostes[compta].get_width() + 25-salt*2, sfc_respostes[compta].get_height()  ))

				pantalla.blit( sfc_respostes[compta], (posx, 450) )
				posx += sfc_respostes[compta].get_width() + espai_entre_respostes

			frate.next( pantalla )

			pygame.display.flip()


def fesPregunta( pantalla, pregunta, respostes, predeterminat = 0, cancel = -1 ):

	question = Question()

	return question.ask( pantalla, pregunta, respostes, predeterminat = 0, cancel = -1 )




