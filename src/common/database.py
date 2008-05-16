# -*- coding: utf-8 -*-

#
# Freevial
# Database Class
#
# Copyright (C) 2007, 2008 The Freevial Team
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

from random import shuffle, sample, randint
from copy import deepcopy
import gettext

class Database:
	
	def __init__( self, num, name, language, description, players, authors, time, image, sound, version ):
		
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

		self.version = version
		
		# Questions
		self._questions = []
		self._old_questions = []
		
		# Internal Variables
		self._shuffled = False
	
	def __len__( self ):
		""" Returns the total amount of questions in this database. """
		
		return len( self._questions ) + len( self._old_questions )
	
	def _shuffle( self ):
		""" Shuffles the question list. """
		
		shuffle(self._questions)

		self._shuffled = True
	
	def _get_question( self ):
		""" Returns the next question in a list, where the first answer
		    is the correct one. """
		
		if len(self._questions) == 0:
			print _(u'All questions in category «%s» have been answered. Reshuffling...') %  self.name
			self._questions = deepcopy(self._old_questions)
			self._old_questions = []
			self._shuffled = False
		
		if not self._shuffled:
			self._shuffle()
		
		self._old_questions.append( self._questions.pop() )
		
		return self._old_questions[-1]
	
	def addQuestion( self, question, answ1, answ2, answ3, author, comment, mediatype, media, difficulty):
		
		self._questions.append( [question, answ1, answ2, answ3, 1, author, comment, mediatype, media, difficulty] )
	
	def question( self ):
		""" Returns the next question in a dictionary (with the answers
		    in a random position). """
		
		data = self._get_question()
		answer_order = sample(xrange(1, 4), 3)
		
		question = {}
		question['text'] = data[0]
		question['opt1'] = data[answer_order[0]]
		question['opt2'] = data[answer_order[1]]
		question['opt3'] = data[answer_order[2]]
		question['answer'] = answer_order.index(1) + 1
		question['author'] = data[5]
		question['comment'] = data[6]
		question['mediatype'] = data[7]
		question['media'] = data[8]

		return question
