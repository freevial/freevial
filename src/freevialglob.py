# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Estructura de dades globals
#
# Carles 24/08/2007
# RainCT 27/08/2007
#

import os.path, pygame
from pygame.locals import *


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


def loadImage( filename ):
	""" Returns a Surface of the indicated image, which is expected to be in the images folder. """
	
	return pygame.image.load( os.path.join(Freevial_globals.folders['images'], str(filename) ))


def loadSound( filename, volume = '' ):
	""" Returns a sound object of the indicated audio file, which is expected to be in the sounds folder. """
	
	obj = pygame.mixer.Sound( os.path.join(Freevial_globals.folders['sounds'], str(filename) ))
	
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
