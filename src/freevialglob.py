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

	pantalla = ""
	
	basefolder = '../data'
	
	folders = {
						'base': basefolder,
						'images': os.path.join(basefolder, 'images'),
						'sounds': os.path.join(basefolder, 'sounds'),
						'fonts': os.path.join(basefolder, 'fonts'),
					}
	
	# TODO: Reemplaçar la següent línia per un mètode millor
	equips = ( Equip(), Equip(), Equip(), Equip(), Equip(), Equip() )
	
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
		obj = pygame.mixer.music.load( filename )
	
	if volume != '':
		if not music:
			obj.set_volume( float(volume) )
		else:
			pygame.mixer.music.set_volume( float(volume) )
	
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
	
	return keyname
