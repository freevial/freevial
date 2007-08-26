#!/usr/bin/python
# -*- coding: utf-8 -*-
 
##########################################
#
# Realitzador de preguntes
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

import preguntes

from Numeric import *
from pygame.locals import *
from preguntes import textpreguntes

mida_pantalla_x = 1024
mida_pantalla_y = 768
#Limit_FPS = 40

color_de_fons = 0, 0, 128
color_de_text = 255, 255, 255

mida_font = 40
altlinies = mida_font + 5
postextx= 80
postexty = 40

pregunta_actual = 0
pregunta = textpreguntes [pregunta_actual]

pantalla = pygame.display.set_mode((mida_pantalla_x,mida_pantalla_y), 0, 32)

mostrasolucions = 0


#pygame.display.toggle_fullscreen()
pygame.mixer.pre_init( 44100 )
pygame.mixer.init(  )
pygame.font.init()

fons = [ 	pygame.image.load('imatges/categoria1.png'), 
			pygame.image.load('imatges/categoria2.png'), 
			pygame.image.load('imatges/categoria3.png'), 
			pygame.image.load('imatges/categoria4.png'), 
			pygame.image.load('imatges/categoria5.png'), 
			pygame.image.load('imatges/categoria6.png') ]

mascara_de_fons = pygame.image.load('imatges/mascara_de_fons.png')
retalla_sel = pygame.image.load('imatges/retalla_sel.png')

solucio_ok = pygame.image.load('imatges/ok.png')
solucio_nook = pygame.image.load('imatges/nook.png')




mascara = pygame.Surface((655, 150), pygame.SRCALPHA, 32)
#mascara_de_fons = pygame.image.load('imatges/ruleta_front.png')

lletres = [ [pygame.image.load('imatges/lletraA.png'), pygame.image.load('imatges/lletraA_off.png')], [pygame.image.load('imatges/lletraB.png'), pygame.image.load('imatges/lletraB_off.png')], [pygame.image.load('imatges/lletraC.png'), pygame.image.load('imatges/lletraC_off.png')] ]

so_ticking2 = pygame.mixer.Sound( "sons/ticking2.ogg" )
so_drum2 = pygame.mixer.Sound( "sons/drum2.ogg" )
so_sub = pygame.mixer.Sound( "sons/sub.ogg" )
so_sub.set_volume( .1 )

so_ok = pygame.mixer.Sound( "sons/evil.ogg" )
so_nook = pygame.mixer.Sound( "sons/crboo.ogg" )


seleccio = 0

ypos = 190

nomove = 0	

def Scroll( surface, x, y, w, h, dx, dy ):

	surface.blit( surface, (x + dx, y + dy), (x, y, w - dx , h - dy) )



global sfc_pregunta

def comptalinies( cadena ):
	compta = 1

	for caracter in cadena:
		if ( '#' == caracter ) :
			compta += 1

	return compta



def pintatext( textapintar, mida ):

	font1 = pygame.font.Font( "lb.ttf", mida)

	cadenes = re.split( '#', textapintar )

	nlinia = 0


	sfc = pygame.Surface((1024, (comptalinies(textapintar) + 1)*altlinies), pygame.SRCALPHA, 32)
		

	for cadena in cadenes:
		text_pregunta = font1.render( cadena, 1, (0,0,0) )
		sfc.blit( text_pregunta, (0 + 2, altlinies * nlinia + 2))
		text_pregunta = font1.render( cadena, 1, color_de_text )
		sfc.blit( text_pregunta, (0, altlinies * nlinia))
		nlinia += 1

	return sfc

def Scroll( surface, x, y, w, h, dx, dy ):

	surface.blit( surface, (x + dx, y + dy), (x, y, w - dx , h - dy) )

def inicialitza_pregunta():
	global sfc_pregunta
	global sfc_respostaA 
	global sfc_respostaB
	global sfc_respostaC
	global sfc_npregunta
	global sfc_apregunta
	global seleccio 
	global temps_inici_pregunta
	global mostrasolucions
	global segons

	seleccio = 0

	sfc_pregunta  = pintatext( pregunta[1], mida_font )
	sfc_respostaA = pintatext( pregunta[2], mida_font )
	sfc_respostaB = pintatext( pregunta[3], mida_font )
	sfc_respostaC = pintatext( pregunta[4], mida_font )

	font1 = pygame.font.Font( "lb.ttf", 100)
	sfc_npregunta = text_pregunta = font1.render( str(pregunta[9]), 0, (255,255,255) )
	sfc_npregunta.set_alpha( 64 )

	font1 = pygame.font.Font( "lb.ttf", 16)
	sfc_apregunta = text_pregunta = font1.render( pregunta[6], 0, (255,255,255) )
	sfc_apregunta.set_alpha( 64 )	

	temps_inici_pregunta = time.time()
	segons = 99
	so_drum2.stop()
	so_drum2.play()

	mostrasolucions = 0

