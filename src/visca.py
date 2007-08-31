#!/usr/bin/python
# -*- coding: utf-8 -*-
 
##########################################
#
# Iterador de fons mentre el concursant 
# pensa la pregunta
# 
# Cal sobreposar la pregunta i les respostes
#
# Carles 22/08/2007
# RainCT 27/08/2007
#

import sys, random, pygame, time
import math

from freevialglob import *

#from pygame import *
#from pygame.overlay import *


class Nau:
		x = 1024.0 / 2.0
		y = 768.0 / 2.0
		dir = 45.0
		vel = 1.0
		img = 0
		spin = 0

		def __init__( self, angle = None ):

			self.dir = angle if angle else random.randint( 0, 359 )
			self.vel = random.randint( 7, 15 )
			self.img = random.randint( 0, 71 )
			self.spin = random.randint( 1, 3) * -1 if random.randint(0,1) else 1 

			self.x += math.cos( self.dir ) * 100
			self.y += math.sin( self.dir ) * 100

		def esFora( self ):
			marge = 100
			return self.x < -marge or self.x > 1024 + marge or self.y < -marge or self.y > 768 + marge


def ensegments( llista_freevial, segons ):
	
	for segment in llista_freevial:
		if segons >= segment[0] and segons <= segment[1]:
			return True

	return False

class Visca:

	def __init__( self, joc ):

		self.joc = joc
	
		self.fons = loadImage('score_fons.png')
		self.fons_2 = pygame.Surface( ( 1024, 768), pygame.SRCALPHA, 32 )

		self.nau_sfc = []
		for num in range( 0, 72 ): 
			self.nau_sfc.append( loadImage('ovnis/freevial_tot' + str( num ).zfill(2) + '.png') )



	def juguem( self, joc, nomguanya ):

		self.joc = joc

		self.naus = []

		temps = time.time()
		darrer_temps = pygame.time.get_ticks()
		Limit_FPS = 50
		imatges_x_segon = 0
		
		inici = time.time()

		loadSound( 'wonfv.ogg', volume = 0.8, music = 1).play( 1 )
		
		mou_fons = ypos = xpos = 0

		#sfc_guanyadors = render_text( self.joc.equips[self.joc.equip_actual].nom, (64,64,64), 30, 1 )	
		sfc_guanyadors = render_text( nomguanya, (255,255,255), 300, 1 )	
		text_pos = 1024 + 50

		sfc_freevial = render_text( "freevial", (255,0,0), 200, 0 )	
		sfc_freevial.set_alpha( 64 )

		surten = 0
		while 1:

			segons = time.time() - inici

			if segons < 5.5 and int(segons) > surten:
				surten = int( segons)
				for compta in range( 0, 360, 10):
					nova_nau = Nau( compta )
					nova_nau.vel = surten * 2
					self.naus.append( nova_nau )

			if( segons > 5.5 ):
				if segons >= 35 and segons <= 48:
					nova_nau = Nau( segons *5 )
					nova_nau.velociat = segons - 30
					self.naus.append( nova_nau )
				else:
					if not random.randint(0, 1):
						nova_nau = Nau()
						self.naus.append( nova_nau )
			
			for compta in range( len(self.naus) - 1, -1, -1):
				nau = self.naus[compta]
				if nau.esFora() :
					self.naus.remove( nau )
				else:
					nau.img += nau.spin
					nau.img %= 72
					nau.x += math.cos( nau.dir ) * nau.vel
					nau.y += math.sin( nau.dir ) * nau.vel


			# Calculem el nombre de FPS
			if time.time() > temps + 1:
				#print "FPS: " + str( imatges_x_segon )
				temps = time.time()
				imatges_x_segon = 0
			else:
				imatges_x_segon +=  1

			# No cal limitador de frames actualment ja que estem en 7 aprox
			dif_fps = 1000 / Limit_FPS 
			dif_ticks = pygame.time.get_ticks() - darrer_temps
			if dif_ticks < dif_fps:
				pygame.time.wait(  dif_fps - dif_ticks )
				darrer_temps = pygame.time.get_ticks()



			for event in pygame.event.get():
				if event.type == pygame.QUIT or ( event.type == pygame.KEYUP and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE) ): sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN: nomove = 1
				if event.type == pygame.MOUSEBUTTONUP: nomove = 0
				if event.type == pygame.KEYUP and ( event.key == pygame.K_f or event.key == pygame.K_F11 ): pygame.display.toggle_fullscreen()

				if event.type == pygame.KEYUP and event.key == pygame.K_a:
					print "surt", segons

				if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
					print "entra", segons

			if segons >= 68: return

			ypos += 1
			ypos %= self.joc.mida_pantalla_y
			xpos += 1
			xpos %= self.joc.mida_pantalla_x


			mou_fons += 10
	#		for num in range(0, 1024):
	#			self.fons_2.blit( self.fons, (num, math.cos((float(mou_fons +num)) / 100.0) * 10), ((xpos + num) % 1024, 0, 1, 768) )
 
			if( segons > 5.5 ):

				self.joc.pantalla.blit( self.fons, (0,0))

				for num in range(0, 768):
					self.joc.pantalla.blit( self.fons, (math.cos((float(mou_fons +num)) / 100.0) * 20, num), (0, (ypos + num) % 768, 1024, 1) )
	
				llista_freevial = [ [8.7, 12], [12.7, 17], [20, 23.5], [27.5, 31], [33, 35.5], [49.5, 52.5], [55.5, 57.5], [60.9, 63.5] ]

				if ensegments( llista_freevial, segons ):
					for compta in range( 0, 5):
						self.joc.pantalla.blit( sfc_freevial, (random.randint(	-sfc_freevial.get_width(), 1024), random.randint(-sfc_freevial.get_height(), 768 )) ) 	
			else:
				self.joc.pantalla.fill( (0,0,0) )		


			for nau in self.naus:
				self.joc.pantalla.blit( self.nau_sfc[nau.img], (nau.x, nau.y ) )
			
			if( segons > 5.5 ):
				text_pos -= 20
				if( text_pos < -(sfc_guanyadors.get_width() + 50)):
					text_pos = 1024 + 50

				self.joc.pantalla.blit( sfc_guanyadors, (text_pos, 150 + math.cos((float(mou_fons +num)) / 100.0) * 200) )

			pygame.display.flip()

