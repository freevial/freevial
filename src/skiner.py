# -*- coding: utf-8 -*-
 
#
# Freevial
# Game categories selector
#
# Copyright (C) 2007 The Freevial Team
#
# By Nil Oriol <nil@kumbaworld.com>
# By Carles Oriol <carles@kumbaworld.com>
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

from math import *
import ConfigParser, os
from common.freevialglob import *
from preguntes import *

skin_file='skin.ini'
skin_folder = ''

def setSkinName( nom ):
	skin_folder = nom
	skin_file = os.path.join( nom, 'skin.ini' )

class Skin:
	
	def __init__( self ):
				
		self.config = ConfigParser.ConfigParser()
		self.config.readfp(open(skin_file))
				
		self.skin_maxim_equips = int(self.config.get( 'game', 'max_teams' ))
		
		self.skin_folder = skin_folder
		
		self.skin_score_fons = self.config.get( 'score', 'background')
		self.skin_score_mascara_de_fons = self.config.get( 'score', 'background_mask')
		self.skin_score_element = self.config.get( 'score', 'element')
		self.skin_score_element_sel = self.config.get( 'score', 'sel_element')
		self.skin_score_element_sel_offsetx = int(self.config.get( 'score', 'sel_element_offsetx'))
		self.skin_score_element_sel_offsety = int(self.config.get( 'score', 'sel_element_offsety'))
		self.skin_score_teams_offsetx = int(self.config.get( 'score', 'teams_offsetx'))
		self.skin_score_teams_offsety = int(self.config.get( 'score', 'teams_offsety'))
		
		self.skin_score_figureta_visible = self.config.get( 'score', 'figureta_visible') 
		self.skin_score_figureta_mode = self.config.get( 'score', 'figureta_mode') # 0 - del 0 al 63 combinacions 1 - del 0 al 5 figures individuals
		self.skin_score_figureta_mascara = self.config.get( 'score', 'figureta_mask')
		
		self.skin_score_figureta_offsetx = int(self.config.get( 'score', 'figureta_offsetx'))
		self.skin_score_figureta_offsety = int(self.config.get( 'score', 'figureta_offsety'))
		
		self.skin_score_figureta_individual_pos = [[int(self.config.get( 'score', 'figureta_individual_pos_0_X')),int(self.config.get( 'score', 'figureta_individual_pos_0_Y'))], [int(self.config.get( 'score', 'figureta_individual_pos_1_X')),int(self.config.get( 'score', 'figureta_individual_pos_1_Y'))], [int(self.config.get( 'score', 'figureta_individual_pos_2_X')),int(self.config.get( 'score', 'figureta_individual_pos_2_Y'))], [int(self.config.get( 'score', 'figureta_individual_pos_3_X')),int(self.config.get( 'score', 'figureta_individual_pos_3_Y'))], [int(self.config.get( 'score', 'figureta_individual_pos_4_X')),int(self.config.get( 'score', 'figureta_individual_pos_4_Y'))], [int(self.config.get( 'score', 'figureta_individual_pos_5_X')),int(self.config.get( 'score', 'figureta_individual_pos_5_Y'))] ]
		
		self.skin_score_figureta_show_hide = self.config.get( 'score', 'figureta_show_hide') # 0 - Es mostren les parts aconseguides, 1 - S'amaguen les parts aconseguides
		
		self.skin_score_so_sub = self.config.get( 'score', 'sub_sound')
		self.skin_score_so_sub_vol = self.config.get( 'score', 'sub_sound_vol')
		self.skin_score_so_sub2 = self.config.get( 'score', 'sub_sound2')
		self.skin_score_so_sub2_vol = self.config.get( 'score', 'sub_sound2_vol')
		
		self.skin_score_ok = self.config.get( 'score', 'ok')
		self.skin_score_ok_vol = self.config.get( 'score', 'ok_vol')
		
		self.skin_score_locked = self.config.get( 'score', 'locked')
		self.skin_score_locked_pos = (int(self.config.get( 'score', 'locked_pos_X')),int(self.config.get( 'score', 'locked_pos_Y')))
		
		self.skin_score_so_de_fons = self.config.get( 'score', 'background_sound')
		self.skin_score_so_de_fons_vol = self.config.get( 'score', 'background_sound_vol')

		self.skin_score_desplaca_el_fons = self.config.get( 'score', 'move_background') # True o False = no hi ha scroll vertical
		self.skin_score_ones_al_fons = self.config.get( 'score', 'background_waves') # True o False = quiet
		
		self.skin_score_caixes = [int(self.config.get( 'score', 'boxes_0_X')),int(self.config.get( 'score', 'boxes_0_Y'))], [int(self.config.get( 'score', 'boxes_1_X')),int(self.config.get( 'score', 'boxes_1_Y'))], [int(self.config.get( 'score', 'boxes_2_X')),int(self.config.get( 'score', 'boxes_2_Y'))], [int(self.config.get( 'score', 'boxes_3_X')),int(self.config.get( 'score', 'boxes_3_Y'))], [int(self.config.get( 'score', 'boxes_4_X')),int(self.config.get( 'score', 'boxes_4_Y'))], [int(self.config.get( 'score', 'boxes_5_X')),int(self.config.get( 'score', 'boxes_5_Y'))]
		
		#------------------------------------------
		
		self.ypos = 0
		self.mou_fons = 0
		#-----------------------------------------------
	
		self.skin_roda_fons = self.config.get( 'wheel', 'wheel_background')
		self.skin_roda_front = self.config.get( 'wheel', 'wheel_front')
		self.skin_roda_paper = self.config.get( 'wheel', 'wheel_paper')
		

		self.skin_roda_so_dot = self.config.get( 'wheel', 'sound_wheel_dot')
		self.skin_roda_so_dot_vol = self.config.get( 'wheel', 'sound_wheel_dot_vol')
		self.skin_roda_so_evil = self.config.get( 'wheel', 'sound_wheel_evil')
		self.skin_roda_so_evil_vol = self.config.get( 'wheel', 'sound_wheel_evil_vol')
		self.skin_roda_so_sub = self.config.get( 'wheel', 'sound_wheel_sub')
		self.skin_roda_so_sub_vol = self.config.get( 'wheel', 'sound_wheel_sub_vol')
		self.skin_roda_tipografia = self.config.get( 'wheel', 'wheel_tipografia')
		
	def carregaGeneral ( self ):
		self.figureta = range(0,64)
		for num in range(0, 64):
			self.figureta[num] = self.skinLoadImage(( self.skin_score_figureta_mascara + str( num ).zfill(2) + '.png'), ('points/freevial_tot' + str( num ).zfill(2) + '.png' ))

		
			
	def skinLoadImage ( self, name1, name2 ):
	
		fullname = os.path.join( self.skin_folder, name1 )

		retval = None
		
		if 	os.path.exists( fullname ):
			retval = loadImage( fullname )
		else:
			retval = loadImage( name2 )
			
			
		return retval
		
		
	def skinLoadSound ( self, name1, vol1, name2, vol2, music = 0 ):
		
		fullname = os.path.join( self.skin_folder, name1)
		
		retval = None
		
		if os.path.exists( fullname ):
			retval = loadSound (fullname, volume = vol1, music = music)
		else:	
			retval = loadSound ( name2, volume = vol2, music = music )
		
		return retval
		
			
	def scoreCarrega ( self ):
		
		self.carregaGeneral()
		self.mascara_de_fons = self.skinLoadImage( self.skin_score_mascara_de_fons, 'fons_score.png' )
		self.fons = self.skinLoadImage( self.skin_score_fons, 'score_fons.png' )
		self.element_score = self.skinLoadImage( self.skin_score_element, 'element_score.png')
		self.seleccio_score = self.skinLoadImage( self.skin_score_element_sel, 'seleccio_score.png' )
		self.so_sub = self.skinLoadSound(self.skin_score_so_sub, self.skin_score_so_sub_vol, 'sub.ogg', 0.1)
		self.so_sub2 = self.skinLoadSound( self.skin_score_so_sub2, self.skin_score_so_sub2_vol, 'sub2.ogg', 0.4)
		self.so_ok = self.skinLoadSound( self.skin_score_ok, self.skin_score_ok_vol, 'cheer.ogg', 1 )
		self.sfc_llum = self.skinLoadImage( self.skin_score_locked, 'llum.png' )
		self.sfc_cursor = render_text( "_", (0,0,0), 30, 1)
	
	def scoreSoDeFons ( self ) :
		self.skinLoadSound( self.skin_score_so_de_fons, self.skin_score_so_de_fons_vol, 'score.ogg', 0.6, music = 1).play( -1 )
	
	def scoreSoOk ( self ):
		self.so_ok.play()
	
	def scorePlayClic1 ( self ):
		self.so_sub.play()
	
	def scorePlayClic2 ( self ):
		self.so_sub2.play()
	
	def barra_pos( self, total, posicio, color, ample, alt ):

		sfc = pygame.Surface( ( ample, alt), pygame.SRCALPHA, 32 )
		pygame.draw.rect(sfc, color, (0,0,ample-1,alt-1), 2)

		ample_rect = ample - 8

		pygame.draw.rect(sfc, (color[0], color[1], color[2], 64), (4, 4, ample_rect, alt - 8))
		if total != 0 and posicio != 0: 
			pos_ample = ( posicio * ample_rect ) / total 
			pygame.draw.rect(sfc, color, (4, 4, pos_ample, alt - 8))

		return sfc


	
	def scorePintaFons ( self, screen ):
								
		if self.skin_score_desplaca_el_fons:
			# Animem el fons
			self.ypos += 1
			self.ypos %= Global.screen_y
		
		xpinta = 0
		
		if self.skin_score_ones_al_fons:
			self.mou_fons += 8
			

		# Pintem el fons animat
		for num in range(0, 768):
			
			if self.skin_score_ones_al_fons:
				xpinta = cos((float(self.mou_fons +num)) / 100.0) * 20
		
			screen.blit( self.fons, (xpinta, num), (0, (self.ypos + num) % 768, 1024, 1) )


	def scorePintaMascaraDeFons ( self, screen ):

		screen.blit( self.mascara_de_fons, (0, 0) )
		
	def scorePintaPuntuacions( self, screen, joc, element_seleccionat, estat, escriu, mostra_estad, frate ):
			
		# pintem les puntuacions
		for num in range(0, self.skin_maxim_equips):
			ycaixa = self.skin_score_caixes[num][1]
			xcaixa = self.skin_score_caixes[num][0]

			if element_seleccionat == num:
				for compta in range( 0, self.seleccio_score.get_height() ):
					desp = 0 if not estat else ( cos( frate.segons() * 10.0 + (float(compta)/10.0) ) * 2.0 )
					screen.blit( self.seleccio_score, (xcaixa + self.skin_score_element_sel_offsetx + desp, ycaixa + self.skin_score_element_sel_offsety + compta), (0,compta, self.seleccio_score.get_width(),1) )

			
			if joc.teams[num].actiu:

				screen.blit( self.element_score, (xcaixa, ycaixa ) )
				
				screen.blit( self.figureta[joc.teams[num].figureta], (xcaixa + self.skin_score_figureta_offsetx, ycaixa + self.skin_score_figureta_offsety ) )

				if joc.teams[num].sfc_nom:
					joc.screen.blit( joc.teams[num].sfc_nom, (xcaixa + self.skin_score_teams_offsetx , ycaixa + self.skin_score_teams_offsety ) )
				ampletext = joc.teams[num].sfc_nom.get_width() if joc.teams[num].sfc_nom else 0
				if escriu and num == element_seleccionat:
					if (int(time.time() * 4) % 2) == 0: 
						screen.blit( self.sfc_cursor, (xcaixa + 25 + ampletext, ycaixa + 125 )) 
						
				color = (128,0,0) if (maxPunts(joc.teams) > joc.teams[num].punts ) else (0,128,0)
				pinta = render_text( str(joc.teams[num].punts).zfill(2), color, 150, 1)
				screen.blit( pinta, (xcaixa + 200, ycaixa - 15) )

				if mostra_estad:
					for cat in range(0,6):
						screen.blit( self.barra_pos( joc.teams[num].preguntes_tot[cat], joc.teams[num].preguntes_ok[cat],  colorsCategories()[cat], 50, 14 ), (xcaixa + 140, ycaixa + 21 + cat * 16) )


	def scorePintaLocked( self, screen ):
		
		if Global.LOCKED_MODE: 
			screen.blit( self.sfc_llum, (0, 0) )
			
			
	def rodaCarrega( self ):
		self.carregaGeneral()
		self.fons = self.skinLoadImage( self.skin_roda_fons, 'ruleta_fons.png' )
		self.front = self.skinLoadImage( self.skin_roda_front, 'ruleta_front.png' )
		self.paper = self.skinLoadImage( self.skin_roda_paper, 'ruleta_paper.png')
		self.so_dot = self.skinLoadSound(self.skin_roda_so_dot, self.skin_roda_so_dot_vol, 'dot.ogg', 1)
		self.so_evil = self.skinLoadSound(self.skin_roda_so_evil, self.skin_roda_so_evil_vol, 'evil.ogg', 1)
		self.so_sub = self.skinLoadSound(self.skin_roda_so_sub, self.skin_roda_so_sub_vol, 'sub.ogg', 0.3)
		self.so_cat = range(0, 6)
		for num in range(0, 6):
			self.so_cat[num] = self.skinLoadSound(soCategoria( num ), 1, soCategoria( num ), 1)
			
		for compta in range(0, self.skin_maxim_equips):
			sfc = render_text( textCategoria(compta), (0,0,0), 60, 1, self.skin_roda_tipografia, 350 );
			self.paper.blit( sfc, (122, 2+(compta * 200) + 100 - sfc.get_height() / 2 ))
			sfc = render_text( textCategoria(compta), colorsCategories()[compta], 60, 1, self.skin_roda_tipografia, 350 );
			self.paper.blit( sfc, (120, (compta * 200) + 100 - sfc.get_height() / 2 ))


		


