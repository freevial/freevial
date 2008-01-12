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
		

		
		#--------------------------------------------------------
		

		
	#	self.skin_preguntador_mostra_punt_de_categoria = self.configGet( 'preguntador', 'mostra_punt_de_categoria')
	#	self.skin_preguntador_match_point = self.configGet( 'preguntador', 'match_point')
	
		

		


	
			
			
		


#		self.help_on_screen = helpOnScreen( HOS_RODA_ATURA  )
#		self.help_on_screen.sec_timeout = 10
	




	def so_ok_play ( self ):
		self.so_ok.play()
		
	def so_nook_play ( self ):
		self.so_nook.play()
		
	def so_sub_play ( self ):
		self.so_sub.play()
		


		
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
			
			

