# -*- coding: utf-8 -*-
 
#
# Freevial
# Question Message
#
# Copyright (C) 2007, 2008 The Freevial Team
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
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import os
import pygame

from freevialglob import *
from events import EventHandle


class QuestionDialog:
	
	def ask( self, screen, question, answers, default = 0, cancel = -1, color = (255, 0, 0) ):
		
		frate = frameRate( Global.fps_limit )
		
		sfc_screen_bg = pygame.Surface( ( screen.get_width(), screen.get_height()), pygame.SRCALPHA, 32 )
		sfc_screen_bg.blit( screen, (0,0) )
		
		sfc_screen2 = pygame.Surface( ( screen.get_width(), screen.get_height() ), pygame.SRCALPHA, 32 )
		
		selection = default
		total_duracio_fadeout = duracio_fadeout = 10
		fadeout_intensity = 20
		
		sfc_question = render_text( question, (255,255,255), 50, 1, '', 600 )
		sfc_answers = []
		
		space_between_answers = 32
		answers_width = 0
		
		for num in range( 0, len(answers) ):
			sfc = render_text( answers[num], (255,255,255), 50, 1, '', 500 )
			answers_width += sfc.get_width()
			if num: answers_width += space_between_answers
			sfc_answers.append( sfc )
		
		while True:
			
			for event in pygame.event.get():
				
				eventhandle = EventHandle(event)
				if eventhandle.handled: continue
				
				if eventhandle.keyUp('ESCAPE', 'q'):
					return cancel
				
				if eventhandle.keyUp('RIGHT'):	
					selection += 1
					selection %= len(answers)
				
				if eventhandle.keyUp('LEFT'):	
					selection -= 1
					selection %= len(answers)
				
				if eventhandle.isRelease('primary') or eventhandle.keyUp('RETURN', 'SPACE', 'KP_ENTER'):
					return selection
			
			if duracio_fadeout:
				sfc_screen2.blit( sfc_screen_bg, (0,0) )
				sfc_screen2.fill( (0,0,0, total_duracio_fadeout * fadeout_intensity - duracio_fadeout * fadeout_intensity) ) 
				duracio_fadeout -= 1
			
			screen.blit( sfc_screen_bg, (0,0) )
			screen.blit( sfc_screen2, (0,0) )
			
			screen.blit( sfc_question, (screen.get_width() / 2 -sfc_question.get_width() / 2, 300) )
			
			posx = (screen.get_width() / 2 - answers_width / 2 )
			for num in range(0, len(answers) ):
				
				if selection == num:
					for salt in range(0, 25):
						screen.fill( (color[0] * salt / 25, color[1]* salt / 25, color[2]* salt / 25), (posx - 25 + salt, 450, sfc_answers[num].get_width() + 25*2-salt*2, sfc_answers[num].get_height()  ))
				
				screen.blit( sfc_answers[num], (posx, 450) )
				posx += sfc_answers[num].get_width() + space_between_answers
			
			frate.next( screen )
			pygame.display.flip()