#		self.help_on_screen = helpOnScreen( HOS_RODA_ATURA  )
#		self.help_on_screen.sec_timeout = 10
	
	def rodaSoEvil ( self ):
		self.so_evil.play()
	def rodaSoEvilStop ( self ):
		self.so_evil.stop()
	def rodaSoDot ( self ):
		self.so_dot.play(100)
	def rodaSoDotStop ( self ):
		self.so_dot.stop()
	def rodaSoSub ( self ):
		self.so_sub.play()
	def rodaSoCat ( self, resultat ):
		self.so_cat[ resultat - 1].play()
		
	def rodaGira ( self, joc ):
		joc.screen.blit( self.fons, (0,0) )

		self.nom_equip_sfc = render_text( joc.teams[joc.current_team].nom, (255,255,255), 30, 1 )
		self.nom_equip_sfc = pygame.transform.rotate ( self.nom_equip_sfc, 90 )
		
#		self.help_on_screen.activitat( )
	
	def rodaPinta ( self, joc, pos_fons, pos ):
		#pintem el paper freevial
		joc.screen.blit( self.fons, ( 0, pos_fons ) )
		joc.screen.blit( self.fons, ( 0, - 768 + pos_fons ) )
		
		#pintem el paper d'impressora
		joc.screen.blit( self.paper, ( 178, pos ) )
		joc.screen.blit( self.paper, ( 178, pos + 1200 ) )
		
		#pintem els marges vermells i degradats
		joc.screen.blit( self.front, (0,0) )	
		
		joc.screen.blit( self.nom_equip_sfc, (20, 748 - self.nom_equip_sfc.get_height()))
		joc.screen.blit( self.figureta[joc.teams[joc.current_team].figureta], (70, 630) )

	
