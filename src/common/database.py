# -*- coding: utf-8 -*-

#
# Freevial
# Database Class
#
# Copyright (C) 2007 The Freevial Team
#
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

from random import shuffle
from copy import deepcopy
import gettext

class Database:
	
	def __init__( self, num, name, language, description, players, authors, time, image, sound ):
		
		# General Database Data
		self.num = num	# provisional, should be removed soon
		self.name = unicode(name)
		self.language = unicode(language)
		self.description = unicode(description)
		self.players = unicode(players)
		self.authors = unicode(authors)
		self.time = [ time[0], time[1] ]
		self.image = image
		self.sound = sound
		
		# Questions
		self._questions = []
		self._old_questions = []
		
		# Internal Variables
		self._shuffled = False
	
	def __len__( self ):
		""" Returns the amount of questions. """
		
		return len( self._questions ) + len( self._old_questions )
	
	def _shuffle( self ):
		""" Shuffles the question list. """
		
		shuffle(self._questions)
		self._shuffled = True
	
	def addQuestion( self, question, answ1, answ2, answ3, author, comments, time ):
		
		self._questions.append( [ question, answ1, answ2, answ3, 1, author, comments, time ] )
	
	def question( self ):
		
		if len(self._questions) == 0:
			print _('All questions have been answered. Reshuffling...')
			self._questions = deepcopy(self._old_questions)
			self._old_questions = []
			self.shuffled = False
		
		if not self._shuffled:
			self._shuffle()
		
		self._old_questions.append( self._questions.pop() )
		
		# provisional, self.num should be deprecated
		retval = self._old_questions[-1]
		retval.insert(0, self.num)
		return retval
	
	def currentQuestionNumber( self ):
		
		return len(self._old_questions)
