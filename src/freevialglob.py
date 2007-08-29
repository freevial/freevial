# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Estructura de dades i funcions globals
#
# Carles 28/08/2007
# RainCT 28/08/2007
#

import os.path, random, re, pygame
from pygame.locals import *

DEBUG_MODE = False

class Equip:
	
	nom = ''
	punts = figureta = 0
	actiu = False
	
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
					}
	
	equips = []
	for num in range(0, 6): equips.append( Equip() )
	equips = tuple(equips)
	
	equip_actual = 0

def loadImage( filename ):
	""" Returns a Surface of the indicated image, which is expected to be in the images folder. """
	
	return pygame.image.load( os.path.join(Freevial_globals.folders['images'], str(filename) )).convert_alpha()


def loadSound( filename, volume = '' , music = 0 ):
	""" Returns a sound object of the indicated audio file, which is expected to be in the sounds folder. """
	
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


def mouseClick( event, request ):
	
	mouseButtons = {
			'primary': 1,
			'secondary': 2,
			'middle': 3,
		}
	
	if type(request) is not int:
		request = mouseButtons[ request ]
	
	if event.type == pygame.MOUSEBUTTONDOWN and event.button == request:
		return True


def render_text( cadena, color, mida, antialias = 0, nomfont = '' ):
	""" Function for easier text rendering. """
	
	if nomfont == '':
		nomfont = os.path.join(Freevial_globals.folders['fonts'], 'lb.ttf')
	
	font1 = pygame.font.Font( nomfont, mida )
	return font1.render( cadena, antialias, color )


def shuffleQuestions( questions ):
	""" Returns the given questions list, but shuffled. """
	
	for num in range(0, 6):
		random.shuffle( questions[num] )
	
	return questions


def maxPunts( equips ):

	puntsmax = 0

	for compta in range(0,6):
		if equips[compta].actiu:
			puntsmax = max( puntsmax, equips[compta].punts )
	
	return puntsmax

def puntsTotals( equips ):

	punts = 0

	for compta in range(0,6):
		punts += equips[compta].punts
	
	return punts

def equipsActius( equips ):

	actius = 0

	for compta in range(0,6):
		if equips[compta].actiu: actius += 1
	
	return actius


def seguentEquipActiu( equips, actual ):

	actual += 1

	for compta in range(0,6):
		if equips[(actual + compta) % 6].actiu: 
			return (actual + compta) % 6
	
	return -1


def anteriorEquipActiu( equips, actual ):

	actual -= 1

	for compta in range(0,6):
		if equips[(actual - compta ) % 6].actiu: 
			return (actual - compta ) % 6
	
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

def createHelpScreen( help_string ):
	""" Creates a help overlay surface based on a help string list. """

	help_overlay = pygame.Surface( ( 1024, 768), pygame.SRCALPHA, 32 )
	
	for compta in range( 0, 10):
		#self.help_overlay.fill( (0,0,16,200), ( 100, 100, 1024 - 100 * 2, 768 - 150) )
		help_overlay.fill( (0,0,16,compta * 25), ( 100 + (compta*2), 100+ (compta*2), 1024 - 100 * 2 - (compta * 4), 768 - 150 - (compta *4)) )

	nlinia = 0

	for cadena in help_string:
		text_pregunta = render_text( cadena, (0,0,0), 30, 1 )
		help_overlay.blit( text_pregunta, (150 + 2, 35 * nlinia + 152))

		text_pregunta = render_text( cadena, (255,255,0), 30, 1 )
		help_overlay.blit( text_pregunta, (150, 35 * nlinia + 150))

		nlinia += 1

	return help_overlay

