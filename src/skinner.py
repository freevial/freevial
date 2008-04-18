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

import sys
import os.path
import gettext
from math import *
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError

from common.freevialglob import *
from common.globals import Global

Global.skin_file = default_file = os.path.join(Global.basefolder, 'skin.ini')
Global.skin_folder = Global.basefolder

def setSkinName( path ):
	
	basename = sys.argv[sys.argv.index( '--skin' ) + 1]
	
	if not os.path.isdir( path ) and not '/' in basename:
		
		# If the directory doesn't exist, and it contains no slashes,
		# guess that it's not a path but just the name of the wanted
		# skin, and try to find it.
		
		calculated_path = firstExistingDirectory( basename,
			# Search directories:
			'/usr/share/games/freevial/skins/', 
			os.path.join(os.path.expanduser('~/'), '.freevial/skins/'),
			os.path.abspath('../skins/') )
		
		if calculated_path:
			path = calculated_path
	
	if not os.path.isdir( path ):
		print _('Could not find skin "%s".') % unicode(path, 'utf-8')
		sys.exit( 1 )
	
	Global.skin_folder = path
	Global.skin_file = os.path.join( path, 'skin.ini' )
	
	print _('Loading skin "%s"...') % unicode(Global.skin_folder, 'utf-8')

class Skin:
	
	def __init__( self ):
		
		self.defconfig = SafeConfigParser()
		self.defconfig.readfp(open(default_file, 'r'))				
		
		self.config = SafeConfigParser()
		self.config.readfp(open(Global.skin_file, 'r'))	
		
		Global.skin_folder = Global.skin_folder

		fontname = self.search_font_name('' )
		if fontname != '':
			set_default_font( fontname )
	
	def set_domain( self, domain ):
		self.domain = domain
	
	def configGet( self, field, domain = None ):
		
		try:
			text = self.config.get( domain if domain else self.domain, field )
		
		except (NoOptionError, NoSectionError):
			try:
				text = self.defconfig.get( domain if domain else self.domain, field )
			except (NoOptionError, NoSectionError):
				text = 0
		
		return text
	
	def configGetInt( self, field, domain = None ):	
		return int( self.configGet( field, domain ) ) 
	
	def configGetFloat( self, field, domain = None ):	
		return float( self.configGet( field, domain ) ) 
	
	def configGetBool( self, field, domain = None ):
		return True if self.configGet( field, domain ) == "True" else False

	def configGetEval( self, field, domain = None ):	
		toeval = self.configGet( field, domain )
		return eval( toeval ) 

	def configGetRGB( self, field, domain = None ):	
		return self.configGetEval( field, domain )
	
	def LoadImage( self, field, domain = None ):
		
		name = self.configGet( field, domain )
		fullname = os.path.join( Global.skin_folder, name )
		
		if os.path.exists( fullname ):
			retval = loadImage( fullname )
		else:
			retval = loadImage( name )
		
		return retval
	
	def LoadImageRange( self, name, maxrange, digits, domain = None ):
		
		torna = range(0, maxrange)
		pos = self.configGet( name, domain )
		
		for num in range(0, 64):
			torna[num] = loadImage(pos + str( num ).zfill(digits) + '.png')
		
		return torna
	
	def LoadSound( self, name, volume, music = 0, domain = None ):
		
		name = self.configGet( name, domain )
		volume = self.configGetFloat( volume, domain )
		
		fullname = os.path.join( Global.skin_folder, name )
		
		return loadSound( fullname if os.path.exists( fullname ) else name, volume = volume, music = music )

	def preguntadorCarregaFiguretes( self, joc, selcat ):
		self.mostra_punt_de_categoria = True
		self.figureta_no = loadImage('points/freevial_tot' + str( joc.teams[joc.current_team].figureta).zfill(2) + '.png')
		self.figureta_si = loadImage('points/freevial_tot' + str( joc.teams[joc.current_team].figureta | bitCategoria ( selcat )).zfill(2) + '.png')
		self.match_point = True if (joc.teams[joc.current_team].figureta | bitCategoria ( selcat ) == 63) else False

	def search_font_name( self, nomfont ):

		if nomfont == '':
			nomfont = self.configGet( 'default_font', 'game' )

		if nomfont != '':
			if not os.path.exists( nomfont ):
				fullname = os.path.join( unicode(Global.skin_folder, 'utf-8'), nomfont)	

				if os.path.exists( fullname ):
					nomfont = fullname

		return nomfont

	def render_text( self, cadena, color, mida, antialias = 0, nomfont = '', maxwidth = 0 ):

		nomfont == self.search_font_name( nomfont )

		return render_text( cadena, color, mida, antialias, nomfont, maxwidth )		

	def teamsGuanyador( self, teams ):
	
		return teamsGuanyador( teams, self.configGetInt("game_mode", "game") , self.configGetInt("game_limit", "game"))
