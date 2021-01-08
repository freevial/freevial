# -*- coding: utf-8 -*-
 
#
# Freevial
# Preferences
#
# Copyright (C) 2009 The Freevial Team
#
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

import os.path
import gettext
from configparser import SafeConfigParser, NoOptionError, NoSectionError
from xdg import BaseDirectory

from common.globals import GlobalVar

class Preferences(GlobalVar):
	
	settings = {
		# section
		'questions': (
			# settings_name, section, type, default
			('special_answers', 'special_answers', 'boolean', False),
		),
	}
	
	def __init__(self, filename=None):
		
		if not filename:
			if BaseDirectory.load_first_config('freevial'):
				filename = os.path.join(
					BaseDirectory.load_first_config('freevial'),
					'preferences.ini')
			else:
				filename = ''
		
		self._config = None
		if os.path.isfile(filename):
			print(_(u'Loading configuration file "%s"...' % filename))
			self._config = SafeConfigParser()
			self._config.readfp(open(filename))
		
		for section in self.settings:
			for element in self.settings[section]:
				# Set the default value
				setattr(self, element[0], element[3])
				# Check if the user has overriden it
				self.set_setting(section, element[1], element[2], element[0])
	
	def set_setting(self, section, option, type, setting_name):
		if self._config and self._config.has_section(section) and \
		self._config.has_option(section, option):
			parser = getattr('config.get' + type)
			setattr(self, setting_name, parser(section, option))
