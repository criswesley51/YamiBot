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

import irclib

def run(eventname, connection, event):
    if not eventname == "privmsg": return
    
    nick = event.source().split('!')[0]
    message = event.arguments()[0]
    
    if message.lower() == "hello":
        connection.privmsg(nick, "Hi!")
