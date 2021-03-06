# -*- coding: utf-8 -*-

#
# Freevial
# End Screen
#
# Copyright (C) 2007-2009 The Freevial Team
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
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import random
import pygame
import time
import math

from common.globals import Global
from common.freevialglob import *
from common.events import eventLoop


class Nau:
		x = 1024.0 / 2.0
		y = 768.0 / 2.0
		dir = 45.0
		vel = 1.0
		img = 0
		spin = 0

		def __init__(self, angle = None):
			
			self.dir = if2(angle, angle, random.randint(0, 359))
			self.vel = random.randint(7, 15)
			self.img = random.randint(0, 71)
			self.spin = if2(random.randint(0,1), random.randint(1, 3) * -1, 1)

			self.x += math.cos(self.dir) * 100
			self.y += math.sin(self.dir) * 100

		def esFora(self):
			marge = 100
			return self.x < -marge or self.x > 1024 + marge or self.y < -marge or self.y > 768 + marge


class Cua:

	def __init__(self, punt):
		self.pos = [punt[0], punt[1]]
		self.time = time.time()
		self.cau = 0


def ensegments(llista_freevial, segons):
	
	for segment in llista_freevial:
		if segons >= segment[0] and segons <= segment[1]:
			return True

	return False


class Visca:

	def __init__(self, joc):

		Global.game = joc
	
		self.fons = load_image('score_fons.png')
		self.fons_2 = pygame.Surface((1024, 768), pygame.SRCALPHA, 32)

		self.nau_sfc = []
		for num in xrange(0, 72): 
			self.nau_sfc.append(load_image('ovnis/freevial_tot' + str(num).zfill(2) + '.png'))

		self.sfc_llum = load_image('llum.png')

	def juguem(self, game, nomguanya):
		
		Global.game = game
		self.frate = frameRate(Global.fps_limit)
		inici = time.time()

		self.naus = []

		load_sound('wonfv.ogg', volume = 0.8, music = 1).play(1)
		
		mou_fons = ypos = xpos = 0

		sfc_guanyadors = render_text(nomguanya, (255,255,255), 300, 1)	
		text_pos = 1024 + 50

		sfc_freevial = render_text("freevial", (255,0,0), 200, 0)	
		sfc_freevial.set_alpha(64)

		surten = 0

		cues = []
		
		llums = 0
	
		while 1:

			segons = time.time() - inici

			for cua in cues:
				if time.time() - cua.time > .4 and cua.cau == 0: 
					cues.remove(cua)

				if cua.cau:
					cua.pos[1] += cua.cau
					if cua.pos[1] > 768:
						cues.remove(cua)


			fes_llums = False
			if (llums == 0 and segons > 45) or (llums == 1 and segons > 55) or (llums == 2 and segons > 64) or (llums == 3 and segons > 65) or (llums == 4 and segons > 66):
				llums += 1
				fes_llums = True
 
			if fes_llums:
				pos = 0
				while pos < 1024:
					pos += random.randint(1, 10)
					cua = Cua((pos, random.randint(0,5)))
					cua.cau = random.randint(5, 25) 
					cues.append (cua) 

			if segons < 5.5 and int(segons) > surten:
				surten = int(segons)
				for num in xrange(0, 360, 10):
					nova_nau = Nau(num)
					nova_nau.vel = surten * 2
					self.naus.append(nova_nau)

			if segons > 5.5:
				if segons >= 35 and segons <= 48:
					nova_nau = Nau(segons *5)
					nova_nau.velociat = segons - 30
					self.naus.append(nova_nau)
				elif not random.randint(0, 1):
						nova_nau = Nau()
						self.naus.append(nova_nau)
			
			for num in xrange(len(self.naus) - 1, -1, -1):
				nau = self.naus[num]
				if nau.esFora() :
					self.naus.remove(nau)
				else:
					nau.img += nau.spin
					nau.img %= 72

					dist = math.sqrt(abs(nau.x - 1024/2) * abs(nau.x - 1024/2) + abs(nau.y - 768/2) * abs(nau.y - 768/2))
					dist /= 150
		
					if(segons < 48):					
						nau.x += math.cos(nau.dir) * nau.vel
						nau.y += math.sin(nau.dir) * nau.vel
					elif (segons < 58):
						nau.x += math.cos(nau.dir + dist) * nau.vel
						nau.y += math.sin(nau.dir + dist) * nau.vel
					else :
						nau.x += math.cos(nau.dir - dist) * nau.vel
						nau.y += math.sin(nau.dir - dist) * nau.vel

			for event in eventLoop():
				
				if event.keyUp('q', 'ESCAPE') and not Global.LOCKED_MODE:
					if not Global.MUSIC_MUTE:
						pygame.mixer.music.fadeout(1500)
					return
			
			if segons >= 68: return

			ypos += 1
			ypos %= Global.screen_y
			xpos += 1
			xpos %= Global.screen_x

			mou_fons += 10

			if segons > 5.5:

				Global.game.screen.blit(self.fons, (0,0))

				for num in xrange(0, 768):
					Global.game.screen.blit(self.fons, (math.cos((float(mou_fons +num)) / 100.0) * 20, num), (0, (ypos + num) % 768, 1024, 1))
	
				llista_freevial = [ [8.7, 12], [12.7, 17], [20, 23.5], [27.5, 31], [33, 35.5], [49.5, 52.5], [55.5, 57.5], [60.9, 63.5] ]

				if ensegments(llista_freevial, segons):
					for num in xrange(0, 5):
						Global.game.screen.blit(sfc_freevial, (random.randint(-sfc_freevial.get_width(), 1024), random.randint(-sfc_freevial.get_height(), 768))) 	

					if segons >= 20 and segons <=34:
						for nau in self.naus:
							cues.append (Cua((nau.x + 32 - 8, nau.y + 32 - 4)))

			else:
				Global.game.screen.fill((0,0,0))

			for cua in cues:
								#m'ha petat aqui. suposo que faltava l'if2 pero no m'ho he mirat
				dist = if2(cua.cau == 0, int((time.time() - cua.time) * 40), 0)
				Global.game.screen.blit(self.sfc_llum, (cua.pos[0] + random.randint(-dist,dist), cua.pos[1] + random.randint(-dist,dist)))

			for nau in self.naus:
				Global.game.screen.blit(self.nau_sfc[nau.img], (nau.x, nau.y))
			
			if segons > 5.5:
				text_pos -= 20
				if text_pos < -(sfc_guanyadors.get_width() + 50):
					text_pos = 1024 + 50

				Global.game.screen.blit(sfc_guanyadors, (text_pos, 150 + math.cos((float(mou_fons +num)) / 100.0) * 200))
			
			self.frate.next(Global.game.screen)

			pygame.display.flip()
