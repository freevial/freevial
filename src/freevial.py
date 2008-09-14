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
		pygame.display.set_icon( load_image('freevial.png') )
		
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
				print >> sys.stderr, _('Sound initialization failed. %s' % message)
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
		for num in xrange( 0, Global.game.max_teams ):
			Global.game.teams.append( Equip(num) )
	
	
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
						Global.game.teams[ Global.game.current_team ].points += 1
						
						fig_abans = Global.game.teams[ Global.game.current_team ].figureta
						Global.game.teams[ Global.game.current_team ].activaCategoria( resultat ) 
						
						if fig_abans != 63 and Global.game.teams[ Global.game.current_team ].figureta == 63:
							Global.game.teams[ Global.game.current_team ].points += 2
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
	action = 'store_true', dest = 'debug',
	help = _('debug mode'),
	)
optParser.add_option(
	'-f', '--fullscreen',
	action = 'store_true', dest = 'fullscreen',
	help = _('start in fullscreen mode'),
	)
optParser.add_option(
	'-l', '--locked',
	action = 'store_true', dest = 'locked',
	help = _('start game in locked mode'),
	)
optParser.add_option(
	'--lang', '--languages',
	dest = 'languages',
	help = _('only load those questions written in the indicated language(s); '
			'for example, "ca, en"'),
	)
optParser.add_option(
	'--database',
	dest = 'database', metavar='PATH',
	help = _('path to the database file / directory you want to append to the '
		'default database'),
	)
optParser.add_option(
	'--real',
	dest = 'real', metavar='PATH',
	help = _('(do not use this)')
	)
optParser.add_option(
	'--skin',
	dest = 'skin', metavar='PATH',
	help = _('absolute path to the skin directory'),
	)
optParser.add_option(
	'--no-sound',
	action = 'store_true', dest = 'no_sound',
	help = _('disable sound'),
	)
optParser.add_option(
	'--no-music',
	action = 'store_true', dest = 'no_music',
	help = _('disable music'),
	)
optParser.add_option(
	'-m', '--mute',
	action = 'store_true', dest = 'mute',
	help = _('disable all sounds and music'),
	)
optParser.add_option(
	'--no-media',
	action = 'store_true', dest = 'no_media',
	help = _('disable media questions'),
	)
optParser.add_option(
	'--fps',
	action = 'store_true', dest = 'fps',
	help = _('show the framerate on screen'),
	)
optParser.add_option(
	'--max-fps',
	dest = 'max_fps', metavar = 'NUM',
	help = _('set the framerate limit (default is %d)' % Global.fps_limit),
	)
optParser.add_option(
	'--dbus',
	action = 'store_true', dest = 'dbus',
	help = _('enable D-Bus support, to interface with external applications'),
	)
optParser.add_option(
	'--info-db', '--info-database',
	action = 'store_true', dest = 'info_db',
	help = _('print information about the loaded database and exit'),
	)
optParser.add_option(
	'--preload',
	action = 'store_true', dest = 'preload',
	help = _('load all images and sounds at startup'),
	)
optParser.add_option(
	'--psyco',
	action = 'store_true', dest = 'psyco',
	help = _('use psyco, if available (this will use more memory)'),
	)
(options, args) = optParser.parse_args()

if options.languages:
	Global.languages = [ x.strip().strip(',').lower() for x in
		options.languages.split() if x]
	for language in Global.languages:
		if len(language) != 2 or not language.isalpha():
			print >> sys.stderr, _('Error: You\'ve indicated an incorrect '
				'language code. Valid examples are: "ca", "en, de", etc.')
			sys.exit( 1 )
	print _(u'Selected languages: %s' % ', '.join(Global.languages))

if options.database:
	path = os.path.abspath(os.path.join(options.real, options.database))
	if not os.path.isdir( path ):
		print _(u'Could not find database "%s"...' % path)
		sys.exit( 1 )
	Global.databases.append(path)

if options.info_db:
	total_categories = 0
	total_questions = 0
	categories = []
	
	for database in get_databases():
		total_categories += 1
		total_questions += len(database)
		categories.append((database.name, len(database)))
	
	print
	print _('Freevial - About the loaded database...\n')
	
	print _('Location:'), '; '.join(Global.databases)
	print _('Amount of categories:'), total_categories
	print _('Amount of questions:'), total_questions, '\n'
	
	categories.sort()
	for category in categories:
		print _(u'%(category)s: %(num)s questions' \
			% {'category': category[0], 'num': category[1]})
	print
	
	sys.exit( 0 )

if options.debug:
	Global.DEBUG_MODE = True

if options.locked:
	Global.LOCKED_MODE = True

if options.fullscreen:
	Global.FULLSCREEN_MODE = True

if options.fps:
	Global.DISPLAY_FPS = True

if options.max_fps:
	if not options.max_fps.isdigit():
		print >> sys.stderr, _('You\'ve given an incorrect value for --max-fps.')
		sys.exit(1)
	Global.fps_limit = int(options.max_fps)

if options.mute:
	Global.SOUND_MUTE = True
	Global.MUSIC_MUTE = True

if options.no_sound:
	Global.SOUND_MUTE = True

if options.no_music:
	Global.MUSIC_MUTE = True

if options.no_media or (Global.SOUND_MUTE and Global.MUSIC_MUTE):
	Global.DISABLE_MEDIA = True

if options.dbus:
	try:
		import dbus
	except:
		print >> sys.stderr, _('Error: Couldn\'t find dbus-python.')
		sys.exit( 1 )
	else:
		Global.DBUS = True
		Global.session_bus = dbus.SessionBus()
		import common.dbus

if options.preload:
	Global.PRELOAD = True

if options.skin in sys.argv:
	path = os.path.abspath(os.path.join(options.real, options.skin))
	setSkinName( path )

if len(get_databases()) < 6:
	print >> sys.stderr, _('Error: couldn\'t find enough categories; '
		'at least six are required.')
	sys.exit( 1 )

try:
	if options.psyco:
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
