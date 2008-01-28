#! /bin/sh

#
# Freevial
# Tarball Generator
#
# Copyright (C) 2007 The Freevial Team
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

if [ $# -ne 1 ]
then
	echo "Usage: $0 <version>"
	exit 1
fi

# Define variables
TMPDIR=/tmp/freevial-release
CURDIR=$(pwd)
VERSION=$1

# Create temporal directory
echo "Copying files..."
mkdir -p $TMPDIR/freevial-$VERSION

# Copy files
cp COPYING README ChangeLog freevial devscripts/distrib/* $TMPDIR/freevial-$VERSION
cp -r data/ src/ databases/ $TMPDIR/freevial-$VERSION

# Copy skins
mkdir -p $TMPDIR/freevial-$VERSION/skins/kde4
cp skins/kde4/* $TMPDIR/freevial-$VERSION/skins/kde4 2> /dev/null

# Remove unneeded stuff
cd $TMPDIR/freevial-$VERSION/src
rm -f *.pyc ./*/*.pyc *.~1~ ./*/*.~1~ .hidden ./*/.hidden

# Hardcode version
sed -i "s/VERSION = 'UNRELEASED'/VERSION = '$VERSION'/g" $TMPDIR/freevial-$VERSION/src/freevial.py

# Generate tarball
echo "Generating tarball..."
cd $TMPDIR
tar -czf freevial-$VERSION.tar.gz freevial-$VERSION

# Copy generated tarball
cd $CURDIR
if [ -e releases ]
then
	if [ ! -d ]; then
		echo "$0: error: can't create directory «releases», a file with the same name already exists."
		rm -rf $TMPDIR; exit 1
	fi
else
	mkdir releases
fi
cp $TMPDIR/freevial-$VERSION.tar.gz releases/

# Print a success message
echo "File «./releases/freevial-$VERSION.tar.gz» successfully generated."

# Clean up
echo "Cleaning up..."
cd $CURDIR
rm -rf $TMPDIR
