# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Control de puntuació
#
# Carles 28/08/2007
# RainCT 28/08/2007
#

import sys, os.path, random, time
import math
import pygame, pygame.surfarray
from Numeric import *
from pygame.locals import *

from freevialglob import *


##################################################
#
# Empaquetat en una classe del selector d'equips
#

class Score:

	###########################################
	#
	def __init__( self, joc ):
		
		self.joc = joc
		
		self.mascara_de_fons = loadImage('fons_score.png')
		self.fons = loadImage('score_fons.png')	

		self.element_score = loadImage('element_score.png')
		self.seleccio_score = loadImage('seleccio_score.png')

		self.figureta = range(0,64)
		for num in range(0, 64):
			self.figureta[num] = loadImage('points/freevial_tot' + str( num ).zfill(2) + '.png')	

		self.so_sub = loadSound('sub.ogg', volume = 0.1)

	###########################################
	#
	# Bucle principal del programa
	#
	def juguem( self ):

		self.joc.pantalla.fill( (0,0,0,0) )

		temps = time.time()
		imatges_x_segon = 0
		darrer_temps = pygame.time.get_ticks()

		ypos = escriu = atzar = 0
		element_seleccionat = self.joc.equip_actual

		mou_fons = 0

		nou_grup = 1

		while 1:

			# Calculem el nombre de FPS
			if time.time() > temps + 1:
				#print "FPS: " + str( imatges_x_segon )
				temps = time.time()
				imatges_x_segon = 0
			else:
				imatges_x_segon +=  1
		
			# No cal limitador de frames actualment ja que estem en 7 aprox
			dif_fps = 1000 / self.joc.Limit_FPS 
			dif_ticks = pygame.time.get_ticks() - darrer_temps
			if( dif_ticks < dif_fps ):
				pygame.time.wait(  dif_fps - dif_ticks )
				darrer_temps = pygame.time.get_ticks()

			# Iterador d'events
			for event in pygame.event.get():

				if escriu:
					if event.type == pygame.KEYUP:
						if event.key in (K_RETURN, K_ESCAPE, K_KP_ENTER):
							escriu = 0
							if self.joc.equips[element_seleccionat].nom == '' and event.key == K_ESCAPE:
								self.joc.equips[element_seleccionat].actiu = 0
						elif event.key == K_BACKSPACE:
							if len(self.joc.equips[element_seleccionat].nom) > 0:
								self.joc.equips[element_seleccionat].nom = self.joc.equips[element_seleccionat].nom[:-1]
						else:
							self.joc.equips[element_seleccionat].nom += printKey( event.key )

				else:
				
					if event.type == pygame.QUIT or keyPress(event, ('q', 'ESCAPE')):
						return -1
					
					if keyPress(event, ('RIGHT', 'LEFT')): 
						element_seleccionat += +1 if (0 == (element_seleccionat % 2)) else -1 
						self.so_sub.play() 
					
					if keyPress(event, ('DOWN')): 
						element_seleccionat = (element_seleccionat + 2) % 6
						self.so_sub.play() 
					
					if keyPress(event, ('UP')): 
						element_seleccionat = (element_seleccionat - 2) % 6
						self.so_sub.play() 
					
					if keyPress(event, ('a')):
						nou_grup = 1
					
					if keyPress(event, ('n')):
						if self.joc.equips[element_seleccionat].actiu:
							escriu ^= 1
						else:
							nou_grup = 1
					
					if keyPress(event, ('K_f', 'K_F11')): pygame.display.toggle_fullscreen()
					
					if keyPress(event, ('z')): 
						if self.joc.equips[element_seleccionat].actiu: self.joc.equips[element_seleccionat].punts += 1
					
					if keyPress(event, ('x')): 
						if self.joc.equips[element_seleccionat].actiu and self.joc.equips[element_seleccionat].punts > 0: self.joc.equips[element_seleccionat].punts -= 1
					
					if self.joc.equips[element_seleccionat].actiu:
						if keyPress(event, ('1', 'KP1')): self.joc.equips[element_seleccionat].canviaCategoria( 1 )
						if keyPress(event, ('2', 'KP2')): self.joc.equips[element_seleccionat].canviaCategoria( 2 )
						if keyPress(event, ('3', 'KP3')): self.joc.equips[element_seleccionat].canviaCategoria( 3 )
						if keyPress(event, ('4', 'KP4')): self.joc.equips[element_seleccionat].canviaCategoria( 4 )
						if keyPress(event, ('5', 'KP5')): self.joc.equips[element_seleccionat].canviaCategoria( 5 )
						if keyPress(event, ('6', 'KP6')): self.joc.equips[element_seleccionat].canviaCategoria( 6 )
 					
					if keyPress(event, ('PAGEDOWN')): 
						if equipsActius( self.joc.equips ) >= 1:
							element_seleccionat = seguentEquipActiu( self.joc.equips, element_seleccionat )
							self.so_sub.play() 
					
					if keyPress(event, ('PAGEUP')): 
						if equipsActius( self.joc.equips ) >= 1:
							element_seleccionat = anteriorEquipActiu( self.joc.equips, element_seleccionat )
							self.so_sub.play() 
					
					if keyPress(event, ('r')): 
						atzar = 30 + int(random.random() * 30 )
 					
					if  event.type == pygame.MOUSEBUTTONDOWN or keyPress(event, ('RETURN', 'SPACE', 'KP_ENTER')):
						if self.joc.equips[element_seleccionat].actiu: 
							return element_seleccionat
						else:
							nou_grup = 1
					
					if nou_grup == 1:
						nou_grup = 0
						self.joc.equips[element_seleccionat].actiu ^= 1
						if self.joc.equips[element_seleccionat].actiu and self.joc.equips[element_seleccionat].nom == "": escriu ^= 1

			if atzar != 0 and equipsActius( self.joc.equips ) >= 2:
				element_seleccionat = seguentEquipActiu( self.joc.equips, element_seleccionat )
				atzar -= 1 
				self.so_sub.play() 
		
			# Animem el fons
			ypos += 1
			if ypos >= self.joc.mida_pantalla_y: ypos %= self.joc.mida_pantalla_y

			# Pintem el fons animat
			mou_fons += 8
			for num in range(0, 768):
				self.joc.pantalla.blit( self.fons, (cos((float(mou_fons +num)) / 100.0) * 20, num), (0, (ypos + num) % 768, 1024, 1) )
			#self.joc.pantalla.blit( self.fons, (0, ypos - 765 ) )
			#self.joc.pantalla.blit( self.fons, (0, ypos) )

			self.joc.pantalla.blit( self.mascara_de_fons, (0, 0) )

			# pintem les puntuacions
			for num in range(0, 6):
				ycaixa = (int(num / 2) * 200) + 135
				xcaixa = 75 if ((num % 2) == 0) else 515

				if element_seleccionat == num:
					self.joc.pantalla.blit( self.seleccio_score, (xcaixa - 58, ycaixa - 36) )
				
				if self.joc.equips[num].actiu:
	
					self.joc.pantalla.blit( self.element_score, (xcaixa, ycaixa ) )
					self.joc.pantalla.blit( self.figureta[self.joc.equips[num].figureta], (xcaixa + 15, ycaixa  ) )

					text_nom = self.joc.equips[num].nom
					if escriu and num == element_seleccionat:
						if (int(time.time() * 4) % 2) == 0: text_nom += "_"  
					pinta = render_text( text_nom, (0,0,0), 30, 1)
					self.joc.pantalla.blit( pinta, (xcaixa + 25 , ycaixa + 125 ) )

					color = (128,0,0) if (maxPunts( self.joc.equips) > self.joc.equips[num].punts ) else (0,128,0)
					pinta = render_text( str(self.joc.equips[num].punts).zfill(2), color, 150, 1)
					self.joc.pantalla.blit( pinta, (xcaixa + 200, ycaixa - 15) )


			#intercanviem els buffers de self.joc.pantalla
			pygame.display.flip()

		return 0
