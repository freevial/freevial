# -*- coding: utf-8 -*-

#
# Freevial
# Commonly used stuff
#
# Copyright (C) 2007, 2008 The Freevial Team
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
import os.path
import random
import pygame
import locale
import time
import gettext
import urllib

from pygame.locals import *

from common.globals import Global

gettext.install('freevial', '/usr/share/locale', unicode=1)

class Equip:
	
	name = ''
	points = 0
	errors = 0
	figureta = 0
	active = False
	eliminat = False
	teamgotxie_name = ''
	
	sfc_nom = None
	teamgotxie_sfc = None
	
	def __init__(self, num):
		
		self.id = num
		
		self.preguntes_tot = []
		self.preguntes_ok = []
		
		for num in xrange(0, 6): 
			self.preguntes_tot.append(0)
			self.preguntes_ok.append(0)

	def canviaCategoria(self, categoria):
		# Les tenim desendreçades i això ho complica una mica
		self.figureta ^= bitCategoria(categoria)

	def activaCategoria(self, categoria):
		# Les tenim desendreçades i això ho complica una mica
		self.figureta |= bitCategoria(categoria)

	def teCategoria(self, categoria) :
		return (self.figureta & bitCategoria(categoria)) != 0


def bitCategoria (categoria):
	return (0x4,0x8,0x20,0x10,0x2,0x1)[ categoria ]


def load_image_http(filename):
	
	imatge = None
		
	try:
		import tempfile
		fileonly = filename[filename.rfind("/")+1:]
		tempdir = tempfile.mkdtemp()
		tempname = os.path.join(tempdir, fileonly)
		
		opener = urllib.FancyURLopener({})
		f = opener.open(filename)
		
		llegit = f.read()
		f.close()
		
		file = open(tempname, "wb")
		file.write(llegit)
		file.close()
		
		imatge = pygame.image.load(tempname).convert_alpha()

	except:
		imatge = None

	return imatge


def load_image(name, colorkey = None, rotate = 0):
	""" Returns a Surface of the indicated image, which is expected to be in one
	of the images directories. """
	
	image = None
	
	if name.lower().startswith('http://'):
		image = load_image_http(name)
	
	else:
		
		fullname = first_existing_location(name, [Global.folders['images'],
			Global.folders['teamgotxies']] + Global.databasefolders)
		
		if fullname:
			try:
				image = pygame.image.load(fullname)
			except pygame.error:
				print >> sys.stderr, _(u'Could not load image "%s".' % fullname)
				raise SystemExit
		else:
			print >> sys.stderr, _(u'Could not find image "%s".' % name)
			# TODO: Consider returning a placeholder image and not crashing.
			raise SystemExit
	
	if image != None:
		
		if colorkey is not None:
			if colorkey is -1:
				colorkey = image.get_at((0,0))
			image = image.convert()
			image.set_colorkey(colorkey, pygame.RLEACCEL)
		else:
			image = image.convert_alpha()
		
		if rotate != 0:
			image = rotateImage(image, rotate)
	
	return image


def load_sound(name, volume = 1.0, music = False):
	""" Returns a sound object of the indicated audio file, which is expected to be in the sounds folder. """
	
	if (Global.MUSIC_MUTE and music) or (Global.SOUND_MUTE and not music) or not pygame.mixer or not pygame.mixer.get_init():
	
		class NoneSound:
			def load(*args): pass
			def play(*args): pass
			def stop(*args): pass
			def set_volume(*args): pass
		
		return NoneSound()
	
	fullname = os.path.join(Global.folders['sounds'], name)
	
	if not os.path.exists(fullname):
		# Also try in database paths
		for foldername in Global.databasefolders:
			fulln = os.path.join(foldername, str(name))
			if os.path.exists(fulln):
				fullname = fulln	
				break
	
	try:
		if not music:
			obj = pygame.mixer.Sound(fullname)
		else:
			obj = pygame.mixer.music
			obj.load(fullname)
	
	except pygame.error, message:
		
		print _('Failed loading sound: %s' % fullname)
		
		if not music:
			raise SystemExit, message
	
	obj.set_volume(float(volume))
	
	return obj

default_font = '/usr/share/fonts/truetype/unfonts/UnBatangBold.ttf'


def set_default_font(font_name):

	if os.path.isfile(font_name):
		default_font = font_name
		

