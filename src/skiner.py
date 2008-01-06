# -*- coding: utf-8 -*-
 
#
# Freevial
# Skin Stuff
#
# Copyright (C) 2007, 2008 The Freevial Team
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

import os
import gettext
from math import *
from ConfigParser import ConfigParser

from common.freevialglob import *
from preguntes import *

skin_file = u'skin.ini'
skin_folder = ''

def setSkinName( nom ):
	global skin_folder, skin_file
	skin_folder = nom
	skin_file = os.path.join( nom, u'skin.ini' )
	print _('Loading skin "%s"...') % unicode(skin_folder, 'utf-8')

class Skin:
	
	def __init__( self ):
			
		global skin_folder, skin_file
		
		self.defconfig = ConfigParser()
		self.defconfig.readfp(open(u'skin.ini'))				
				
		self.config = ConfigParser()
		self.config.readfp(open(skin_file))	
	
		self.skin_folder = skin_folder
	
	
	def configGet( self, grup, entrada ):
		
		try:
			text = self.config.get( grup, entrada)			
		except Exception:
			try:
				text = self.defconfig.get( grup, entrada)	
			except Exception:
				text = ""
		
		return text
	
	def configGetInt( self, grup, entrada ):	
		return int( self.configGet( grup, entrada) ) 
	
	def configGetFloat( self, grup, entrada ):	
		return float( self.configGet( grup, entrada) ) 
	
	def configGetBool( self, grup, entrada ):
		return True if self.configGet( grup, entrada ) == "True" else False
	
				
	def LoadImage ( self, grup, name ):
		print "Load Image", grup, name
		
		name1 = self.configGet( grup, name )
		
		fullname = os.path.join(  unicode(self.skin_folder, 'utf-8'), name1 )

		retval = None
		
		if 	os.path.exists( fullname ):
			retval = loadImage( fullname )
		else:
			retval = loadImage( name1 )			

		return retval
		
	def LoadImageRange ( self, grup, name, maxrange, digits ):
		
		torna = range(0, maxrange)
		pos = self.configGet( grup, name )
		
		for num in range(0, 64):
			torna[num] = loadImage(pos + str( num ).zfill(digits) + '.png')
	
		return torna
		
	def LoadSound ( self, grup, name, vol, musics = "" ):
		print "Load sound", grup, name
		
		name2 = self.configGet( grup, name )
		vol1 = self.configGetFloat( grup, vol )
		
		if( musics != ""):
			music = self.configGetInt( grup, musics )
		else:
			music = 0
		
				
		fullname = os.path.join( unicode(self.skin_folder, 'utf-8'), name2)		
		
		retval = None
		
		if os.path.exists( fullname ):
			retval = loadSound (fullname, volume = vol1, music = music)
		else:	
			retval = loadSound ( name2, volume = vol1, music = music )
		
		return retval
	
	
	def inicia_vell( self ):
		global skin_folder, skin_file
		
		self.defconfig = ConfigParser.ConfigParser()
		self.defconfig.readfp(open('skin.ini'))				
				
		self.config = SafeConfigParser()
		self.config.readfp(open(skin_file))		
				
		self.skin_maxim_equips = self.configGetInt( 'game', 'max_teams' )
		
		self.skin_folder = skin_folder
		

	
		self.skin_roda_fons = self.configGet( 'wheel', 'wheel_background')
		self.skin_roda_front = self.configGet( 'wheel', 'wheel_front')
		self.skin_roda_paper = self.configGet( 'wheel', 'wheel_paper')
		

		self.skin_roda_so_dot = self.configGet( 'wheel', 'sound_wheel_dot')
		self.skin_roda_so_dot_vol = self.configGet( 'wheel', 'sound_wheel_dot_vol')
		self.skin_roda_so_evil = self.configGet( 'wheel', 'sound_wheel_evil')
		self.skin_roda_so_evil_vol = self.configGet( 'wheel', 'sound_wheel_evil_vol')
		self.skin_roda_so_sub = self.configGet( 'wheel', 'sound_wheel_sub')
		self.skin_roda_so_sub_vol = self.configGet( 'wheel', 'sound_wheel_sub_vol')
		self.skin_roda_tipografia = self.configGet( 'wheel', 'wheel_tipografia')
		
		#--------------------------------------------------------
		
		self.skin_preguntador_color_de_fons_red = self.configGetInt('preguntador','color_de_fons_red')
		self.skin_preguntador_color_de_fons_green = self.configGetInt('preguntador','color_de_fons_green')
		self.skin_preguntador_color_de_fons_blue = self.configGetInt('preguntador','color_de_fons_blue')
		self.skin_preguntador_color_de_text_red = self.configGetInt('preguntador','color_de_text_red')
		self.skin_preguntador_color_de_text_green = self.configGetInt('preguntador','color_de_text_green')
		self.skin_preguntador_color_de_text_blue = self.configGetInt('preguntador','color_de_text_blue')
		self.skin_preguntador_color_de_fons = (self.skin_preguntador_color_de_fons_red, self.skin_preguntador_color_de_fons_green, self.skin_preguntador_color_de_fons_blue)
		self.skin_preguntador_color_de_text = (self.skin_preguntador_color_de_text_red, self.skin_preguntador_color_de_text_green, self.skin_preguntador_color_de_text_blue)
		
		self.skin_preguntador_mida_font = self.configGetInt('preguntador','mida_font')
		self.skin_preguntador_altlinies = self.skin_preguntador_mida_font + 5
		self.skin_preguntador_postextx= self.configGetInt('preguntador','postextx')
		self.skin_preguntador_postexty = self.configGetInt('preguntador','postexty')
		self.skin_preguntador_mascara_de_fons = self.configGet('preguntador','mascara_de_fons')
		self.skin_preguntador_retalla_sel = self.configGet('preguntador','retalla_sel')
		
		self.skin_preguntador_solucio_ok = self.configGet('preguntador','solucio_ok')
		self.skin_preguntador_solucio_nook = self.configGet('preguntador','solucio_nook')
		
		self.skin_preguntador_lletraA = self.configGet('preguntador','lletraA')
		self.skin_preguntador_lletraB = self.configGet('preguntador','lletraB')
		self.skin_preguntador_lletraC = self.configGet('preguntador','lletraC')
		self.skin_preguntador_lletraAoff = self.configGet('preguntador','lletraAoff')
		self.skin_preguntador_lletraBoff = self.configGet('preguntador','lletraBoff')
		self.skin_preguntador_lletraCoff = self.configGet('preguntador','lletraCoff')
		
		self.skin_preguntador_itr1 = self.configGet('preguntador','itr1')
		self.skin_preguntador_itr2 = self.configGet('preguntador','itr2')
		
		self.skin_preguntador_so_ticking2 = self.configGet( 'preguntador', 'so_ticking2')
		self.skin_preguntador_so_ticking2_vol = self.configGet( 'preguntador', 'so_ticking2_vol')
		
		self.skin_preguntador_so_drum2 = self.configGet( 'preguntador', 'so_drum2')
		self.skin_preguntador_so_drum2_vol = self.configGet( 'preguntador', 'so_drum2_vol')
		
		self.skin_preguntador_so_sub = self.configGet( 'preguntador', 'so_sub')
		self.skin_preguntador_so_sub_vol = self.configGet( 'preguntador', 'so_sub_vol')
		
		self.skin_preguntador_so_ok = self.configGet( 'preguntador', 'so_ok')
		self.skin_preguntador_so_ok_vol = self.configGet( 'preguntador', 'so_ok_vol')
		
		self.skin_preguntador_so_nook = self.configGet( 'preguntador', 'so_nook')
		self.skin_preguntador_so_nook_vol = self.configGet( 'preguntador', 'so_nook_vol')
		
		self.skin_preguntador_mostranpregunta = self.configGet( 'preguntador', 'mostranpregunta')
		
	#	self.skin_preguntador_mostra_punt_de_categoria = self.configGet( 'preguntador', 'mostra_punt_de_categoria')
	#	self.skin_preguntador_match_point = self.configGet( 'preguntador', 'match_point')
	
		

		


	
			
			
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

	def preguntadorCarrega( self, joc ):
		
		self.preguntadorYpos = 190
		
		self.color_de_fons = self.skin_preguntador_color_de_fons
		self.color_de_text = self.skin_preguntador_color_de_text
		
		self.mida_font = self.skin_preguntador_mida_font
		self.altlinies = self.skin_preguntador_altlinies
		self.postextx = self.skin_preguntador_postextx
		self.postexty = self.skin_preguntador_postexty
		
		self.mascara_de_fons = self.skinLoadImage( self.skin_preguntador_mascara_de_fons, 'mascara_de_fons.png' )
		self.retalla_sel = self.skinLoadImage( self.skin_preguntador_retalla_sel, 'retalla_sel.png' )
		
		self.solucio_ok = self.skinLoadImage( self.skin_preguntador_solucio_ok, 'ok.png' )
		self.solucio_nook = self.skinLoadImage( self.skin_preguntador_solucio_nook, 'nook.png' )
		
		self.fons = range(0, 6)
		for num in range(0, 6):
			self.fons[num] = loadImage( nomImatgeCategoria( num ) )
			sfcmask = loadImage( 'filtre_c' + str(num+1) + '.png' )
			self.fons[num].blit( sfcmask, (0,0))
		
		self.mascara = pygame.Surface((655, 150), pygame.SRCALPHA, 32)
		
		self.lletres = [
								[ self.skinLoadImage(self.skin_preguntador_lletraA, 'lletraA.png'), self.skinLoadImage(self.skin_preguntador_lletraAoff, 'lletraA_off.png') ], 
								[ self.skinLoadImage(self.skin_preguntador_lletraB, 'lletraB.png'), self.skinLoadImage(self.skin_preguntador_lletraBoff, 'lletraB_off.png') ], 				
								[ self.skinLoadImage(self.skin_preguntador_lletraC, 'lletraC.png'), self.skinLoadImage(self.skin_preguntador_lletraCoff, 'lletraC_off.png') ],
							]
		
		self.info = [ self.skinLoadImage(self.skin_preguntador_itr1, 'itr1.png'), self.skinLoadImage(self.skin_preguntador_itr2, 'itr2.png') ]	
		
		
		self.so_ticking2 = self.skinLoadSound(self.skin_score_so_sub, self.skin_score_so_sub_vol,'ticking2.ogg', 1)
		self.so_drum2 = self.skinLoadSound(self.skin_score_so_sub, self.skin_score_so_sub_vol,'drum2.ogg', 1)
		self.so_sub = self.skinLoadSound(self.skin_score_so_sub, self.skin_score_so_sub_vol,'sub.ogg', 0.1)
		self.so_ok = self.skinLoadSound(self.skin_score_so_sub, self.skin_score_so_sub_vol,'cheer.ogg', 1)
		self.so_nook = self.skinLoadSound(self.skin_score_so_sub, self.skin_score_so_sub_vol,'crboo.ogg', 1)
		
		self.nom_equip_sfc = render_text( joc.teams[joc.current_team].nom, (64,64,64), 30, 1 )	
		self.nom_equip_sfc = pygame.transform.rotate ( self.nom_equip_sfc, 90 )
		self.nom_equip_sfc.set_alpha( 64 )

		self.compos = 768


	def so_drum2_play ( self ):
		self.so_drum2.play()
		
	def so_ok_play ( self ):
		self.so_ok.play()
		
	def so_nook_play ( self ):
		self.so_nook.play()
		
	def so_sub_play ( self ):
		self.so_sub.play()
		
	def so_drum2_stop ( self ):
		self.so_drum2.stop()


	###########################################
	#
	# Funció per pintar el text i les preguntes sobre una nova superficie
	# usant el color del text i el sobrejat
	def preguntadorPintatext( self, textapintar, maxample = 0 ):

		nalt = 0

		cadenes = textapintar.split('#')
		sfc_pregunta = range(0, len(cadenes) )
		sfc_shad = range(0, len(cadenes) )

		nlinia = 0

		for cadena in cadenes:
			sfc_pregunta[nlinia] = render_text( cadena if cadena != "" else " ", self.color_de_text, self.skin_preguntador_mida_font, 1, '', maxample - 2)
			sfc_shad[nlinia] = render_text( cadena if cadena != "" else " ", self.color_de_fons, self.skin_preguntador_mida_font, 1, '', maxample - 2)
			nalt += sfc_pregunta[nlinia].get_height() + 2				     
			nlinia += 1
		
		sfc = pygame.Surface( ( 1024 if maxample == 0 else maxample, nalt ), pygame.SRCALPHA, 32 )

		nalt = 0
		nlinia = 0
		for cadena in cadenes:
			sfc.blit( sfc_shad[nlinia], (0 + 2, nalt + 2))
			sfc.blit( sfc_pregunta[nlinia], (0, nalt ))
			nalt += sfc_pregunta[nlinia].get_height() + 2
			nlinia += 1
			
		return sfc
			

	###########################################
	#
	# Inicialitzador de nova pregunta
	#
	def preguntadorInicialitza_pregunta( self, current_question, num_asked_questions ):

		self.sfc_pregunta  = self.preguntadorPintatext( current_question['text'], 1024 - 175 )

		self.sfc_resposta = range(0, 3)
		for num in xrange(0, 3):
			self.sfc_resposta[ num ] = self.preguntadorPintatext( current_question[ 'opt' + str(num + 1) ], 1024 - 260 )

		self.sfc_npregunta = render_text( str(num_asked_questions), (255,255,255), 100 )
		self.sfc_npregunta.set_alpha( 64 )

		self.sfc_apregunta = render_text( str(current_question['author']), (255,255,255), 16 )
		self.sfc_apregunta.set_alpha( 64 )	

		self.temps_inici_pregunta = time.time()
		self.segons = 61
		self.so_drum2_play()
		self.so_drum2_stop()

		self.show_answers = 0
		
		
	def preguntadorCarregaFiguretes( self, joc, selcat ):
		self.mostra_punt_de_categoria = True
		self.figureta_no = loadImage('points/freevial_tot' + str( joc.teams[joc.current_team].figureta).zfill(2) + '.png')
		self.figureta_si = loadImage('points/freevial_tot' + str( joc.teams[joc.current_team].figureta | bitCategoria ( selcat )).zfill(2) + '.png')
		self.match_point = True if (joc.teams[joc.current_team].figureta | bitCategoria ( selcat ) == 63) else False




			
	def preguntadorPinta( self, joc, categoria, selected, mostra_comentaris ):		
		# Animem el fons
		self.ypos += 2
		if self.ypos >= Global.screen_y: self.ypos %= Global.screen_y
			
		# Pintem el fons animat
		joc.screen.blit( self.fons[categoria - 1], (0,0), (0, (768 - self.ypos), Global.screen_x, min(200, self.ypos)))
		if self.ypos < 200:
			joc.screen.blit( self.fons[categoria - 1], (0, min( 200, self.ypos)), (0, 0, Global.screen_x, 200 - min( 200, self.ypos)))
		
		# i el sombrejem per fer l'efecte de desapariió
		# també pintem el logotip del peu a l'hora que esborrem el fons de self.joc.screen
		joc.screen.blit( self.mascara_de_fons, (0, 0) )
		
		# preparem el sobrejat de l'opció seleccionada
		ympos = self.ypos + 300
		ympos %= 768
		self.mascara.blit( self.fons[ categoria - 1], (0,0), (0, (768 - ympos), Global.screen_x, min( 200, ympos )))
		
		if ympos < 200: 
			self.mascara.blit( self.fons[ categoria - 1], (0, min( 200, ympos)), (0, 0, Global.screen_x, 200 - min( 200, ympos)))
		
		# i el mesclem amb la mascara per donar-li forma
		self.mascara.blit( self.retalla_sel, (0,0))
			
		# pintem l'ombrejat on correspongui	
		if selected == 1: joc.screen.blit( self.mascara, ( self.postextx, 260))
		if selected == 2: joc.screen.blit( self.mascara, ( self.postextx, 260+150))
		if selected == 3: joc.screen.blit( self.mascara, ( self.postextx, 260+300))
		
		# mostrem l'autor i el nombre de pregunta
		if self.skin_preguntador_mostranpregunta != 'False' :
			joc.screen.blit( self.sfc_npregunta, (1024 - ( self.sfc_npregunta.get_width() + 25), 0) )
			joc.screen.blit( self.sfc_apregunta, (1024 - ( self.sfc_apregunta.get_width() + 25), 94) )
			
		# mostrem la pregunta
		joc.screen.blit( self.sfc_pregunta, (self.postextx, self.postexty) )	
			
		# i les solucions			
		linia_act = 270
			
		for num in range(0, 3):
			joc.screen.blit( self.lletres[num][(selected != num + 1)], ( self.postextx, linia_act + (150 * num)) )
			joc.screen.blit( self.sfc_resposta[ num ], (self.postextx + 180 , linia_act + 20 + (150 * num)) )		
			
		# comprovem l'estat del temps
		segons_act = 60 - int( (time.time() - self.temps_inici_pregunta) )
		if segons_act < 0: 
			segons_act = 0
			self.segons = 0
			
		# si no estem en l'estat de mostrar les soŀlucions mostrem el temps restant
		if self.show_answers == 0:
			if self.segons != segons_act:
				# el segon actual ha canviat
				self.segons = segons_act 
				self.pinta_segons = render_text( str( self.segons ).zfill(2), (255,255,255), 600)
				# s'acaba el temps indiquem'ho amb so
				if self.segons < 20:
					self.so_ticking2.set_volume( (20 - float( self.segons )) / 20.0  ) 
					self.so_ticking2.play()
			
				# pintem els segons que queden, posant-los cada cop menys transparents
			self.pinta_segons.set_alpha( (60 - segons_act) )
			joc.screen.blit( self.pinta_segons, ( 300 , 150) )
			
		# Pintem les solucions
		linia_act = 270
		posn = 700
		posnook = 700 + cos(time.time()) * 25
		posok = 700 + cos(time.time() * 2) * 50
		
		if self.show_answers > 0:
				
			for num in range (0, 3):
				if self.current_question['answer'] == (num + 1):
					if selected != (num + 1):
						joc.screen.blit( self.solucio_nook, (posnook, linia_act + (150 * num)) )
					else:
						joc.screen.blit( self.solucio_ok, (posok, linia_act + (150 * num)) )
					
				else:
					if selected == (num + 1):
						joc.screen.blit( self.solucio_nook, (posnook, linia_act + (150 * num)) )
				
			if len( self.current_question['comment'] ) > 5:
				joc.screen.blit( self.info[0] if (int(time.time() * 3) % 3) == 0 else self.info[1], (self.postextx, 150) )
			
		if self.mostra_punt_de_categoria:
			if self.match_point:
				t = time.time()
				for compta in range( 0, 16 ) :
					joc.screen.blit( self.figureta_no if (int(time.time() * 2) % 2) == 0 else self.figureta_si, (500 + cos(t+(float(compta)/15)) * 400, 110 + sin((t + (float(compta)/10)) * 2) * 25) )
			else:
				joc.screen.blit( self.figureta_no if (int(time.time() * 2) % 2) == 0 else self.figureta_si, (880, 130) )

		
		joc.screen.blit( self.nom_equip_sfc, (20, 748 - self.nom_equip_sfc.get_height()))



		if mostra_comentaris:
			if self.compos > 0: self.compos -= 100 
			joc.screen.blit( sfc_comentaris, (0,self.compos))
		else:
			if self.compos < 768: 
				self.compos += 100
				joc.screen.blit( sfc_comentaris, (0,self.compos))
		
		

