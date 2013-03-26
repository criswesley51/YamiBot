"""
    This file is part of YamiBot.

    YamiBot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    YamiBot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with YamiBot.  If not, see <http://www.gnu.org/licenses/>.
    
    Copyright Nash van Gool 2013 <darealnash@gmail.com>
"""

#! /usr/bin/env python

import sys
import hashlib

passstring = raw_input("Please enter your desired password: ")
passcheck = raw_input("Please re-enter your desired password: ")

while not passstring == passcheck:
    print "Passwords do not match!"
    passstring = raw_input("Please enter your desired password: ")
    passcheck = raw_input("Please re-enter your desired password: ")

passfile = None
try:
    passfile = open("password.md5", "w")
except IOError, e:
    print "Error opening file: ", e
    sys.exit()

passhash = hashlib.md5(passstring)
hashstring = passhash.digest()

passfile.write(hashstring)
