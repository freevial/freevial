#!/usr/bin/python
# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
#
# Carles 28/08/2007
# RainCT 27/08/2007
#

import sys, os.path, pygame
from Numeric import *

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
	
		self.joc = Freevial_globals()
	
	
	###########################################
	# Iniciem partida
	#
	def inici( self ):
		
		# inicialize presentation surface
		self.joc.pantalla = pygame.display.set_mode( ( self.joc.mida_pantalla_x, self.joc.mida_pantalla_y), 0, 32)
		pygame.display.set_caption('Freevial')
		pygame.display.set_icon( pygame.image.load(os.path.join(self.joc.folders['images'], 'logo.png')) )
		
		if not DEBUG_MODE:
			pygame.mouse.set_visible( False )
			pygame.display.toggle_fullscreen()
		
		# inicialize sound and text systems
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.mixer.init()
		pygame.font.init()
		
		self.joc.sfc_credits = createHelpScreen( 'credits', alternate_text = True )
	
	###########################################
	#
	# Control principal del programa
	#
	def juguem( self ):
		
		self.inici()
		
		score = roda = fespregunta = None

		while 1:
			
			if not score: score = Score( self.joc )
			
			self.joc.equip_actual = score.juguem( self.joc )
			
			if self.joc.equip_actual != -1:
				
				self.joc.rondes += 1		
				
				if not roda: roda = Roda( self.joc )
				
				resultat = roda.juguem( self.joc )
				
				if resultat != 0:
					
					self.joc.equips[ self.joc.equip_actual].preguntes_tot[resultat-1] += 1		
					
					if not fespregunta:	fespregunta = Preguntador( self.joc )
					
					resultat = fespregunta.juguem( resultat )	
					
					if resultat > 0:
						self.joc.equips[ self.joc.equip_actual].preguntes_ok[resultat-1] += 1
						self.joc.equips[ self.joc.equip_actual].punts += 1
						
						fig_abans = self.joc.equips[ self.joc.equip_actual].figureta
						self.joc.equips[ self.joc.equip_actual].activaCategoria( resultat ) 
						
						if fig_abans != 63 and self.joc.equips[ self.joc.equip_actual].figureta == 63:
							self.joc.equips[ self.joc.equip_actual].punts += 2
						
					self.joc.equip_actual = seguentEquipActiu( self.joc.equips, self.joc.equip_actual )
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
