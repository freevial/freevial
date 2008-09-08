# -*- coding: utf-8 -*-

#
# Freevial
# DBUS Service
#
# Copyright (C) 2008 The Freevial Team
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

# WIP - WIP - WIP - WIP - WIP

from common.globals import Global

class Example( dbus.service.Object ):
	
	interface = 'net.freevial.Freevial'
	
	def __init__( self, object_path ):
		dbus.service.Object.__init__( self, Global.session_bus, object_path )
	
	@dbus.service.method( dbus_interface=self.interface, in_signature='v', out_signature='s' )
	def StringifyVariant( self, variant ):
		return 'Hey'
