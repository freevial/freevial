# -*- coding: utf-8 -*-

#
# Freevial
# Global Data and Functions
#
# Copyright (C) 2007 The Freevial Team
#
# By Carles Oriol i Margarit <carles@kumbaworld.com>
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
#GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os.path, random, re, pygame, locale
import time
from pygame.locals import *
from preguntes import preguntes_autors


DEBUG_MODE = False
SOUND_MUTE = False
MUSIC_MUTE = False

textos = []

class Equip:
	
	nom = ''
	punts = figureta = 0
	actiu = False

	sfc_nom = None

	def __init__( self ):

		self.preguntes_tot = []
		self.preguntes_ok = []

		for num in range(0, 6): 
			self.preguntes_tot.append( 0 )
			self.preguntes_ok.append( 0 )

		

	def canviaCategoria( self, categoria ):
		# Les tenim desendreçades i això ho complica una mica
		self.figureta ^= bitCategoria( categoria )


	def activaCategoria( self, categoria ):
		# Les tenim desendreçades i això ho complica una mica
		self.figureta |= bitCategoria( categoria )


	def teCategoria( self, categoria ) :
		return (self.figureta & bitCategoria( categoria )) != 0


def bitCategoria ( categoria ):
	if categoria == 6: return 0x1
	if categoria == 5: return 0x2
	if categoria == 1: return 0x4
	if categoria == 2: return 0x8
	if categoria == 4: return 0x10
	if categoria == 3: return 0x20


class Freevial_globals:
	""" Contains all variables that are commonly used by all components of Freevial. """
	
	mida_pantalla_x = 1024
	mida_pantalla_y = 768
	Limit_FPS = 40

	pantalla = ''
	rondes = 0
	
	basefolder = '../data'
	
	folders = {
						'base': basefolder,
						'images': os.path.join(basefolder, 'images'),
						'sounds': os.path.join(basefolder, 'sounds'),
						'fonts': os.path.join(basefolder, 'fonts'),
						'help': os.path.join(basefolder, 'help'),
					}
	
	equips = []
	for num in range(0, 6): equips.append( Equip() )
	equips = tuple(equips)
	
	equip_actual = 0

	sfc_credits = ""


def mute( sound = '', music = '' ):
	""" Mute sound or music. """
	
	global SOUND_MUTE, MUSIC_MUTE
	
	if sound != '': SOUND_MUTE = sound
	if music != '': MUSIC_MUTE = music
	
	return {
			'sound': SOUND_MUTE,
			'music': MUSIC_MUTE,
		}


def loadImage( filename ):
	""" Returns a Surface of the indicated image, which is expected to be in the images folder. """
	
	return pygame.image.load( os.path.join(Freevial_globals.folders['images'], str(filename) )).convert_alpha()


def loadSound( filename, volume = '' , music = 0 ):
	""" Returns a sound object of the indicated audio file, which is expected to be in the sounds folder. """
	
	if ( mute()['music'] and music ) or ( mute()['sound'] and not music ) :
		
		class voidClass:
			def load( var ): pass
			def set_volume( var, var2 = '' ): pass
			def play( var, var2 = '' ): pass
			def stop( var ): pass
		
		return voidClass()
	
	filename = os.path.join(Freevial_globals.folders['sounds'], str(filename))
	
	if not music:
		obj = pygame.mixer.Sound( filename )
	else:
		obj = pygame.mixer.music
		obj.load( filename )
	
	if volume != '':
		obj.set_volume( float(volume) )
	
	return obj


def keyPress( event, keys ):
	""" Returns true if the given event is the release of one of the indicated keys. 
	Just a key can be passed or a whole bunch inside a tuple, and in both cases they may be 
	either a string or directly it's pygame object. """
	
	if type(keys) is str or type(keys) is int:
		keys = ( keys, )
	
	# Check if any of the indicated keys matches
	found = 0
	for key in keys:
		
		if key[:2] != 'K_':
			key = 'K_' + key
		
		if type(key) is str:
			key = getattr(pygame, key)
		
		if event.type == pygame.KEYUP and event.key == key:
			found = 1
	
	return True if found == 1 else False


