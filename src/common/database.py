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

class Question:
	
	def __init__(self, question=None, author=None):
		
		# Public Variables
		self.question = question
		self.author = author
		self.comment = u''
		self.mediatype = None
		self.media = None
		self.difficulty = 'Medium'
		
		# Internal Variables
		self._correct_answers = []
		self._wrong_answers = []
	
	def add_answer(self, text, correct=False):
		
		if correct:
			self._correct_answers.append(text)
		else:
			self._wrong_answers.append(text)
	
	def get_answers(self):
		
		if len(self._wrong_answers) == 1:
			i = 1
		else:
			i = 2
		
		return sample(self._correct_answers, 1) + sample(self._wrong_answers, i)

class Database:
	
	def __init__(self, name, language, description, players, authors, time, image, sound, version):
		
		# General Database Data
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
	
	def __len__(self):
		""" Returns the total amount of questions in this database. """
		
		return len(self._questions) + len(self._old_questions)
	
	def _shuffle(self):
		""" Shuffles the question list. """
		
		shuffle(self._questions)

		self._shuffled = True
	
	def _get_question(self):
		""" Returns the next question in a list, where the first answer
			is the correct one. """
		
		if len(self._questions) == 0:
			print _(u'All questions in category «%s» have been answered. Reshuffling...') %  self.name
			self._questions = deepcopy(self._old_questions)
			self._old_questions = []
			self._shuffled = False
		
		if not self._shuffled:
			self._shuffle()
		
		self._old_questions.append(self._questions.pop())
		
		return self._old_questions[-1]
	
	def add_question(self, obj):
		
		self._questions.append(obj)
	
	def question(self):
		""" Returns the next question in a dictionary (with the answers
			in a random position). """
		
		data = self._get_question()
		answers = data.get_answers()
		answer_order = sample(xrange(0, len(answers)), len(answers))
		
		question = {}
		question['text'] = data.question
		question['options'] = tuple((answers[answer_order[num]] for num in xrange(0, len(answers))))
		question['answer'] = answer_order.index(0)
		question['author'] = data.author
		question['comment'] = data.comment
		question['mediatype'] = data.mediatype
		question['media'] = data.media
		
		return question
