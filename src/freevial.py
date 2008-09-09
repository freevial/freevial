# -*- coding: utf-8 -*-

#
# Freevial
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
import pygame
import gettext
from optparse import OptionParser

from common.globals import GlobalVar, Global
from common.freevialglob import *
from questions import get_databases
from skinner import setSkinName, Skin
from score import Score
from preguntador import Preguntador
from roda import Roda

gettext.install('freevial', '/usr/share/locale', unicode=1)

# Version information
VERSION = 'UNRELEASED'
SERIES = 'gresca'

class Freevial:
	
	def __init__( self ):
		
		Global.game = GlobalVar()
		
		Global.game.screen = ''
		Global.game.rounds = 0
		
		Global.game.teams = []
		
		Global.game.current_team = 0
		Global.game.sfc_credits = ''
	
	
	def inici( self ):
		
		# inicialize presentation surface
		Global.game.screen = pygame.display.set_mode( ( Global.screen_x, Global.screen_y))
		pygame.display.set_caption('Freevial')
		pygame.display.set_icon( loadImage('freevial.png') )
		
		if not Global.DEBUG_MODE:
			
			pygame.mouse.set_visible( False )
			
			if Global.FULLSCREEN_MODE:
				pygame.display.toggle_fullscreen()
		
		# Initialize sound system
		if not (Global.SOUND_MUTE and Global.MUSIC_MUTE):
			try:
				pygame.mixer.pre_init(44100, -16, 2, 2048)
				pygame.mixer.init()
			except pygame.error, message:
				print _('Sound initialization failed. %s' % message)
				Global.SOUND_MUTE = True
				Global.MUSIC_MUTE = True
		
		pygame.font.init()
		
		Global.game.sfc_credits = createHelpScreen( 'credits', alternate_text = True )
		
		initTextos()
		
		# initialize joystick, if there's one
		pygame.joystick.init()
		if pygame.joystick.get_count():
			pygame.joystick.Joystick( 0 ).init()
		
		# initialize skin system
		Global.game.skin = Skin()
		Global.game.max_teams = Global.game.skin.configGetInt( 'max_teams', domain='game' )
		for num in range( 0, Global.game.max_teams ): Global.game.teams.append( Equip() )
	
	
	def juguem( self ):
		
		self.inici()
		
		score = wheel = question = None
		
		if Global.PRELOAD:
			score = Score( Global.game )
			wheel = Roda( Global.game )
			question = Preguntador( Global.game )
		
		while 1:
			
			if not score:
				score = Score( Global.game )
			Global.game.current_team = score.juguem()
			
			if Global.game.current_team != -1:
				
				Global.game.rounds += 1		
				
				if not wheel:
					wheel = Roda( Global.game )
				resultat = wheel.juguem( )
				
				if resultat != -1:
						
					Global.game.teams[ Global.game.current_team ].preguntes_tot[ resultat - 1 ] += 1		
					
					if not question:
						question = Preguntador( Global.game )
					resultat = question.juguem( resultat )	
					
					if resultat > -1:
						Global.game.teams[ Global.game.current_team ].preguntes_ok[ resultat - 1 ] += 1
						Global.game.teams[ Global.game.current_team ].punts += 1
						
						fig_abans = Global.game.teams[ Global.game.current_team ].figureta
						Global.game.teams[ Global.game.current_team ].activaCategoria( resultat ) 
						
						if fig_abans != 63 and Global.game.teams[ Global.game.current_team ].figureta == 63:
							Global.game.teams[ Global.game.current_team ].punts += 2
					else:
						Global.game.teams[ Global.game.current_team ].errors += 1
					
					Global.game.current_team = seguentEquipActiu( Global.game.teams, Global.game.current_team )
			else:
				sys.exit()

version_string = _(u"""
Freevial, a trivia platform for use on community events.

You are running version %(version)s, which is part of the «%(series)s» series.

https://launchpad.net/freevial/%(series)s

"""  % {'version': VERSION, 'series': SERIES})

optParser = OptionParser(
	usage = _('Usage: %prog [options]'),
	version = version_string,
	)
optParser.add_option(
	'-d', '--debug',
	action='store_false', dest = 'debug',
	help = _('debug mode'),
	)
optParser.add_option(
	'-f', '--fullscreen',
	action='store_false', dest = 'fullscreen',
	help = _('start in fullscreen mode'),
	)
optParser.add_option(
	'-l', '--locked',
	action='store_false', dest = 'locked',
	help = _('start game in locked mode'),
	)
