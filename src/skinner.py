# -*- coding: utf-8 -*-
 
#
# Freevial
# Skin Stuff
#
# Copyright (C) 2007-2009 The Freevial Team
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
from configparser import SafeConfigParser, NoOptionError, NoSectionError

from common.freevialglob import *
from common.globals import Global

Global.skin_file = default_file = os.path.join(Global.basefolder, 'skin.ini')
Global.skin_folder = Global.basefolder

def setSkinName(path):
	
	basename = sys.argv[sys.argv.index('--skin') + 1]
	
	if not os.path.isdir(path) and not '/' in basename:
		
		# If the directory doesn't exist, and it contains no slashes,
		# guess that it's not a path but just the name of the wanted
		# skin, and try to find it.
		
		calculated_path = first_existing_directory(basename,
			# Search directories:
			'/usr/share/games/freevial/skins/', 
			os.path.join(os.path.expanduser('~/'), '.freevial/skins/'),
			os.path.abspath('../skins/'))
		
		if calculated_path:
			path = calculated_path
	
	if not os.path.isdir(path):
		print(_('Could not find skin "%s".') % str(path))
		sys.exit(1)
	
	Global.skin_folder = path
	Global.skin_file = os.path.join(path, 'skin.ini')
	
	print(_(u'Loading skin "%s"...' % str(Global.skin_folder)))

class Skin:
	
	def __init__(self):
		
		self.defconfig = SafeConfigParser()
		self.defconfig.readfp(open(default_file))				
		
		self.config = SafeConfigParser()
		self.config.readfp(open(Global.skin_file))	
		
		Global.skin_folder = Global.skin_folder

		fontname = self.search_font_name('')
		if fontname != '':
			set_default_font(fontname)
	
	def set_domain(self, domain):
		self.domain = domain
	
	def configGet(self, field, domain = None, type = None):
		
		if not domain:
			domain = self.domain
		
		if self.config.has_section(domain) and self.config.has_option(domain, field):
			conf = self.config
		elif self.defconfig.has_section(domain) and self.defconfig.has_option(domain, field):
			conf = self.defconfig
		else:
			conf = None
		
		if conf:
			if type == bool:
				value = conf.getboolean(domain, field)
			elif type == int:
				value = conf.getint(domain, field)
			elif type == float:
				value = conf.getfloat(domain, field)
			else:
				value = conf.get(domain, field)
		else:
			value = 0
		
		return value
	
	def configGetInt(self, field, domain = None):	
		return self.configGet(field, domain, type = int)
	
	def configGetFloat(self, field, domain = None):	
		return self.configGet(field, domain, type = float)
	
	def configGetBool(self, field, domain = None):
		return self.configGet(field, domain, type = bool)

	def configGetEval(self, field, domain = None):
		toeval = self.configGet(field, domain)
		return eval(str(toeval))

	def configGetRGB(self, field, domain = None):	
		return self.configGetEval(field, domain)
	
	def directLoadImage(self, name):
		
		fullname = os.path.join(Global.skin_folder, name)

		if os.path.exists(fullname):
			retval = load_image(fullname)
		else:
			retval = load_image(name)
		
		return retval

	def LoadImage(self, field, domain = None):
		
		return self.directLoadImage(self.configGet(field, domain))

	
	def LoadImageRange(self, name, maxrange, digits, domain = None):
		
		torna = list(range(0, maxrange))
		pos = self.configGet(name, domain)
		
		for num in range(0, 64):
			torna[num] = load_image(pos + str(num).zfill(digits) + '.png')
		
		return torna
	
	def LoadSound(self, name, volume, music = 0, domain = None):
		
		name = self.configGet(name, domain)
		volume = self.configGetFloat(volume, domain)
		
		fullname = os.path.join(Global.skin_folder, name)
		
		if os.path.isfile(fullname):
			name = fullname
		
		return load_sound(name, volume = volume, music = music)

	def preguntadorCarregaFiguretes(self, joc, selcat):
		self.mostra_punt_de_categoria = True
		self.figureta_no = load_image('points/freevial_tot' + str(joc.teams[joc.current_team].figureta).zfill(2) + '.png')
		self.figureta_si = load_image('points/freevial_tot' + str(joc.teams[joc.current_team].figureta | bitCategoria (selcat)).zfill(2) + '.png')
		self.match_point = joc.teams[joc.current_team].figureta | bitCategoria (selcat) == 63

	def search_font_name(self, nomfont):

		if nomfont == '':
			nomfont = self.configGet('default_font', 'game')

		if nomfont != '':
			if not os.path.exists(nomfont):
				fullname = os.path.join(str(Global.skin_folder), nomfont)

				if os.path.exists(fullname):
					nomfont = fullname

		return nomfont

	def render_text(self, cadena, color, mida, antialias = 0, nomfont = '', maxwidth = 0):

		nomfont = self.search_font_name(nomfont)

		return render_text(cadena, color, mida, antialias, nomfont, maxwidth)		

	def winning_team(self, teams, force=False):
	
		return winning_team(teams, self.configGetInt('game_mode', 'game'),
			self.configGetInt('game_limit', 'game'), force=force)
