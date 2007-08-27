#!/usr/bin/python
# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
#
# Carles 24/8/2007
#

import sys
import pygame
import Numeric
import pygame.surfarray
import random
import re
import math
import time
import os

from Numeric import *
from pygame.locals import *

import freevialglob
from freevialglob import Freevial_globals

import preguntador
from preguntador import Preguntador

import roda
from roda import Roda


##################################################
#
# Classe de control del programa
#

carpeta_dades = '../data'

class Freevial:

	###########################################
	#
	def __init__( self ):
	
		self.dades_joc = Freevial_globals()
		
		self.dades_joc.mida_pantalla_x = 1024
		self.dades_joc.mida_pantalla_y = 768
		self.dades_joc.Limit_FPS = 40

	
	###########################################
	# Iniciem partida
	#
	def inici( self ):
		# inicialitzem la superficie de presentació
		self.dades_joc.pantalla = pygame.display.set_mode( ( self.dades_joc.mida_pantalla_x, self.dades_joc.mida_pantalla_y), 0, 32)
		pygame.display.toggle_fullscreen()

		# inicialitzem el sistema de so
		pygame.mixer.pre_init( 44100 )
		pygame.mixer.init(  )
		pygame.font.init()


	###########################################
	#
	# Control principal del programa
	#
	def juguem( self ):

		self.inici()

		roda = Roda( carpeta_dades )
		roda.juguem( self.dades_joc )

		fespregunta = Preguntador( carpeta_dades )
		fespregunta.juguem( self.dades_joc ) 


joc = Freevial()
joc.juguem()