optParser.add_option(
	'--database',
	dest = 'database',
	help = _('absolute path to the database file / directory'),
	)
optParser.add_option(
	'--real',
	dest = 'real',
	help = _('(do not use this)')
	)
optParser.add_option(
	'--skin',
	dest = 'skin',
	help = _('absolute path to the skin directory'),
	)
optParser.add_option(
	'--no-sound',
	action='store_false', dest = 'no_sound',
	help = _('disable sound'),
	)
optParser.add_option(
	'--no-music',
	action='store_false', dest = 'no_music',
	help = _('disable music'),
	)
optParser.add_option(
	'-m', '--mute',
	action='store_false', dest = 'mute',
	help = _('disable all sounds and music'),
	)
optParser.add_option(
	'--no-media',
	action='store_false', dest = 'no_media',
	help = _('disable media questions'),
	)
optParser.add_option(
	'--fps',
	action='store_false', dest = 'fps',
	help = _('show the framerate on screen'),
	)
optParser.add_option(
	'--dbus',
	action='store_false', dest = 'dbus',
	help = _('enable D-Bus support, to interface with external applications'),
	)
optParser.add_option(
	'--info-db',
	action='store_false', dest = 'info_db',
	help = _('print information about the loaded database and exit'),
	)
optParser.add_option(
	'--preload',
	action='store_false', dest = 'preload',
	help = _('load all images and sounds at startup'),
	)
optParser.add_option(
	'--psyco',
	action='store_false', dest = 'psyco',
	help = _('use psyco, if available (this will use more memory)'),
	)
(options, args) = optParser.parse_args()

if options.database:
	path = os.path.abspath(os.path.join(sys.argv[sys.argv.index( '--real' ) + 1],
		sys.argv[sys.argv.index( '--database' ) + 1]))
	if not os.path.isdir( path ):
		print _('Could not find database "%s"...') % unicode(path, 'utf-8')
		sys.exit( 1 )
	Global.database = path

if '--info-db' in sys.argv or '--info-database' in sys.argv:
	total_categories = 0
	total_questions = 0
	categories = []
	
	for database in get_databases():
		total_categories += 1
		total_questions += len(database)
		categories.append((database.name, len(database)))
	
	print
	print _('Freevial - About the loaded database...\n')
	
	print _('Location:'), os.path.abspath(Global.database)
	print _('Amount of categories:'), total_categories
	print _('Amount of questions:'), total_questions, '\n'
	
	for category in categories:
		print _(u'%(category)s: %(num)s questions' \
			% {'category': category[0], 'num': category[1]})
	print
	
	sys.exit( 0 )

if '-d' in sys.argv or '--debug' in sys.argv:
	Global.DEBUG_MODE = True

if '-l' in sys.argv or '--locked' in sys.argv:
	Global.LOCKED_MODE = True

if '--fullscreen' in sys.argv or '-f' in sys.argv:
	Global.FULLSCREEN_MODE = True

if '--fps' in sys.argv:
	Global.DISPLAY_FPS = True

if '-m' in sys.argv or '--mute' in sys.argv:
	Global.SOUND_MUTE = True
	Global.MUSIC_MUTE = True

if '--no-sound' in sys.argv:
	Global.SOUND_MUTE = True

if '--no-music' in sys.argv:
	Global.MUSIC_MUTE = True

if '--no-media' in sys.argv or (Global.SOUND_MUTE and Global.MUSIC_MUTE):
	Global.DISABLE_MEDIA = True

if '--dbus' in sys.argv:
	try:
		import dbus
	except:
		print _('Error: Couldn\'t find dbus-python.')
		sys.exit( 1 )
	else:
		Global.DBUS = True
		Global.session_bus = dbus.SessionBus()
		import common.dbus

if '--preload' in sys.argv:
	Global.PRELOAD = True

if '--skin' in sys.argv:
	path = os.path.abspath(os.path.join(sys.argv[sys.argv.index( '--real' ) + 1], sys.argv[sys.argv.index( '--skin' ) + 1]))
	setSkinName( path )

print _('Loading database "%s"...' % Global.database)
if len(get_databases()) < 6:
	print _('Error: the database hasn\'t enough categories; at least six are required.')
	sys.exit( 1 )

try:
	if '--psyco' in sys.argv:
		try:
			import psyco
			psyco.profile()
		except ImportError:
			print >> sys.stderr, _('Warning: Could not find psyco.')
	
	joc = Freevial()
	joc.juguem()

except KeyboardInterrupt:
	print _('User requested interrupt.')
	sys.exit( 0 )
