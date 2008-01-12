#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-
 
#
# Freevial
# Database Conversor: CSV -> XML
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

import os
import sys
import csv
from lxml import etree, objectify
import time
import gettext

sys.path.extend((os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), '../../src/common/'), '/usr/share/games/freevial/src/common'))
from database import Database

#######################################################################

# Check command line parameters
if len(sys.argv) != 2 or sys.argv[1] in ('-h', '--help', 'help'):
	print 'Usage: %s <CSV file>' % sys.argv[0]
	sys.exit(1)

# Check if the indicated file exists
if not os.path.isfile(sys.argv[1]):
	print 'File «%s» doesn\'t exist, or it isn\'t a file.»' % sys.argv[1]
	sys.exit(1)

# Check if it seems a CSV file
if sys.argv[1][-4:] != '.csv':
	print 'Only CSV files are accepted. If «%s» is a CSV file, rename it in order that it ends with ".csv".' % sys.argv[1]
	sys.exit(1)

#######################################################################

def GetDatabase( csvFile ):
	""" Returns a Database instance with the questions from a CSV file. """
	
	csv_read = csv.reader( open( csvFile ) )
	
	comptaline  = 0
	error_count = 0
	
	for line in csv_read:
		
		comptaline += 1
		
		if comptaline > 16:
			
			if len(line) < 9:
				print 'Error in database file «%s», line %d: expected %d values, found %d.' % (os.path.basename(csvFile), comptaline, 10, len(line))
				error_count += 1
				
				if error_count < 3:
					continue
				else:
					print 'Found 3 problems, this will abort the game.'
					sys.exit(1)
			elif len(line) == 9:
				line.append('')
			
			for num in range(0, 10):
				line[ num ] = unicode(line[ num ], 'utf-8')
			
			for num in (5, 8):
				try:
					line[ num ] = int(line[ num ])
				except ValueError:
					line[ num ] = 0
			
			database.addQuestion(
				question = line[1],
				answ1 = line[1 + line[5]],
				answ2 = line[3] if line[5] != 2 else line[2],
				answ3 = line[4] if line[5] != 3 else line[2],
				author = line[6],
				comment = line[9],
				)
		
		# Get information from the header lines
		elif comptaline == 1: continue
		elif comptaline == 2: name = unicode( line[1], 'utf-8' )
		elif comptaline == 3: time = [ unicode( line[1], 'utf-8' ) ]
		elif comptaline == 4: time.append( unicode( line[1], 'utf-8' ) )
		elif comptaline == 5: authors = unicode( line[1], 'utf-8' )
		elif comptaline == 6: description = unicode( line[1], 'utf-8' )			
		elif comptaline == 7: players = unicode( line[1], 'utf-8' )
		elif comptaline == 8: language = unicode( line[1], 'utf-8' )
		elif comptaline == 9: image = unicode( line[1], 'utf-8' )
		elif comptaline == 10:
			sound = unicode( line[1], 'utf-8' )
			database = Database( 1, name, language, description, players, authors, time, image, sound )
	
	return database

#######################################################################

# Load CSV file into an instance of the Database class
database = GetDatabase(sys.argv[1])

# Create the XML parser
parser = etree.XMLParser(remove_blank_text = True)
parser.setElementClassLookup(objectify.ObjectifyElementClassLookup())

xmlobject = parser.makeelement('database')
xml_info = etree.SubElement(xmlobject, 'information')
xml_appe = etree.SubElement(xmlobject, 'appearance')
xml_questions = etree.SubElement(xmlobject, 'questions')

xmlobject.set('version', '1.0')
xmlobject.set('id', database.name)
xmlobject.set('language', database.language)

etree.SubElement(xml_info, 'name')
etree.SubElement(xml_info, 'description')
etree.SubElement(xml_info, 'destination')
etree.SubElement(xml_info, 'timestamp_creation')
etree.SubElement(xml_info, 'timestamp_modification')
etree.SubElement(xml_info, 'authors')

xml_info.name = database.name
xml_info.description = database.description
xml_info.destination = database.players
xml_info.timestamp_creation = int(time.mktime(time.strptime(database.time[0], "%d/%m/%y")))
xml_info.timestamp_modification = int(time.time())

for (i, author) in enumerate(database.authors.split(', ')):
	etree.SubElement(xml_info.authors, 'author')
	xml_info.authors.author[i] = '%s, <email>' % author

etree.SubElement(xml_appe, 'image')
etree.SubElement(xml_appe, 'sound')

xml_appe.image = database.image
xml_appe.sound = database.sound

# Don't shuffle the database, we like it how it is
database._shuffled = True

for i in range(0, len(database)):
	
	# Get question data
	question = database.question()
	
	xml_question = etree.SubElement(xml_questions, 'question')
	
	etree.SubElement(xml_question, 'sentence')
	etree.SubElement(xml_question, 'author')
	etree.SubElement(xml_question, 'comments')
	etree.SubElement(xml_question, 'answers')
	
	xml_question.sentence = question['text']
	xml_question.author = question['author']
	xml_question.comments = question['comment']
	
	answs = range(0, 3)
	answs[0] = question['opt' + str(question['answer'])]
	answs[1] = question['opt1'] if question['answer'] != 1 else question['opt2']
	answs[2] = question['opt3'] if question['answer'] != 3 else question['opt2']
	
	for j in range(0, 3):
		etree.SubElement(xml_question.answers, 'answer')
		xml_question.answers.answer[j] = answs[j]
	
	xml_question.answers.answer[0].set('correct', 'True')

print etree.tostring(xmlobject, encoding='utf-8', pretty_print=True)