def atzar( categoria ):
	global pregunta

	cerca = categoria	
	anterior = pregunta[9] - 1
	nova = anterior

	while( nova == anterior or pregunta[0] != cerca ):		
		nova = 	int(random.random() * len(textpreguntes))
		pregunta = textpreguntes [ nova ]
		if( categoria == 0 ): cerca = pregunta[0]
	
	inicialitza_pregunta()

atzar( 0 )

inicialitza_pregunta()

temps = time.time()
darrer_temps = pygame.time.get_ticks()

imatges_x_segon = 0
Limit_FPS = 60

pantalla.fill( (0,0,0,0) )

mostranpregunta = 1

segons = 99

while 1:

	if time.time() > temps + 1:
		print "FPS: " + str( imatges_x_segon )
		temps = time.time()
		imatges_x_segon = 0
	else:
		imatges_x_segon = imatges_x_segon  + 1

#	dif_fps = 1000 / Limit_FPS 
#	dif_ticks = pygame.time.get_ticks() - darrer_temps
#	if( dif_ticks < dif_fps ):
#		pygame.time.wait(  dif_fps - dif_ticks )
#	darrer_temps = pygame.time.get_ticks()

	acaba = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYUP and event.key == pygame.K_q: sys.exit()

		if event.type == pygame.KEYUP and event.key == pygame.K_f: pygame.display.toggle_fullscreen()

		if ( mostrasolucions == 0 ):
			if event.type == pygame.KEYUP and event.key == pygame.K_a:	
				seleccio = 1
				so_sub.play()

			if event.type == pygame.KEYUP and event.key == pygame.K_b:	
				seleccio = 2
				so_sub.play()

			if event.type == pygame.KEYUP and event.key == pygame.K_c:	
				seleccio = 3
				so_sub.play()

			if event.type == pygame.KEYUP and event.key == pygame.K_DOWN: 
				seleccio += 1
				if( seleccio == 4):
					seleccio = 1
				so_sub.play()

			if event.type == pygame.KEYUP and event.key == pygame.K_UP: 
				seleccio -= 1
				if( seleccio <= 0):
					seleccio = 3	
				so_sub.play()

		if event.type == pygame.KEYUP and event.key == pygame.K_z:	
			mostranpregunta ^= 1
		
		if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT: 
			pregunta_actual+=1;
			pregunta_actual %= len ( textpreguntes )
			pregunta = textpreguntes [pregunta_actual]
			inicialitza_pregunta()

		if event.type == pygame.KEYUP and event.key == pygame.K_LEFT: 
			pregunta_actual-=1;
			pregunta_actual %= len ( textpreguntes )			
			pregunta = textpreguntes [pregunta_actual]
			inicialitza_pregunta()

		if event.type == pygame.KEYUP and event.key == pygame.K_1: 	atzar( 1 )
		if event.type == pygame.KEYUP and event.key == pygame.K_2:	atzar( 2 )
		if event.type == pygame.KEYUP and event.key == pygame.K_3:	atzar( 3 )
		if event.type == pygame.KEYUP and event.key == pygame.K_4:	atzar( 4 )
		if event.type == pygame.KEYUP and event.key == pygame.K_5:	atzar( 5 )
		if event.type == pygame.KEYUP and event.key == pygame.K_6:	atzar( 6 )
		if event.type == pygame.KEYUP and event.key == pygame.K_0:	atzar( 0 )

		if (event.type == pygame.KEYUP and event.key == pygame.K_RETURN):
			acaba = 1

	if (acaba == 1 or segons <= 0):
		if (mostrasolucions == 0):
			mostrasolucions = 3		
			if( pregunta[5] == seleccio):
				so_ok.play()
			else:
				so_nook.play()	
	

	ypos = ypos + 2
	if ypos >= mida_pantalla_y: ypos %= mida_pantalla_y


	#pantalla.blit( fons, (0, ypos) )
	#pantalla.blit( fons, (0, ypos- mida_pantalla_y) )

	pantalla.blit( fons[pregunta[0] - 1], (0,0), (0, (768 - ypos), mida_pantalla_x, min(200, ypos)))
	if( ypos < 200):
		pantalla.blit( fons[pregunta[0] - 1], (0, min( 200, ypos)), (0, 0, mida_pantalla_x, 200-min( 200, ypos)))


	pantalla.blit( mascara_de_fons, (0, 0) )

	ympos = ypos + 300
	ympos %= 768
	mascara.blit( fons[pregunta[0] - 1], (0,0), (0, (768 - ympos), mida_pantalla_x, min(200, ympos)))
	if( ympos < 200):
		mascara.blit( fons[pregunta[0] - 1], (0, min( 200, ympos)), (0, 0, mida_pantalla_x, 200-min( 200, ympos)))
	mascara.blit( retalla_sel, (0,0))

	if( seleccio == 1): pantalla.blit( mascara, (postextx, 260))
	if( seleccio == 2): pantalla.blit( mascara, (postextx, 260+150))
	if( seleccio == 3): pantalla.blit( mascara, (postextx, 260+300))

	if ( mostranpregunta != 0 ):
		pantalla.blit( sfc_npregunta, (1024 - (sfc_npregunta.get_width() + 25),0))
		pantalla.blit( sfc_apregunta, (1024 - (sfc_apregunta.get_width() + 25), 94))
		
	
	pantalla.blit( sfc_pregunta, (postextx, postexty) )	
	
	linia_act = 270
	if( seleccio == 1 ):
		pantalla.blit( lletres[0][0], ( postextx, linia_act ) )
	else:
		pantalla.blit( lletres[0][1], ( postextx, linia_act ) )

	pantalla.blit( sfc_respostaA, (postextx + 180 , linia_act + 20) )	

	linia_act += 150
	if( seleccio == 2 ):
		pantalla.blit( lletres[1][0], ( postextx, linia_act ) )
	else:
		pantalla.blit( lletres[1][1], ( postextx, linia_act ) )

	pantalla.blit( sfc_respostaB, (postextx + 180 , linia_act + 20) )	

	linia_act += 150

	if( seleccio == 3 ):
		pantalla.blit( lletres[2][0], ( postextx, linia_act ) )
	else:
		pantalla.blit( lletres[2][1], ( postextx, linia_act ) )

	pantalla.blit( sfc_respostaC, (postextx + 180 , linia_act + 20) )	

	segons_act = 60- int( (time.time() - temps_inici_pregunta) )
	if( segons_act < 0 ) : 
		segons_act = 0
		segons = 0

	if( mostrasolucions == 0):
		if( segons != segons_act ):
			segons = segons_act 
			font1 = pygame.font.Font( "lb.ttf", 600)
			pinta_segons = font1.render( str(segons).zfill(2), 0, (255,255,255) )
			print float(segons) / 60.0
			if ( segons < 20 ) :
				so_ticking2.set_volume( (20 -float(segons)) / 20.0  ) 
				so_ticking2.play()
		
		pinta_segons.set_alpha( (60 - segons_act) )
		pantalla.blit( pinta_segons, ( 300 , 150) )

