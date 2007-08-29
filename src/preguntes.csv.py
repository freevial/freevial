# -*- coding: utf-8 -*-
 
##########################################
#
# Freevial
# Preguntes
#
# RainCT 28/08/2007
#

import csv
from freevialglob import *

preguntes = csv_questions = []

csv_read = csv.reader( open('../preguntes.csv') )

seen_header = 0
for csv_line in csv_read:
	if seen_header == 0:
		seen_header = 1; continue
	
	for num in range(0, 9):
		csv_line[ num ] = unicode(csv_line[ num ], 'utf-8')
	
	for num in (0, 5, 9):
		csv_line[ num ] = int(csv_line[ num ])
	
	csv_questions.append(csv_line)

for num in range(0, 6):
	preguntes.append( [] )

for element in csv_questions:
	if len(element) == 0: continue
	
	preguntes[ element[0] - 1 ].append( element )

# Copy the questions to get them back if a categories gets empty
preguntes_backup = preguntes

preguntes = shuffleQuestions(preguntes)