def render_text(cadena, color, mida, antialias = 0, font_name = '', maxwidth = 0):
	""" Function for easier text rendering. """

	global default_font

	if os.path.isfile(font_name):
		font = pygame.font.Font(font_name, mida)
	else:
		if not font_name:
			font_name = default_font
		font_path = os.path.join(Global.folders['fonts'], font_name)
		if os.path.isfile(font_path):
			font = pygame.font.Font(font_path, mida)
		else:
			# NOT WORKING IN PYGAME
			font = pygame.font.SysFont(font_name, mida)
	
	text_restant = cadena
	sfc = None

	if maxwidth:
		sfcs = []

		while text_restant != "":

			ample = maxwidth + 1
			escriure = text_restant

			while ample > maxwidth:

				sfc = font.render(escriure, antialias, color)
				ample = sfc.get_width()		
			
				if ample > maxwidth:
					tpos = escriure.rfind(' ')
					if tpos == -1:
						ample = maxwidth
					else:
						escriure = escriure[0:tpos]		

			sfcs.append(sfc)
			text_restant = text_restant[ len(escriure)+1:]
		
		if len(sfcs) > 1:
			iample = 0
			ialt = 0
			for num in xrange(0, len(sfcs)):
				ialt += max(sfcs[num].get_height(), mida)
				iample = min(maxwidth, max(iample, sfcs[num].get_width()))
			
			sfc = pygame.Surface((iample, ialt), pygame.SRCALPHA, 32)
			
			pos = 0
			for num in xrange(0, len(sfcs)):
				sfc.blit(sfcs[num], (0, pos))
				pos += max(sfcs[num].get_height(), mida)
		
		else:
			sfc = if2(len(sfcs) == 1, sfcs[0], None)
	else:
		sfc = font.render(cadena, antialias, color)
	
	return sfc

def screenshot(surface, destination = os.path.join(os.path.expanduser('~'), 'Freevial/Screenshots/')):
	""" Saves a screenshot of the indicated surface. """
	
	destination = os.path.normpath(destination)
	
	if not os.path.exists(destination):
		os.makedirs(destination)
	
	# PNG and JPEG saving is new in pygame 1.8.
	destination = os.path.join(destination, str(time.time()) + '.tga')
	
	pygame.image.save(surface, destination)


def maxPunts(teams):

	puntsmax = 0

	for team in teams:
		if team.active:
			puntsmax = max(puntsmax, team.points)
	
	return puntsmax


def puntsTotals(teams):

	punts = 0

	for team in teams:
		punts += team.points
	
	return punts


def teamsActius(teams):

	actius = 0

	for team in teams:
		if team.active: actius += 1
	
	return actius


def winning_team(teams, mode, extra=None, force=False):
	""" winning_team(teams, mode, extra=None) -> int
	
	Calculates which team is currently winning and returns it's index number
	in the teams array, or -1 if there's a tie or the game can't end yet.
	
	Possible values for mode:
	 - 0. The game ends when one of the teams completes the six parts of its
		  icon and there is no tie. The team with the most points wins.
	 - 1. The first team to get the amount of points indicated as $extra wins.
	 - 2. The last team which fails the amount of questions indicated as
		  $extra wins.
	 - 3. The first team to complete the six parts of its icon wins.
	
	Setting $force to true will relax the checks and if there is no tie a winner
	will returned be even if the game hasn't ended yet.
	
	"""

	winner = -1
	active_teams = [x for x in teams if x.active]
	
	# Used by some modes
	best_value = 0
	game_ends = False
	
	if force and len(active_teams) == 1:
		# There's only one team
		return active_teams[0].id
	
	if mode == 0:
		
		for team in active_teams:
			if team.points == best_value:
				winner = -1 # Tie
			elif team.points > best_value:
				winner = team.id
				best_value = team.points
			if team.figureta == 63:
				game_ends = True
		
		if not game_ends and not force:
			winner = -1
	
	elif mode == 1:
		
		for team in active_teams:
			if team.points >= extra:
				winner = team.id
				game_ends = True
			elif force and not game_ends and team.points > best_value:
				winner = team.id
				best_value = team.points
	
	elif mode == 2:
		candidates = []
		for team in active_teams:
			if team.errors < extra:
				candidates.append(team.id)
		if len(candidates) == 1:
			winner = candidates[0]
		elif force and team.errors < best_value:
			winner = team.id
			best_value = team.errors
	
	elif mode == 3:
		# TODO: Calculate the winner in an alternative way if $force is True.
		for team in active_teams:
			if team.figureta == 63:
				winner = team.id
	
	return winner


def seguentEquipActiu(teams, actual):

	actual += 1

	for team in teams:
		if teams[ (actual + team.id) % Global.game.max_teams ].active: 
			return (actual + team.id) % Global.game.max_teams
	
	return -1


def anteriorEquipActiu(teams, actual):

	actual -= 1

	for team in teams:
		if teams[ (actual - team.id) % Global.game.max_teams ].active: 
			return (actual - team.id) % Global.game.max_teams
	
	return -1


def list2string(list, wordsEachLine = 5, lineEnd = ','):
	""" Converts a list of words into a list of comma-separated string with 'wordsEachLine' words. """
	
	lines = []
	string = ''
	i = 0
	
	for author in list:
		
		if string != '':
			string += ', '
		
		string += author
		
		if (wordsEachLine - 1) == (i % wordsEachLine):
			lines.append(str(string + lineEnd))
			string = ''

		i += 1
		
	if string != '':
		lines.append(str(string + lineEnd))
	
	lines[-1] = lines[-1][:-len(lineEnd)]
	
	return lines


