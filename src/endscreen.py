# -*- coding: utf-8 -*-

#
# Freevial
# End Screen
#
# Copyright (C) 2007 The Freevial Team
#
# By Carles Oriol i Margarit <carles@kumbaworld.com>
# By Siegfried-Angel Gevatter Pujals <siggi.gevatter@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys, random, pygame, time
import math

from freevialglob import *


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
		self.frate = frameRate( 50 )
		inici = time.time()

		self.naus = []

		loadSound( 'wonfv.ogg', volume = 0.8, music = 1).play( 1 )
		
		mou_fons = ypos = xpos = 0

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

			if segons > 5.5:
				if segons >= 35 and segons <= 48:
					nova_nau = Nau( segons *5 )
					nova_nau.velociat = segons - 30
					self.naus.append( nova_nau )
				elif not random.randint(0, 1):
						nova_nau = Nau()
						self.naus.append( nova_nau )
			
			for compta in range( len(self.naus) - 1, -1, -1):
				nau = self.naus[compta]
				if nau.esFora() :
					self.naus.remove( nau )
				else:
					nau.img += nau.spin
					nau.img %= 72

					dist = math.sqrt( abs(nau.x - 1024/2) * abs(nau.x - 1024/2) + abs(nau.y - 768/2) * abs(nau.y - 768/2))
					dist /= 150
		
					if( segons < 48 ):					
						nau.x += math.cos( nau.dir ) * nau.vel
						nau.y += math.sin( nau.dir ) * nau.vel
					elif (segons < 58):
						nau.x += math.cos( nau.dir + dist) * nau.vel
						nau.y += math.sin( nau.dir + dist) * nau.vel
					else :
						nau.x += math.cos( nau.dir - dist) * nau.vel
						nau.y += math.sin( nau.dir - dist) * nau.vel

			for event in pygame.event.get():
				if event.type == pygame.JOYBUTTONDOWN: translateJoystickEvent( event )

				if event.type == pygame.QUIT or keyPress(event, ('q', 'ESCAPE')):
					return
				
				if keyPress(event, ('PRINT')):
					screenshot( self.joc.pantalla )
				
				if mouseClick(event):
					nomove = 1
				
				if mouseRelease(event):
					nomove = 0
				
				if keyPress(event, ('f', 'F11')):
					pygame.display.toggle_fullscreen()

			if segons >= 68: return

			ypos += 1
			ypos %= self.joc.mida_pantalla_y
			xpos += 1
			xpos %= self.joc.mida_pantalla_x

			mou_fons += 10
	#		for num in range(0, 1024):
	#			self.fons_2.blit( self.fons, (num, math.cos((float(mou_fons +num)) / 100.0) * 10), ((xpos + num) % 1024, 0, 1, 768) )
 
			if segons > 5.5:

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
			
			if segons > 5.5:
				text_pos -= 20
				if text_pos < -(sfc_guanyadors.get_width() + 50):
					text_pos = 1024 + 50

				self.joc.pantalla.blit( sfc_guanyadors, (text_pos, 150 + math.cos((float(mou_fons +num)) / 100.0) * 200) )
			
			self.frate.next( self.joc.pantalla )

			pygame.display.flip()
