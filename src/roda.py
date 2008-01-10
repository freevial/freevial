# -*- coding: utf-8 -*-
 
#
# Freevial
# Category selection
#
# Copyright (C) 2007, 2008 The Freevial Team
#
# By Carles Oriol i Margarit <carles@kumbaworld.com>
# By Siegfried-Angel Gevatter Pujals <siggi.gevatter@gmail.com>
# By Nil Oriol <nil@kumbaworld.com>
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
import random
import time
import pygame

from common.freevialglob import *
from common.events import EventHandle
from preguntes import *
from skiner import Skin


##################################################
#
# Empaquetat en una classe del selector
#

class Roda:
	
	def __init__( self, joc ):
		
		self.joc = joc
		self.skin = Skin()
		
		self.fons = self.skin.configGet( 'wheel', 'wheel_background')
		self.front = self.skin.configGet( 'wheel', 'wheel_front')
		self.paper = self.skin.configGet( 'wheel', 'wheel_paper')
		
		self.maxim_equips = self.skin.configGetInt( 'game', 'max_teams' )

		self.roda_so_dot = self.skin.configGet( 'wheel', 'sound_wheel_dot')
		self.roda_so_dot_vol = self.skin.configGet( 'wheel', 'sound_wheel_dot_vol')
		self.roda_so_evil = self.skin.configGet( 'wheel', 'sound_wheel_evil')
		self.roda_so_evil_vol = self.skin.configGet( 'wheel', 'sound_wheel_evil_vol')
		self.roda_so_sub = self.skin.configGet( 'wheel', 'sound_wheel_sub')
		self.roda_so_sub_vol = self.skin.configGet( 'wheel', 'sound_wheel_sub_vol')
		self.tipografia = self.skin.configGet( 'wheel', 'wheel_tipografia')
		
		
		
		
		self.figureta = self.skin.LoadImageRange( "wheel", "figureta_mask", 64, 2)
		self.fons = self.skin.LoadImage( "wheel", 'wheel_background' )
		self.front = self.skin.LoadImage( "wheel", 'wheel_front' )
		self.paper = self.skin.LoadImage( "wheel", 'wheel_paper')
		self.so_dot = self.skin.LoadSound( "wheel", 'sound_wheel_dot', 'sound_wheel_dot_vol')
		self.so_evil = self.skin.LoadSound( "wheel", 'sound_wheel_evil', 'sound_wheel_evil_vol')
		self.so_sub = self.skin.LoadSound( "wheel", 'sound_wheel_sub', 'sound_wheel_sub_vol')
		self.so_cat = range(0, 6)

		
		for num in range(0, 6):
			self.so_cat[num] = loadSound(soCategoria( num ), 1)
						
		for compta in range(0, self.maxim_equips):
			sfc = render_text( textCategoria(compta), (0,0,0), 60, 1, self.tipografia, 350 );
			self.paper.blit( sfc, (122, 2+(compta * 200) + 100 - sfc.get_height() / 2 ))
			sfc = render_text( textCategoria(compta), colorsCategories()[compta], 60, 1, self.tipografia, 350 );
			self.paper.blit( sfc, (120, (compta * 200) + 100 - sfc.get_height() / 2 ))

		self.help_overlay = createHelpScreen( 'roda' )		
		
		self.help_on_screen = helpOnScreen( HOS_RODA_ATURA  )
		self.help_on_screen.sec_timeout = 10
	
	def juguem( self ):
		
		self.frate = frameRate( Global.fps_limit )
				
		self.so_evil.stop()
		self.so_dot.play(100)
		
		velocitat = 75
		deceleracio = 0
		
		pos = pos_fons = atura = frenant = time_fi = mostra_ajuda = mostra_credits = 0
		rodant = 1
		resultat = -1
		
		self.joc.screen.blit( self.fons, (0,0) )

		self.nom_equip_sfc = render_text( self.joc.teams[self.joc.current_team].nom, (255,255,255), 30, 1 )
		self.nom_equip_sfc = pygame.transform.rotate ( self.nom_equip_sfc, 90 )
#		velocitat = 75
#		deceleracio = 0
		
#		pos = pos_fons = atura = frenant = time_fi = mostra_ajuda = mostra_credits = 0
#		rodant = 1
#		resultat = -1
		
