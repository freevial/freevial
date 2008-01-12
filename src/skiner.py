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
	
	def LoadSound ( self, grup, name, vol, music = 0 ):
		
		name2 = self.configGet( grup, name )
		vol1 = self.configGetFloat( grup, vol )
				
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

	#	self.help_on_screen = helpOnScreen( HOS_RODA_ATURA  )
	#	self.help_on_screen.sec_timeout = 10

	def preguntadorCarregaFiguretes( self, joc, selcat ):
		self.mostra_punt_de_categoria = True
		self.figureta_no = loadImage('points/freevial_tot' + str( joc.teams[joc.current_team].figureta).zfill(2) + '.png')
		self.figureta_si = loadImage('points/freevial_tot' + str( joc.teams[joc.current_team].figureta | bitCategoria ( selcat )).zfill(2) + '.png')
		self.match_point = True if (joc.teams[joc.current_team].figureta | bitCategoria ( selcat ) == 63) else False

	def render_text( self, cadena, color, mida, antialias = 0, nomfont = '', maxwidth = 0 ):


		if nomfont == '':
			nomfont = self.configGet( "game", "default_font" )

		print nomfont

		if nomfont != '':
			if not os.path.exists( nomfont ):
				fullname = os.path.join( unicode(self.skin_folder, 'utf-8'), nomfont)	

				print fullname
				if os.path.exists( fullname ):
					nomfont = fullname

		return render_text( cadena, color, mida, antialias, nomfont, maxwidth )		