mouseButtons = {
		'primary': 1,
		'secondary': 2,
		'middle': 3,
	}


def mouseClick( event, request = 0 ):
	
	global mouseButtons
	
	if type(request) is not int:
		request = mouseButtons[ request ]
	
	if event.type == pygame.MOUSEBUTTONDOWN and (event.button == request or request == 0):
		return True


def mouseRelease( event, request = 0 ):
	
	global mouseButtons
	
	if type(request) is not int:
		request = mouseButtons[ request ]
	
	if event.type == pygame.MOUSEBUTTONUP and (event.button == request or request == 0):
		return True


def render_text( cadena, color, mida, antialias = 0, nomfont = '' ):
	""" Function for easier text rendering. """
	
	if nomfont == '':
		nomfont = os.path.join(Freevial_globals.folders['fonts'], 'lb.ttf')
	
	font1 = pygame.font.Font( nomfont, mida )
	return font1.render( cadena, antialias, color )


def screenshot( surface, destination = os.path.join( os.path.expanduser('~'), 'Freevial/Screenshots/' ) ):
	""" Save a screenshot of the indicated surface. """
	
	destination = os.path.normpath( destination )
	
	if not os.path.exists( destination ):
		os.makedirs( destination )
	
	def nextFileNum( directory ):
		files = os.listdir( directory )
		files.sort()
		fileNum = ( int( str.split(files[-1], '.')[0] ) if len(files) > 0 else 0 ) + 1
		return fileNum
	
	destination = os.path.join( destination, str( nextFileNum( destination ) ) + '.png' )
	
	pygame.image.save( surface, destination )


def maxPunts( equips ):

	puntsmax = 0

	for num in range(0,6):
		if equips[num].actiu:
			puntsmax = max( puntsmax, equips[num].punts )
	
	return puntsmax


def puntsTotals( equips ):

	punts = 0

	for num in range(0,6):
		punts += equips[num].punts
	
	return punts


def equipsActius( equips ):

	actius = 0

	for num in range(0,6):
		if equips[num].actiu: actius += 1
	
	return actius


def equipsTancat( equips ):

	for num in range(0,6):
		if equips[num].figureta == 63:
			return True
	
	return False


def equipsGuanyador( equips ):

	puntsmax = 0
	equipmax = -1

	if( equipsTancat( equips )):

		for num in range(0,6):
			if equips[num].actiu:
				if( equips[num].punts == puntsmax ):
					# empat a punts
					equipmax = -1 

				if( equips[num].punts > puntsmax ):
					equipmax = num
					puntsmax = equips[num].punts
	
	return equipmax


def seguentEquipActiu( equips, actual ):

	actual += 1

	for num in range(0,6):
		if equips[(actual + num) % 6].actiu: 
			return (actual + num) % 6
	
	return -1


def anteriorEquipActiu( equips, actual ):

	actual -= 1

	for num in range(0,6):
		if equips[(actual - num ) % 6].actiu: 
			return (actual - num ) % 6
	
	return -1

anterior = ""


def printKey( tecla ):
	""" Translates a pygame Key object for on-game printing of it's value. """
	
	keyname = pygame.key.name( tecla )
	
	if keyname == 'space': 
		return ' '
	
	if keyname == 'world 71':
		return u'ç'
	
	if keyname == 'tab':
		return '    '
	
	if len(keyname) == 3 and keyname[:1] == '[' and keyname[2:] == ']':
		keyname = keyname[1:2]
	
	if not re.search("^[a-zA-Z0-9,.+'-/* ]$", keyname):
		return ''
	
	if pygame.key.get_mods() & pygame.KMOD_SHIFT:
		keyname = keyname.upper()

	return keyname


