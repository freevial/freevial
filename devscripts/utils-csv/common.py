#! /usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################
#
# Freevial Utilities (support file)
# Common stuff used by other utilities
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

import os

def files_in_dir(path, extension=''):
	""" Returns a list with the path to all files in the given directory that match the indicated extension. """
	
	if not os.path.isdir(path):
		raise ValueError, 'Path «%s» does not exists or is not a directory.' % path
	
	file_list = []
	
	for root, dirs, files in os.walk(path):
		for file in files:
			if extension != '' and file[(-len(extension)):] != extension:
				continue
			else:
				file_list.append(os.path.normpath(os.path.join(root, file)))
	
	return file_list
