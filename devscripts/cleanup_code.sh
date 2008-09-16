#! /bin/sh

#
# Freevial
# Code Cleanup Script
#
# Copyright (C) 2008 The Freevial Team
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

FILES="src/*.py src/*/*.py"
TMPDIR="/tmp/freevial-cleanup"

# Ensure that we are in the right directory
if [ -x freevial ] && [ -d src ] && [ -d src/common ] && [ -d devscripts ]
then
	echo "Cleaning up source... $(pwd)"
else
	echo "Please ensure that you are in the right directory."
	exit 1
fi

# Fix indentation (convert "four space"-blocks at the start of a line to tabs)
[ -d $TMPDIR ] && rm -r $TMPDIR; mkdir -p $TMPDIR
for file in $FILES
do
	tmpfile="$TMPDIR/$(basename $file)"
	cp $file $tmpfile; unexpand -t 4 --first-only $tmpfile > $file
done
rm -r $TMPDIR

# Change "( ... )" to "(...)"
sed -r -i 's/\([ \t]+/\(/' $FILES
sed -r -i 's/[ ]+\)/\)/' $FILES # Not matching tabs is intentional.

# Remove backup files
find | grep \~ | xargs rm

echo "Done!"
