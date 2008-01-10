#! /usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################
#
# Freevial Utilities
# Count the amount of questions in a database
#
# Copyright (C) 2007 Siegfried-Angel Gevatter Pujals
# By Siegfried-Angel Gevatter Pujals (RainCT) <siggi.gevatter@gmail.com>
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
#######################################################

import sys, csv
from common import files_in_dir

def countDirectory(path):
	""" Counts the total amount of questions in a database for Freevial """
	
	try:
		file_list = files_in_dir(path, '.csv')
		
	except ValueError, (errno, strerr):
		print strerr
		sys.exit(1)
	
	data = {
			'total_files': len(file_list),
		}
	
	total_questions = 0
	for file in file_list:
		filedata = countFile(file)
		total_questions += filedata[1]
		data[filedata[0]] = filedata[1]
	
	data['total_questions'] = total_questions
	
	return data

def countFile(filename):
	""" Counts the amount of questions in a Freevial .csv file """
	
	# Read File
	csvfile = csv.reader(open(filename))
	
	# Initialize variables
	i = 1
	questions = 0
	name = None
	
	# Count questions
	for line in csvfile:
		
		if i > 14:
			questions += 1
		elif i == 2:
			name = line[1]
		
		i += 1
	
	# Return the number of questions in this file
	return [name, questions]

if __name__ == '__main__':
	
	if len(sys.argv) < 2:
		print "Usage: %s <path to the database>" % sys.argv[0]
		sys.exit(0)
	
	data = countDirectory(sys.argv[1])
	
	print 'Found %d categories, containg a total amount of %d questions.' % (data['total_files'], data['total_questions'])
	
	for key in data:
		if key not in ('total_files', 'total_questions'):
			print "%s: %d" % (key, data[key])