#	if( segons <= 10):
#		pinta_segons.set_alpha( random.random() * 10 + 5 )
#		for compta in range(1, 10):
#			pantalla.blit( pinta_segons, ( random.random() * 1500 - 500 , random.random() * 1000 - 300) )


	linia_act = 270
	posn = 700
	posnook = 700 + cos(time.time()) * 25
	posok = 700 + cos(time.time() * 2) * 50


	if( mostrasolucions > 0):

		if( pregunta[5] == 1 ):
			if( seleccio != 1):
				pantalla.blit( solucio_ok, (posnook ,linia_act ) )
			else:
				pantalla.blit( solucio_ok, (posok ,linia_act ) )
	
		else:
			if( seleccio == 1 ):
				pantalla.blit( solucio_nook, (posn,linia_act ) )

	if( mostrasolucions > 1):
		if( pregunta[5] == 2 ):

			if( seleccio != 2):
				pantalla.blit( solucio_ok, (posnook ,linia_act + 150) )
			else:
				pantalla.blit( solucio_ok, (posok ,linia_act + 150) )
		else:
			if( seleccio == 2 ):
				pantalla.blit( solucio_nook, (posn,linia_act+ 150) )

	if( mostrasolucions > 2):
		if( pregunta[5] == 3 ):
			if( seleccio != 3):
				pantalla.blit( solucio_ok, (posnook ,linia_act +300) )
			else:
				pantalla.blit( solucio_ok, (posok ,linia_act +300) )
	
		else:
			if( seleccio == 3 ):
				pantalla.blit( solucio_nook, (posn,linia_act+ 150+ 150) )




	pygame.display.flip()

	pygame.time.Clock().tick( Limit_FPS )

	
	
