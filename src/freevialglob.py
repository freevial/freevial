# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Estructura de dades globals
#
# Carles 24/08/2007
# RainCT 27/08/2007
#

import os.path

class Freevial_globals:
	
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
