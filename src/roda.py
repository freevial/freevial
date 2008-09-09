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
import time
import pygame

from common.freevialglob import *
from common.events import eventLoop, waitForMouseRelease
from questions import get_databases


##################################################
#
# Empaquetat en una classe del selector
#

class Roda:
	
	def __init__( self, game ):
		
		self.game = game
		
		game.skin.set_domain( 'wheel' )
		
		self.fons = game.skin.configGet( 'wheel_background' )
		self.front = game.skin.configGet( 'wheel_front' )

		self.categories = []
		self.categoriesagafades = []
		self.maxim_equips = game.skin.configGetInt( 'max_teams', 'game' )
		
		self.roda_so_dot = game.skin.configGet( 'sound_wheel_dot' )
		self.roda_so_dot_vol = game.skin.configGet( 'sound_wheel_dot_vol' )
		self.roda_so_evil = game.skin.configGet( 'sound_wheel_evil' )
		self.roda_so_evil_vol = game.skin.configGet( 'sound_wheel_evil_vol' )
		self.roda_so_sub = game.skin.configGet( 'sound_wheel_sub' )
		self.roda_so_sub_vol = game.skin.configGet( 'sound_wheel_sub_vol' )
		self.tipografia = game.skin.configGet( 'wheel_tipografia' )
		
		self.score_figureta_visible = game.skin.configGetBool( 'figureta_visible') 
		
		if self.score_figureta_visible:
			self.figureta = game.skin.LoadImageRange( 'figureta_mask', 64, 2 )
			
		self.fons = game.skin.LoadImage( 'wheel_background' )
		self.front = game.skin.LoadImage( 'wheel_front' )
		self.paper = game.skin.LoadImage( 'wheel_paper')
		self.so_dot = game.skin.LoadSound( 'sound_wheel_dot', 'sound_wheel_dot_vol' )
		self.so_evil = game.skin.LoadSound( 'sound_wheel_evil', 'sound_wheel_evil_vol' )
		self.so_sub = game.skin.LoadSound( 'sound_wheel_sub', 'sound_wheel_sub_vol' )
		self.so_cat = range(0, 6)

		self.so_de_pas = game.skin.configGetInt( 'so_de_pas' )

		self.tipografia_mida = game.skin.configGetInt( 'wheel_tipografia_mida' )
		self.paper_text_width = game.skin.configGetInt( 'paper_text_width' )
		self.paper_text_offsetX = game.skin.configGetInt( 'paper_text_offsetX' )
		self.paper_offsetX = game.skin.configGetInt( 'paper_offsetX' )

		for num in range(0, 6):
			self.so_cat[num] = loadSound( get_databases(num).sound, volume = 1.0 )
		self.canviacat()			
		self.help_overlay = createHelpScreen( 'roda' )		
		
		self.help_on_screen = helpOnScreen( HOS_RODA_ATURA  )
		self.help_on_screen.sec_timeout = 10

		self.rewheelonrepeat = game.skin.configGetBool( 'rewheelonrepeat' );

		self.use_teamgotxies = self.game.skin.configGetBool( 'use_teamgotxies' )
		if self.use_teamgotxies:
			self.teamgotxies_pos = self.game.skin.configGetEval( 'teamgotxies_pos' )

	def canviacat( self ):
		
		self.categoriesagafades = []
		for num in range (0, 6):
			self.categoriesagafades += get_databases(num).name
		
		if self.categoriesagafades != self.categories:
			self.categories = self.categoriesagafades

			self.paper = self.game.skin.LoadImage( 'wheel_paper' )
			for num in range(0, 6):
				sfc = self.game.skin.render_text( get_databases(num).name, (0,0,0), self.tipografia_mida, 1, self.tipografia, self.paper_text_width );
				self.paper.blit( sfc, (self.paper_text_offsetX+2, 2+(num * 200) + 100 - sfc.get_height() / 2 ))
				sfc = self.game.skin.render_text( get_databases(num).name, colorsCategories()[num], self.tipografia_mida, 1, self.tipografia, self.paper_text_width );
				self.paper.blit( sfc, (self.paper_text_offsetX, (num * 200) + 100 - sfc.get_height() / 2 ))
	
	def juguem( self ):
		
		self.game.skin.set_domain( 'wheel' )

		self.canviacat()

		self.frate = frameRate( Global.fps_limit )
				
		self.so_evil.stop()
		self.so_dot.play(100)
		
		velocitat = self.game.skin.configGetInt( 'wheel_speed' )
		deceleracio = 0

		waitForMouseRelease( )
			
		pos = pos_fons = atura = frenant = time_fi = mostra_ajuda = mostra_credits = 0
		rodant = 1
		resultat = -1
		
		self.game.screen.blit( self.fons, (0,0) )

		self.nom_equip_sfc = self.game.skin.render_text( self.game.teams[self.game.current_team].nom, self.game.skin.configGetRGB( "team_name_color" ), 30, 1 )
		self.nom_equip_sfc = pygame.transform.rotate ( self.nom_equip_sfc, 90 )
		
		while 1:
			
			for event in eventLoop():
				
				if event.keyUp('ESCAPE', 'q') and not Global.LOCKED_MODE:
					if not mostra_ajuda and not mostra_credits:
						if not (Global.MUSIC_MUTE or Global.SOUND_MUTE):
							pygame.mixer.fadeout(500)
						return -1
					else:
						mostra_ajuda = mostra_credits = 0
				
				if event.keyUp('F1', 'h'):
					mostra_ajuda ^= 1	
					mostra_credits = 0			
				
				if event.keyUp('F2'):
					mostra_credits ^= 1
					mostra_ajuda = 0
				
				if event.isRelease('primary') or event.keyUp('RETURN', 'SPACE', 'KP_ENTER') and rodant == 1:
					atura = 1
			
			if time_fi != 0 and (time.time() - time_fi > 2.5 or (
			Global.SOUND_MUTE and time.time() - time_fi > 1)):
				# Note: The first time a question is shown the screen can take
				# ... up to some seconds until it loads. That is not a bug here.
				return resultat
			
			if atura == 1:
				atura = 0
				pas = 3
				deceleracio = self.game.skin.configGetInt( 'wheel_deccel' )
				
				if not frenant:
					frenant = 1
					self.so_sub.play()
			
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
						pos += if2(offset < (200 - deceleracio), deceleracio, 1)
					elif offset <= 100:
						pos -= if2(offset > deceleracio, deceleracio, 1)
						if pos <= -1200:
							pos += 1200
				else:
					resultat = int( ( ( - ( pos - 1550 ) / 200 ) ) % 6 )
					
					if self.rewheelonrepeat and self.game.teams[self.game.current_team].teCategoria( resultat ):
						velocitat = random.randint( 0, 1200 ) 
						atura = 0
						pas = 3
						deceleracio = self.game.skin.configGetInt( 'wheel_deccel' )
						frenant = 1
						self.so_sub.play()
					
					else:
						time_fi = time.time()
						self.so_dot.stop()
						self.so_cat[resultat].play()
						if self.so_de_pas == 1:
							self.so_evil.play()
						if self.so_de_pas == 2:
							if not self.game.teams[self.game.current_team].teCategoria( resultat ):
								self.so_evil.play()
						rodant = 0
			
			if rodant == 1:
				pos_fons += velocitat * 2
				if pos_fons >= 768:	pos_fons -= 768
				
				pos -= velocitat
				if pos <= -1200: pos += 1200

			#pintem el paper freevial
			self.game.screen.blit( self.fons, ( 0, pos_fons ) )
			self.game.screen.blit( self.fons, ( 0, - 768 + pos_fons ) )
			
			#pintem el paper d'impressora
			self.game.screen.blit( self.paper, ( self.paper_offsetX, pos ) )
			self.game.screen.blit( self.paper, ( self.paper_offsetX, pos + 1200 ) )
			
			#pintem els marges vermells i degradats
			self.game.screen.blit( self.front, (0,0) )	
			
			self.game.screen.blit( self.nom_equip_sfc, (20, 748 - self.nom_equip_sfc.get_height()))

			if self.use_teamgotxies:
				team = self.game.teams[self.game.current_team]

				if team.teamgotxie_sfc != None:
					self.game.screen.blit( team.teamgotxie_sfc, ( self.teamgotxies_pos[0] - team.teamgotxie_sfc.get_width() / 2, self.teamgotxies_pos[1] - team.teamgotxie_sfc.get_height() / 2 ) )
			
			if self.score_figureta_visible:
				self.game.screen.blit( self.figureta[self.game.teams[self.game.current_team].figureta], (70, 630) )
						
			if mostra_ajuda: self.game.screen.blit( self.help_overlay, (0,0))
			if mostra_credits: self.game.screen.blit( self.game.sfc_credits, (0,0))

			self.help_on_screen.draw( self.game.screen, (350, 740) )
			
			self.frate.next( self.game.screen )
			
			# Exchange self.game.screen buffers
			pygame.display.flip()