#		self.joc.screen.blit( self.fons, (0,0) )

#		nom_equip_sfc = render_text( self.joc.teams[self.joc.current_team].nom, (255,255,255), 30, 1 )
#		nom_equip_sfc = pygame.transform.rotate ( nom_equip_sfc, 90 )
		
#		figureta =  loadImage('points/freevial_tot' + str(self.joc.teams[self.joc.current_team].figureta).zfill(2) + '.png')

#		self.help_on_screen.activitat( )

		while 1:

			for event in pygame.event.get():

				eventhandle = EventHandle(event)
				
				#self.help_on_screen.activitat(event)
				
				if event.type == pygame.JOYBUTTONDOWN:
					translateJoystickEvent(event)
				
				if eventhandle.isQuit():
					sys.exit()
				
				if eventhandle.keyDown('PRINT'):
					screenshot(self.joc.screen)
				
				if eventhandle.keyUp('f', 'F11'):
					pygame.display.toggle_fullscreen()
				
				if eventhandle.keyUp('ESCAPE', 'q') and not Global.LOCKED_MODE:
					if not mostra_ajuda and not mostra_credits:
						if not (Global.MUSIC_MUTE or Global.SOUND_MUTE):
							pygame.mixer.fadeout(500)
						return 0
					else:
						mostra_ajuda = mostra_credits = 0
				
				if eventhandle.keyUp('F1', 'h'):
					mostra_ajuda ^= 1	
					mostra_credits = 0			

				if eventhandle.keyUp('F2'):
					mostra_credits ^= 1
					mostra_ajuda = 0
				
				if (eventhandle.isRelease('primary') or eventhandle.keyUp('RETURN', 'SPACE', 'KP_ENTER')) and rodant == 1:
					if resultat == -1: 	
						atura = 1
					else:
						return resultat
			
			if atura == 1:
				atura = 0
				pas = 3
				deceleracio = 20
				time_fi = time.time()
				
				if not frenant:
					frenant = 1
					self.so_sub.play()

			if time_fi != 0 and time.time() - time_fi > 2.5:
				return resultat

			# decelerem
			velocitat -= deceleracio
			if velocitat < 0: velocitat = 0
			
			# Si ja hem acabat de rodar afinem la selecció
			# a l'element més proper
			rpos = pos + 100
			if velocitat == 0 and rodant != 0:
				offset = int(rpos) % 200
				if offset != 0: 
					if offset > 100:
						pos += deceleracio if ( offset < (200 - deceleracio) ) else 1
					
					elif offset <= 100:
						pos -= deceleracio if ( offset > deceleracio ) else 1
					
						if pos <= -1200: pos += 1200
				
				else:
					resultat = 1 + int( ( ( - ( pos - 1550 ) / 200 ) ) % 6 )
					self.so_dot.stop()
					self.so_cat[ resultat - 1].play()
					if not  self.joc.teams[self.joc.current_team].teCategoria( resultat ):
						self.so_evil.play()
					rodant = 0
				
			if rodant == 1:
				pos_fons += velocitat * 2
				if pos_fons >= 768:	pos_fons -= 768
				
				pos -= velocitat
				if pos <= -1200: pos += 1200
				

			#pintem el paper freevial
			self.joc.screen.blit( self.fons, ( 0, pos_fons ) )
			self.joc.screen.blit( self.fons, ( 0, - 768 + pos_fons ) )
			
			#pintem el paper d'impressora
			self.joc.screen.blit( self.paper, ( 178, pos ) )
			self.joc.screen.blit( self.paper, ( 178, pos + 1200 ) )
			
			#pintem els marges vermells i degradats
			self.joc.screen.blit( self.front, (0,0) )	
			
			self.joc.screen.blit( self.nom_equip_sfc, (20, 748 - self.nom_equip_sfc.get_height()))
			self.joc.screen.blit( self.figureta[self.joc.teams[self.joc.current_team].figureta], (70, 630) )
						
			if mostra_ajuda: self.joc.screen.blit( self.help_overlay, (0,0))
			if mostra_credits: self.joc.screen.blit( self.joc.sfc_credits, (0,0))

			self.help_on_screen.draw( self.joc.screen, (350, 740) )
			
			self.frate.next( self.joc.screen )
			
			# Exchange self.joc.screen buffers

			pygame.display.flip()