def createTextSurface(text, color, intensitat = 25):
	""" Creates a help overlay surface and prints the passed text on it. """
	
	font_size = 14
	
	help_overlay = pygame.Surface((1024, 768), pygame.SRCALPHA, 32)
	
	for num in xrange(0, 10):
		help_overlay.fill((0, 0, 16, num * intensitat), (100 + (num * 2), 100 + (num * 2), 1024 - 100 * 2 - (num * 4), 768 - 150 - (num * 4)))
	
	nline = 0

	pos = 0
	for line in text.split('\n'):
		if line != '':	
			text_pregunta = render_text(line, (0,0,0), font_size, 1, '', 700)
			help_overlay.blit(text_pregunta, (150 + 2, pos + 142))
			
			text_pregunta = render_text(line, color, font_size, 1, '', 700)
			help_overlay.blit(text_pregunta, (150, pos + 140))
			
			pos += text_pregunta.get_height()
		else:
			pos += font_size	

		nline += 1
	
	return help_overlay


def createHelpScreen(text):
	""" Creates a help overlay surface containing the given text. """
	
	return createTextSurface(text, (255, 255, 0))


i_colors_cat = ((0,0,255), (255,128,0), (0,255,0),(255,0,0),(255,0,255), (255,255,0))

def colorsCategories():

	return i_colors_cat


def first_existing_directory(name, *dirs):
	""" Searches for a directory called by the given name inside all given
	directories, and returns the full path to the first one which exists. """
	
	for directory in dirs:
		if os.path.isdir(os.path.join(directory, name)):
			return os.path.join(directory, name)

def first_existing_location(file, directories):
	""" Searches for a file with the indicated name in the given directories
	and returns the path to the first place where it exist. """
	
	for directory in directories:
		filename = os.path.join(directory, file)
		if os.path.isfile(filename):
			return filename


class HelpOnScreen:
	
	_texts = {}
	sec_last_activity = -1
	sec_timeout = 10
	
	def next(self, event=None):
		""" This function updates the last date of user activity (key presses,
		etc). It should be called when a new page is first shown, and then
		each time there's an event. """
		
		if not event or event.is_user_action():
			self.sec_last_activity = time.time()
	
	def get_last_activity(self):
		""" Returns the timestamp of the last user activity. """
		
		return self.sec_last_activity
	
	def draw(self, surface, position, text):
		""" Draws the given text upon the indicated surface if a certain
		amount of time has ellapsed since the last user activity. """
		
		if time.time() >= (self.get_last_activity() + self.sec_timeout):
			if text not in self._texts:
				self._texts[text] = render_text(text, (128,128,128), 15, 1)
			surface.blit(self._texts[text], position)


class frameRate:
	""" Calculates the frame rate (FPS), limits it and, if choosen so, displays it on screen. """
	
	seconds = fps = fps_current = fps_limit = lastTicks = t_inici = 0
	textSurface = None
	
	def __init__(self, fps_limit = 0):
		self.fps_limit = fps_limit
		self.lastTicks = pygame.time.get_ticks()
		self.t_inici = time.time()
	
	def segons(self):
		return time.time() - self.t_inici

	def next(self, surface = None):
		
		if time.time() > self.seconds + 1:
			self.seconds = time.time()
			self.fps = self.fps_current
			self.fps_current = 0
			if Global.DISPLAY_FPS:
				self.textSurface = render_text('FPS: ' + if2(self.fps > 0,
					str(self.fps), 'N/a'), (128, 128, 128), 15, 1)
		else:
			self.fps_current += 1
		
		limit_fps = 1000 / self.fps_limit
		limit_ticks = pygame.time.get_ticks() - self.lastTicks
		
		if limit_ticks < limit_fps:
			pygame.time.wait(limit_fps - limit_ticks)
			self.lastTicks = pygame.time.get_ticks()

		if surface:	
			if self.textSurface and Global.DISPLAY_FPS:
				surface.blit(self.textSurface, (250, 740))


def maskimage (sourceimage, sourcemask):

	pygame.surfarray.pixels_alpha(sourceimage)[...] = pygame.surfarray.array_alpha(sourcemask)


def inkimage (sourceimage, color):

	mida = (sourceimage.get_width(), sourceimage.get_height())

	arraypunt = chr(color[0])+chr(color[1])+chr(color[2])+chr(color[3])
	
	impunt = pygame.image.fromstring(arraypunt, (1,1), "RGBA")

	impunt = pygame.transform.scale(impunt, mida)

	desti = pygame.Surface(mida, pygame.SRCALPHA, 32)
	desti.blit(sourceimage, (0,0))
	desti.blit(impunt, (0,0))

	pygame.surfarray.pixels_alpha(desti)[...] = pygame.surfarray.array_alpha(sourceimage)

	return desti


def if2(boolean, val1, val2):
	"""An 'a if b else c'-syntax replacement for Python 2.4."""

	if bool(boolean):
		return val1
	else:
		return val2
