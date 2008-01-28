#! /bin/sh

#
# Freevial
# Installation Script
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

PREFIX="$1"

BIN="/usr/games"
BASE="/usr/share/games/freevial"

mkdir -p $PREFIX/$BIN
mkdir -p $PREFIX/$BASE
mkdir -p $PREFIX/$BASE/data
mkdir -p $PREFIX/$BASE/data/fonts
mkdir -p $PREFIX/usr/share/pixmaps
mkdir -p $PREFIX/usr/share/applications

cp freevial $PREFIX/$BIN/
cp -r src $PREFIX/$BASE/
cp -r databases $PREFIX/$BASE/

cp data/skin.ini $PREFIX/$BASE/data/
cp -r data/help $PREFIX/$BASE/data/
cp -r data/images $PREFIX/$BASE/data/
cp -r data/sounds $PREFIX/$BASE/data/
cp data/fonts/Ubuntu-Title.ttf $PREFIX/$BASE/data/fonts/

cp data/extra/freevial.xpm $PREFIX/usr/share/pixmaps/
cp data/images/freevial.png $PREFIX/usr/share/pixmaps/
cp data/extra/freevial.desktop $PREFIX/usr/share/applications/
