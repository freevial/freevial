#!/usr/bin/python
# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
#
# Carles 28/08/2007
# RainCT 27/08/2007
#

import sys, os.path
import pygame, pygame.surfarray
from Numeric import *
from pygame.locals import *

from freevialglob import *
from score import Score
from preguntador import Preguntador
from roda import Roda


##################################################
#
# Classe de control del programa
#

class Freevial:

	###########################################
	#
	def __init__( self ):
	
		self.dades_joc = Freevial_globals()
	
	
	###########################################
	# Iniciem partida
	#
	def inici( self ):
		
		# inicialitzem la superficie de presentació
		self.dades_joc.pantalla = pygame.display.set_mode( ( self.dades_joc.mida_pantalla_x, self.dades_joc.mida_pantalla_y), 0, 32)
		pygame.display.set_caption('Freevial')
		pygame.display.set_icon( pygame.image.load(os.path.join(self.dades_joc.folders['images'], 'logo.png')) )
		
		if not DEBUG_MODE:
			pygame.mouse.set_visible( False )
			pygame.display.toggle_fullscreen()
		
		# inicialitzem els sistemes de so i text
		pygame.mixer.pre_init( 44100 )
		pygame.mixer.init()
		pygame.font.init()
	
	
	###########################################
	#
	# Control principal del programa
	#
	def juguem( self ):
		
		self.inici()

		while 1:
			score = Score( self.dades_joc )
			self.dades_joc.equip_actual = score.juguem()
			
			if self.dades_joc.equip_actual != -1:
				roda = Roda( self.dades_joc )
				resultat = roda.juguem()
				
				if resultat != 0:

					fespregunta = Preguntador( self.dades_joc )
					resultat = fespregunta.juguem( resultat )
					if resultat > 0:
						self.dades_joc.equips[ self.dades_joc.equip_actual].punts += 1
						
						fig_abans = self.dades_joc.equips[ self.dades_joc.equip_actual].figureta
						self.dades_joc.equips[ self.dades_joc.equip_actual].activaCategoria( resultat ) 
				
						if fig_abans != 63 and self.dades_joc.equips[ self.dades_joc.equip_actual].figureta == 63:
							self.dades_joc.equips[ self.dades_joc.equip_actual].punts += 2
						
					self.dades_joc.equip_actual = seguentEquipActiu( self.dades_joc.equips, self.dades_joc.equip_actual )
			else:
				sys.exit()


if '-d' in sys.argv or '--debug' in sys.argv:
	DEBUG_MODE = True

try:
	joc = Freevial()
	joc.juguem()
	
except KeyboardInterrupt:
	print 'Manual abort.'
	sys.exit()
