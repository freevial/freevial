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

