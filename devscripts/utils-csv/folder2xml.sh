#! /bin/bash
 
#
# Freevial
# Database Conversor: CSV -> XML
# This script runs csv2xml.py for alk CSV files in a given folder
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

if [ ! -x ./csv2xml.py ]
then
	echo "Please run this script from inside the «devscripts/utils-csv/» directory."
	exit 1
fi

if [ -z "$1" ] || [ "$1" == '-h' ] || [ "$1" == '--hepl' ] || [ "$1" == 'help' ]
then
	echo "Usage: $0 <database folder>"
	exit 1
fi

for file in $1/*.csv
do
	if [ "$file" != "$1/*.csv" ]
	then
		echo "Converting file «$file»..."
		./csv2xml.py $file > ${file%.*}.xml
		rm $file 
	fi
done