def list2string( list, wordsEachLine = 5, lineEnd = ',' ):
	""" Converts a list of words into a list of comma-separated string with 'wordsEachLine' words. """
	
	lines = []
	string = ''
	i = 0
	
	for author in list:
		
		if string != '':
			string += ', '
		
		string += author
		
		if (wordsEachLine - 1) == (i % wordsEachLine):
			lines.append( str(string + lineEnd) )
			string = ''

		i += 1
		
	if string != '':
		lines.append( str(string + lineEnd) )
	
	lines[-1] = lines[-1][:-len(lineEnd)]
	
	return lines


def createTextSurface( frases, color, intensitat = 25 ):
	""" Creates a help overlay surface and prints the passed text on it. """
	
	font_step = (768 - (315)) / len(frases) 
	font_step = min( font_step, 25 )

	font_size = font_step - (font_step * 10) / 100
 
	help_overlay = pygame.Surface( ( 1024, 768), pygame.SRCALPHA, 32 )
	
	for num in range( 0, 10):
		help_overlay.fill( (0, 0, 16, num * intensitat), ( 100 + (num * 2), 100 + (num * 2), 1024 - 100 * 2 - (num * 4), 768 - 150 - (num * 4)) )
	
	nline = 0
	for line in frases:
		
		text_pregunta = render_text( line, (0,0,0), font_size, 1 )
		help_overlay.blit( text_pregunta, (150 + 2, (font_step + 5) * nline + 142))
		
		text_pregunta = render_text( line, color, font_size, 1 )
		help_overlay.blit( text_pregunta, (150, (font_step + 5) * nline + 140))
		
		nline += 1
	
	return help_overlay


def replaceKeywoards( content ):
	""" Replaces keywoards found in the content a help file. """
	
	i = 0
	
	for line in content:
		
		if line.startswith( '##replace:question-authors' ):
			content[ i : (i + 1) ] = list2string( preguntes_autors )
	
		i += 1
	
	return content


def readLocalizedHelpFile( help_section ):
	""" Reads a localized file into an unicoded array. """
	
	filename = os.path.join(Freevial_globals.folders['help'], (help_section + "_"+ locale.getdefaultlocale()[0][:2] +'.txt'))
	
	if not os.path.exists (filename):
		filename = os.path.join(Freevial_globals.folders['help'], (help_section + '.txt'))
	
	lines = []
	
	for line in replaceKeywoards(open( filename, 'r' ).readlines()):
		
		# skip comments
		#if line[:1] == '#': continue
		
		lines.append ( unicode(line, 'utf-8') )
	
	return lines


def createHelpScreen( help_section, alternate_text = False ):
	""" Creates a help overlay surface based on a help file. """
	
	return createTextSurface( readLocalizedHelpFile( help_section ), (0, 255, 255) if alternate_text else (255, 255, 0) )

def initTextos():
	global textos
	textos = readLocalizedHelpFile( "textos" )


HOS_SCORE_MODE0 = 0
HOS_SCORE_MODE1 = 1
HOS_SCORE_MODE2 = 2
HOS_QUIT = 3
HOS_YES = 4
HOS_NO = 5
HOS_PREGUNTADOR_RUN = 6
HOS_PREGUNTADOR_END = 7
HOS_SCORE_MODEW = 8
HOS_RODA_ATURA = 9


class helpOnScreen():
	
	text = ""
	scf_text = None
	sec_darrera_activitat = -1
	sec_timeout = 3

	intensitat = 5

	def __init__( self, itext ):

		self.creaTextdeTextos ( itext )
		sec_darrera_activitat = time.time()	

	def creaTextdeTextos (self, itext ):

		global textos
		self.creaText( textos[itext] )

	def creaText ( self, ptext ):

		if self.text != ptext :
			self.text = ptext
			self.sfc_text = render_text( self.text, (128,128,128), 15, 1 )

	def draw ( self, surface, pos, itext = None ):

		if time.time() >= self.sec_darrera_activitat + self.sec_timeout :

			if itext: self.creaTextdeTextos ( itext )
			surface.blit( self.sfc_text, pos )

	def activitat( self, event = None ):

		if not event or event.type == pygame.KEYUP :
			self.sec_darrera_activitat = time.time()




