#! /usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################
#
# Freevial Utilities
# Search duplicate questions in a questions database
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

import sys, csv, os.path
from common import files_in_dir

if len(sys.argv) < 2:
	print "Usage: %s <path to the database>" % sys.argv[0]
	sys.exit(0)

path = sys.argv[1]

try:
	file_list = files_in_dir(path, '.csv')

except ValueError, (errno, strerr):
	print strerr
	sys.exit(1)

for filename in file_list:
	# Read File
	csvfile = csv.reader(open(filename))
	
	# Initialize variables
	questions = {}
	linenum = 0
	
	# Count questions
	for line in csvfile:
		linenum += 1
		if linenum > 14:
			if line[1] not in questions:
				questions[line[1]] = linenum
			else:
				print "%s (line %d, %d): «%s»" % (os.path.basename(filename), questions[line[1]], linenum, line[1])
