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

import os.path, random, re, pygame, locale, time
from pygame.locals import *
from preguntes import preguntes_autors

DEBUG_MODE = False
SOUND_MUTE = False
MUSIC_MUTE = False
DISPLAY_FPS = False

LOCKED_MODE = False

textos = []


class Equip:
	
	nom = ''
	punts = 0
	figureta = 0
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


def mute( sound = None, music = None ):
	""" Mute sound or music. """
	
	global SOUND_MUTE, MUSIC_MUTE
	
	if sound: SOUND_MUTE = sound
	if music: MUSIC_MUTE = music
	
	return {
			'sound': SOUND_MUTE,
			'music': MUSIC_MUTE,
		}


def ismute():
	return SOUND_MUTE and MUSIC_MUTE


def loadImage( name, colorkey = None, rotate = 0 ):
	""" Returns a Surface of the indicated image, which is expected to be in the images folder. """
	
	fullname = os.path.join(Freevial_globals.folders['images'], str(name))
	
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Failed loading image: ', fullname
		raise SystemExit, message
	
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image = image.convert()
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	else:
		image = image.convert_alpha()
	
	if rotate != 0:
		image = rotateImage(image, rotate)
	
	return image	# [ image, image.get_rect()


def loadSound( name, volume = 1.0, music = False ):
	""" Returns a sound object of the indicated audio file, which is expected to be in the sounds folder. """
	
	if ( mute()['music'] and music ) or ( mute()['sound'] and not music ) or not pygame.mixer or not pygame.mixer.get_init():
	
		class NoneSound:
			def load( *args ): pass
			def play( *args ): pass
			def stop( *args ): pass
			def set_volume( *args ): pass
		
		return NoneSound()
	
	fullname = os.path.join(Freevial_globals.folders['sounds'], name)
	
	try:
		if not music:
			obj = pygame.mixer.Sound(fullname)
		else:
			obj = pygame.mixer.music
			obj.load(fullname)
	except pygame.error, message:
		
		print 'Failed loading sound: ', fullname
		
		if not music:
			raise SystemExit, message
	
	obj.set_volume(float(volume))
	
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


def render_text( cadena, color, mida, antialias = 0, nomfont = '', maxwidth = 0 ):
	""" Function for easier text rendering. """

	nomfont = os.path.join(Freevial_globals.folders['fonts'], 'lb.ttf' if nomfont == '' else nomfont)
	
	font1 = pygame.font.Font( nomfont, mida )
	
	text_restant = cadena
	sfc = None

	if maxwidth:
		sfcs = []

		while text_restant != "":

			ample = maxwidth + 1
			escriure = text_restant

			while ample > maxwidth:

				sfc = font1.render( escriure, antialias, color )
				ample = sfc.get_width()		
			
				if ample > maxwidth:
					tpos = escriure.rfind( ' ' )
					if tpos == -1:
						ample = maxwidth
					else:
						escriure = escriure[0:tpos]		

			sfcs.append( sfc )

			text_restant = text_restant[ len( escriure )+1:]

		if len(sfcs) > 1:
			iample = 0
			ialt = 0
			for compta in range( 0, len(sfcs) ):
				ialt += max(sfcs[compta].get_height(), mida)
				iample = min(maxwidth, max( iample, sfcs[compta].get_width() ))

			sfc = pygame.Surface( ( iample, ialt), pygame.SRCALPHA, 32 )

			pos = 0
			for compta in range( 0, len(sfcs) ):
				sfc.blit( sfcs[compta], (0, pos) )
				pos += max(sfcs[compta].get_height(), mida)

		else:
			sfc = sfcs[0] if len(sfcs) == 1 else None
	else:
		sfc = font1.render( cadena, antialias, color )

	return sfc

def screenshot( surface, destination = os.path.join( os.path.expanduser('~'), 'Freevial/Screenshots/' ) ):
	""" Save a screenshot of the indicated surface. """
	
	destination = os.path.normpath( destination )
	
	if not os.path.exists( destination ):
		os.makedirs( destination )
	
	#PNG, JPEG saving new in pygame 1.8.
	destination = os.path.join( destination, str( time.time() ) + '.tga' )
	
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

	if equipsTancat( equips ):

		for num in range(0,6):
			if equips[num].actiu:
				if equips[num].punts == puntsmax:
					# empat a punts
					equipmax = -1 

				if equips[num].punts > puntsmax:
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

aobert = atancat = adieresi = acirc = False
accents = [u"aeiou", u"àèìòù", u"áéíóú", u"äëïöü", u"âêîôû" ]

def printKey( tecla ):
	""" Translates a pygame Key object for on-game printing of it's value. """

	global aobert, atancat, adieresi, acirc, accents
	
	keyname = pygame.key.name( tecla )

	if keyname == 'space': 
		return ' '
	
	if keyname == 'world 71':
		return u'ç'
	
	if keyname == 'tab':
		return '    '
	
	if len(keyname) == 3 and keyname[:1] == '[' and keyname[2:] == ']':
		keyname = keyname[1:2]
	
	pos = accents[0].find( keyname )
	if pos != -1:
		if aobert: keyname = accents[1][pos]
		if atancat: keyname = accents[2][pos]
		if adieresi: keyname = accents[3][pos]
		if acirc: keyname = accents[4][pos]

	if pygame.key.get_mods() & pygame.KMOD_SHIFT:
		keyname = keyname.upper()

	if tecla == 314:
		print 314
		if pygame.key.get_mods() & pygame.KMOD_SHIFT:
			atancat = True
		elif pygame.key.get_mods() & pygame.KMOD_CTRL:
			adieresi = True
		elif pygame.key.get_mods() & pygame.KMOD_ALT:
			acirc = True
		else:
			aobert = True
	else:
		aobert = atancat = adieresi = acirc = False

	if not re.search(u"^[a-zA-Z0-9,.+'-/*àèìòùáéíóúäëïöüâêîôû ]$", keyname):
		return ''

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

	pos = 0
	for line in frases:
		if line != "":	
			text_pregunta = render_text( line, (0,0,0), font_size, 1, '', 700 )
			help_overlay.blit( text_pregunta, (150 + 2, pos + 142))
			
			text_pregunta = render_text( line, color, font_size, 1, '', 700 )
			help_overlay.blit( text_pregunta, (150, pos + 140))
			
			pos += text_pregunta.get_height()
		else:
			pos += 	font_size	

		nline += 1
	
	return help_overlay


