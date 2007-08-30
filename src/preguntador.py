# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Realitzador de preguntes
#
# Carles 28/08/2007
# RainCT 27/08/2007
#

import sys, os.path, random, math, time, pygame
from Numeric import *

from freevialglob import *
from preguntes import *


##################################################
#
# Empaquetat en una classe del preguntador
#

class Preguntador:

	###########################################
	#
	def __init__( self, joc ):
		
		self.joc = joc
		
		self.color_de_fons = (0, 0, 0)
		self.color_de_text = (255, 255, 255)
		
		self.mida_font = 40
		self.altlinies = self.mida_font + 5
		self.postextx= 80
		self.postexty = 40
		
		self.pregunta_actual = None
		self.mostrasolucions = self.seleccio = 0
		self.ypos = 190
		
		# carrega d'imatges
		self.fons = range(0, 6)
		for num in range(0, 6):
			self.fons[num] = loadImage( 'categoria' + str(num + 1) + '.png' )
		
		self.mascara_de_fons = loadImage('mascara_de_fons.png')
		self.retalla_sel = loadImage('retalla_sel.png')
		
		self.solucio_ok = loadImage('ok.png')
		self.solucio_nook = loadImage('nook.png')
		
		self.mascara = pygame.Surface((655, 150), pygame.SRCALPHA, 32)
		
		self.lletres = [
								[ loadImage('lletraA.png'), loadImage('lletraA_off.png') ], 
								[ loadImage('lletraB.png'), loadImage('lletraB_off.png') ], 				
								[ loadImage('lletraC.png'), loadImage('lletraC_off.png') ],
							]
		

		# carreguem els arxius de so
		self.so_ticking2 = loadSound('ticking2.ogg')
		self.so_drum2 = loadSound('drum2.ogg')
		self.so_sub = loadSound('sub.ogg', volume = 0.1)
		self.so_ok = loadSound('cheer.ogg')
		self.so_nook = loadSound('crboo.ogg')
		
		# mostra nombre de pregunta i autor?
		self.mostranpregunta = 1
		
		self.help_overlay = createHelpScreen( 'preguntador' )

	###########################################
	#
	# Funció per veure el nombre de linies que té una frase a mostrar
	# basant-nos en que el separador és el caracter #
	def numlinies( self, cadena ):
		
		return cadena.count('#')
	
	###########################################
	#
	# Funció per pintar el text i les preguntes sobre una nova superficie
	# usant el color del text i el sobrejat
	def pintatext( self, textapintar, mida ):

		cadenes = textapintar.split('#')
		nlinia = 0

		sfc = pygame.Surface( ( 1024, ( self.numlinies ( textapintar ) + 1 ) * (mida + 25) ), pygame.SRCALPHA, 32 )

		for cadena in cadenes:
			text_pregunta = render_text( cadena, self.color_de_fons, mida, 1 )
			sfc.blit( text_pregunta, (0 + 2, self.altlinies * nlinia + 2))

			text_pregunta = render_text( cadena, self.color_de_text, mida, 1 )
			sfc.blit( text_pregunta, (0, self.altlinies * nlinia))

			nlinia += 1

		return sfc


	###########################################
	#
	# Inicialitzador de nova pregunta
	#
	def inicialitza_pregunta( self ):

		self.seleccio = 0

		self.sfc_pregunta  = self.pintatext( self.pregunta_actual[1], self.mida_font )

		self.sfc_resposta = range(0, 3)
		for num in range(0, 3):
			self.sfc_resposta[ num ] = self.pintatext( self.pregunta_actual[ num + 2 ], self.mida_font )

		self.sfc_npregunta = render_text( str(self.pregunta_actual[9]), (255,255,255), 100 )
		self.sfc_npregunta.set_alpha( 64 )

		self.sfc_apregunta = render_text( str(self.pregunta_actual[6]), (255,255,255), 16 )
		self.sfc_apregunta.set_alpha( 64 )	

		self.temps_inici_pregunta = time.time()
		self.segons = 61
		self.so_drum2.stop()
		self.so_drum2.play()

		self.mostrasolucions = 0

	###########################################
	#
	# Cercador de preguntes a l'atzar
	# si la categoria és 0 no té en compte el valor
	def atzar( self, categoria ):
		
		if len(preguntes[ categoria - 1 ]):
			preguntes[ categoria - 1 ].extend(preguntes_backup[ categoria - 1 ])
		
		self.pregunta_actual = preguntes[ categoria - 1 ].pop()
		
		self.inicialitza_pregunta()


	###########################################
	#
	# Bucle principal del programa
	#
	def juguem( self , selcat):

		# de moment per fer proves agafem una pregunta a l'atzar

		self.atzar( selcat )

		self.inicialitza_pregunta()

		temps = time.time()
		darrer_temps = pygame.time.get_ticks()

		imatges_x_segon = mostra_ajuda = mostra_credits = 0

		self.joc.pantalla.fill( (0,0,0,0) )

		# segons restants per fi de pregunta
		self.segons = 61

		nom_equip_sfc = render_text( self.joc.equips[self.joc.equip_actual].nom, (64,64,64), 30, 1 )	
		nom_equip_sfc = pygame.transform.rotate ( nom_equip_sfc, 90 )
		nom_equip_sfc.set_alpha( 64 )

		mostra_punt_de_categoria = match_point = False

		if (self.joc.equips[self.joc.equip_actual].figureta & bitCategoria( selcat )) == 0:
			mostra_punt_de_categoria = True
			figureta_no = loadImage('points/freevial_tot' + str( self.joc.equips[self.joc.equip_actual].figureta).zfill(2) + '.png')
			figureta_si = loadImage('points/freevial_tot' + str( self.joc.equips[self.joc.equip_actual].figureta | bitCategoria ( selcat )).zfill(2) + '.png')

			match_point = True if (self.joc.equips[self.joc.equip_actual].figureta | bitCategoria ( selcat ) == 63) else False

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
			if dif_ticks < dif_fps:
				pygame.time.wait(  dif_fps - dif_ticks )
				darrer_temps = pygame.time.get_ticks()
			
			acaba = 0
			
			# Iterador d'events
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				
				if keyPress(event, ('q', 'ESCAPE')):
					if not mostra_ajuda and not mostra_credits:
						pygame.mixer.fadeout(500)
						if self.mostrasolucions == 0:
							self.mostrasolucions = 1
							self.seleccio = 0
						acaba = 1
					else:
						mostra_ajuda = mostra_credits = 0
				
				if keyPress(event, ('F1')) or keyPress(event, ('h')):
					mostra_ajuda ^= 1
					mostra_credits = 0

				if keyPress(event, ('F2')):
					mostra_ajuda = 0
					mostra_credits ^= 1
				
				if keyPress(event, ('f', 'F11')): pygame.display.toggle_fullscreen()
				
				if self.mostrasolucions == 0:
					if keyPress(event, ('a', 'i')):
						if keyPress(event, 'a'): acaba = 1	
						self.seleccio = 1
						self.so_sub.play()
					
					if keyPress(event, ('b', 'o')):	
						if keyPress(event, 'b'): acaba = 1
						self.seleccio = 2
						self.so_sub.play()
					
					if keyPress(event, ('c', 'p')):	
						if keyPress(event, 'c'): acaba = 1
						self.seleccio = 3
						self.so_sub.play()
					
					if keyPress(event, ('DOWN', 'TAB')): 
						self.seleccio += 1
						if self.seleccio == 4:
							self.seleccio = 1
						self.so_sub.play()
					
					if keyPress(event, 'UP'): 
						self.seleccio -= 1
						if self.seleccio <= 0:
							self.seleccio = 3	
						self.so_sub.play()
				
				if keyPress(event, 'z'):	
					self.mostranpregunta ^= 1
				
				if keyPress(event, ('1', 'KP1')): 	self.atzar( 1 )
				if keyPress(event, ('2', 'KP2')):	self.atzar( 2 )
				if keyPress(event, ('3', 'KP3')):	self.atzar( 3 )
				if keyPress(event, ('4', 'KP4')):	self.atzar( 4 )
				if keyPress(event, ('5', 'KP5')):	self.atzar( 5 )
				if keyPress(event, ('6', 'KP6')):	self.atzar( 6 )
				
				if mouseClick(event, 'primary') or keyPress(event, ('RETURN', 'SPACE', 'KP_ENTER')):
					acaba = 1
				
			# Si hem premut a return o s'ha acabat el temps finalitzem
			if acaba == 1 or self.segons <= 0:
				if self.mostrasolucions == 0:
					self.mostrasolucions = 3		
					if self.pregunta_actual[5] == self.seleccio:
						self.so_ok.play()
					else:
						self.so_nook.play()	
				elif acaba == 1:
					pygame.mixer.fadeout(500)
					return self.pregunta_actual[0] if ( self.pregunta_actual[5] == self.seleccio) else 0
			
			# Animem el fons
			self.ypos += 2
			if self.ypos >= self.joc.mida_pantalla_y: self.ypos %= self.joc.mida_pantalla_y
			
			# Pintem el fons animat
			self.joc.pantalla.blit( self.fons[self.pregunta_actual[0] - 1], (0,0), (0, (768 - self.ypos), self.joc.mida_pantalla_x, min(200, self.ypos)))
			if self.ypos < 200:
				self.joc.pantalla.blit( self.fons[self.pregunta_actual[0] - 1], (0, min( 200, self.ypos)), (0, 0, self.joc.mida_pantalla_x, 200 - min( 200, self.ypos)))
			
			# i el sombrejem per fer l'efecte de desapariió
			# també pintem el logotip del peu a l'hora que esborrem el fons de self.joc.pantalla
			self.joc.pantalla.blit( self.mascara_de_fons, (0, 0) )
			
			# preparem el sobrejat de l'opció seleccionada
			ympos = self.ypos + 300
			ympos %= 768
			self.mascara.blit( self.fons[ self.pregunta_actual[0] - 1], (0,0), (0, (768 - ympos), self.joc.mida_pantalla_x, min( 200, ympos )))
			
			if ympos < 200: 
				self.mascara.blit( self.fons[ self.pregunta_actual[0] - 1], (0, min( 200, ympos)), (0, 0, self.joc.mida_pantalla_x, 200 - min( 200, ympos)))
			
			# i el mesclem amb la mascara per donar-li forma
			self.mascara.blit( self.retalla_sel, (0,0))
			
			# pintem l'ombrejat on correspongui	
			if self.seleccio == 1: self.joc.pantalla.blit( self.mascara, ( self.postextx, 260))
			if self.seleccio == 2: self.joc.pantalla.blit( self.mascara, ( self.postextx, 260+150))
			if self.seleccio == 3: self.joc.pantalla.blit( self.mascara, ( self.postextx, 260+300))
			
			# mostrem l'autor i el mombre de pregunta
			if  self.mostranpregunta != 0 :
				self.joc.pantalla.blit( self.sfc_npregunta, (1024 - ( self.sfc_npregunta.get_width() + 25),0) )
				self.joc.pantalla.blit( self.sfc_apregunta, (1024 - ( self.sfc_apregunta.get_width() + 25), 94) )
			
			# mostrem la pregunta
			self.joc.pantalla.blit( self.sfc_pregunta, (self.postextx, self.postexty) )	
			
			# i les solucions			
			linia_act = 270
			
			for num in range(0, 3):
				self.joc.pantalla.blit( self.lletres[num][(self.seleccio != num + 1)], ( self.postextx, linia_act + (150 * num)) )
				self.joc.pantalla.blit( self.sfc_resposta[ num ], (self.postextx + 180 , linia_act + 20 + (150 * num)) )		
			
			# comprovem l'estat del temps
			segons_act = 60 - int( (time.time() - self.temps_inici_pregunta) )
			if segons_act < 0: 
				segons_act = 0
				self.segons = 0
			
			# si no estem en l'estat de mostrar les soŀlucions mostrem el temps restant
			if self.mostrasolucions == 0:
				if self.segons != segons_act:
					# el segon actual ha canviat
					self.segons = segons_act 
					self.pinta_segons = render_text( str( self.segons ).zfill(2), (255,255,255), 600)
					# s'acaba el temps indiquem'ho amb so
					if self.segons < 20:
						self.so_ticking2.set_volume( (20 - float( self.segons )) / 20.0  ) 
						self.so_ticking2.play()
				
				# pintem els segons que queden, posant-los cada cop menys transparents
				self.pinta_segons.set_alpha( (60 - segons_act) )
				self.joc.pantalla.blit( self.pinta_segons, ( 300 , 150) )
			
			# Pintem les solucions
			linia_act = 270
			posn = 700
			posnook = 700 + cos(time.time()) * 25
			posok = 700 + cos(time.time() * 2) * 50
			
			if self.mostrasolucions > 0:
				
				for num in range (0, 3):
					if self.pregunta_actual[5] == (num + 1):
						if self.seleccio != (num + 1):
							self.joc.pantalla.blit( self.solucio_ok, (posnook, linia_act + (150 * num)) )
						else:
							self.joc.pantalla.blit( self.solucio_ok, (posok, linia_act + (150 * num)) )
				
					else:
						if self.seleccio == (num + 1):
							self.joc.pantalla.blit( self.solucio_nook, (posn, linia_act + (150 * num)) )
			
			if mostra_punt_de_categoria:
				if match_point:
					t = time.time()
					for compta in range( 0, 16) :
						self.joc.pantalla.blit( figureta_no if (int(time.time() * 2) % 2) == 0 else figureta_si, (500+ cos(t+(float(compta)/15)) * 400, 110 + sin((t + (float(compta)/10)) * 2) * 25) )
				else:
					self.joc.pantalla.blit( figureta_no if (int(time.time() * 2) % 2) == 0 else figureta_si, (880, 130) )
			
			self.joc.pantalla.blit( nom_equip_sfc, (20, 748 - nom_equip_sfc.get_height()))
			
			if mostra_ajuda: self.joc.pantalla.blit( self.help_overlay, (0,0))
			if mostra_credits: self.joc.pantalla.blit( self.joc.sfc_credits, (0,0))

			#intercanviem els buffers de self.joc.pantalla
			pygame.display.flip()
		
		return 0
