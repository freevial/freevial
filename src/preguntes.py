# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Preguntes
#
# Carles 24/08/2007
# RainCT
#

import csv
from freevialglob import *


def shuffleQuestions( questions ):
	""" Returns the given questions list, but shuffled. """
	
	for num in range(0, 6):
		random.shuffle( questions[num] )
	
	return questions


def importQuestions( csvFile ):
	""" Imports the questions from a CSV file and returns them in a list. """
	
	questions = []
	seen_header = 0
	
	csv_read = csv.reader( open( csvFile ) )
	
	for line in csv_read:
		
		# skip the header (first line)
		if seen_header == 0:
			seen_header = 1; continue
		
		for num in range(0, 9):
			line[ num ] = unicode(line[ num ], 'utf-8')
		
		for num in (0, 5, 9):
			line[ num ] = int(line[ num ])
		
		questions.append(line)
	
	return questions


###########################################

csv_questions = importQuestions('../preguntes.csv')
preguntes = []
preguntes_autors = []

for num in range(0, 6):
	# Add a list for each category
	preguntes.append( [] )

for element in csv_questions:
	
	if element[6] not in preguntes_autors:
		preguntes_autors.append( element[6] )
	
	preguntes[ element[0] - 1 ].append( element )

# Copy the questions to get them back if a categories gets empty
preguntes_backup = preguntes

preguntes = shuffleQuestions(preguntes)