def replaceKeywoards( content ):
	""" Replaces keywoards found in the content a help file. """

	for num in range(0, len(content)):
		content[num] = unicode(content[num], 'utf-8')

	i = 0
	for line in content:
		
		if line.startswith( '##replace:question-authors' ):
			#content[ i : (i + 1) ] = list2string( preguntes_autors )
			content[ i : (i + 1) ] = preguntes_autors()

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
		
		lines.append ( line )
	
	return lines


def createHelpScreen( help_section, alternate_text = False ):
	""" Creates a help overlay surface based on a help file. """
	
	return createTextSurface( readLocalizedHelpFile( help_section ), (0, 255, 255) if alternate_text else (255, 255, 0) )

i_colors_cat = ( (0,0,255), (255,128,0), (0,255,0),(255,0,0),(255,0,255), (255,255,0) )


def initTextos():
	global textos

	textos = readLocalizedHelpFile( "textos" )


def valorText( ntext ):
	return textos[ ntext ]




def colorsCategories():

	return i_colors_cat


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
HOS_NEW_GAME = 10


class helpOnScreen():
	
	text = ''
	scf_text = None
	sec_darrera_activitat = -1
	sec_timeout = 10

	intensitat = 5
	
	
	def __init__( self, itext ):
		
		self.creaTextdeTextos ( itext )
		self.sec_darrera_activitat = time.time()	
	
	
	def creaTextdeTextos(self, itext ):
		
		global textos
		self.creaText( textos[itext] )
	
	
	def creaText( self, ptext ):
		
		if self.text != ptext :
			self.text = ptext
			self.sfc_text = render_text( self.text, (128,128,128), 15, 1 )
	
	
	def draw( self, surface, pos, itext = None ):
		
		if time.time() >= self.sec_darrera_activitat + self.sec_timeout :
			
			if itext: self.creaTextdeTextos ( itext )
			surface.blit( self.sfc_text, pos )
	
	
	def activitat( self, event = None ):
		
		if not event or event.type == pygame.KEYUP :
			self.sec_darrera_activitat = time.time()


def displayFPS( display = '' ):
	""" Displays or hides the frame rate from screen. """
	
	global DISPLAY_FPS
	
	if display != '': DISPLAY_FPS = display
	
	return DISPLAY_FPS


class frameRate():
	""" Calculates the frame rate (FPS), limits it and, if choosen so, displays it on screen. """
	
	seconds = fps = fps_current = fps_limit = lastTicks = t_inici = 0
	textSurface = None
	
	def __init__( self, fps_limit = 0 ):
		self.fps_limit = fps_limit
		self.lastTicks = pygame.time.get_ticks()
		self.t_inici = time.time()
	
	def segons( self ):
		return time.time() - self.t_inici

	def next( self, surface = None ):
		
		if time.time() > self.seconds + 1:
			self.seconds = time.time()
			self.fps = self.fps_current
			self.fps_current = 0
			if DISPLAY_FPS:
				self.textSurface = render_text( 'FPS: ' + str( self.fps if self.fps > 0 else 'N/a' ), (128, 128, 128), 15, 1 )
		else:
			self.fps_current += 1
		
		limit_fps = 1000 / self.fps_limit
		limit_ticks = pygame.time.get_ticks() - self.lastTicks
		
		if limit_ticks < limit_fps:
			pygame.time.wait( limit_fps - limit_ticks )
			self.lastTicks = pygame.time.get_ticks()

		if surface:	
			if self.textSurface and DISPLAY_FPS:
				# display the frame rate on the middle of the screen's bottom
				#surface.blit( self.textSurface, ( (( Freevial_globals.mida_pantalla_x / 2 ) - ( self.textSurface.get_width() / 2 )), 740 ) )
				surface.blit( self.textSurface, (250, 740 ) )

Jstick = None

# Alies per comandament tipus PS2
j_alias = { 0: K_RETURN, 1: K_ESCAPE, 2: K_RETURN, 8: K_SPACE, 12: K_UP, 13: K_RIGHT, 14: K_DOWN, 15: K_LEFT, 9: K_ESCAPE, 3: K_s, 7: K_F3, 6: K_F1, 4: K_F2, 5: K_a}

def init_joystick():

	pygame.joystick.init ()

	if pygame.joystick.get_count():
		Jstick = pygame.joystick.Joystick( 0 )
		Jstick.init()

def translateJoystickEvent( event ):

	alies = j_alias.get( event.button )
	if alies:
		event = pygame.event.Event( pygame.KEYUP, {'key': alies, 'unicode': u's', 'mod': 0})
		pygame.event.post( event )

def setLockedMode( mode ):

	global LOCKED_MODE

	LOCKED_MODE = mode


def getLockedMode( ):

	global LOCKED_MODE

	return LOCKED_MODE

