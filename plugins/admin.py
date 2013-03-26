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
import os
import sys
import hashlib
import globals

def reloadPlugins():
    newpluginNames = []

    for filename in os.listdir(globals.pluginDir):
        if filename.endswith(".py") and not filename.startswith("_"): # Only .py files not starting with _ are loaded
            newpluginNames.append(filename[:-3]) # Used slicing to make sure only the file extension is removed, even if ".py" occurs elsewhere in the string

    for name in newpluginNames:
        if not name in globals.pluginNames:
            globals.importedPlugins[name] = __import__(name)
    
    for plugin in globals.importedPlugins.values():
        reload(plugin)
    
    for name in globals.pluginNames:
        if not name in newpluginNames:
            del globals.importedPlugins[name]
            del sys.modules[name]
    
    globals.pluginNames = newpluginNames

def run(eventname, connection, event):   
    if eventname == "privmsg":
        name = event.source().split('!')[0] # format of event.source() is name!user@host
        message = event.arguments()[0]
        # Handle authorization
        if(message.split(' ')[0].lower() == "auth"):
            if len(message.split(' ')) != 2:
                connection.privmsg(name, "Usage: auth <password>")
            else:
                passhash = hashlib.md5(message.split()[1])
                digested = passhash.digest()
                if digested == globals.authPassHash:
                    if name in globals.authorizedUsers:
                        connection.privmsg(name, "You are already authorized!")
                    else:
                        globals.authorizedUsers.append(name)
                        connection.privmsg(name, "You've been successfully authorized!")
                else:
                    connection.privmsg(name, "Invalid password!")
        # Handle reloading modules
        elif(message.split(' ')[0].lower() == "reload"):
            if name in globals.authorizedUsers:
                reloadPlugins()
                connection.privmsg(name, "Modules reloaded!")
            else:
                connection.privmsg(name, "You're not authorized to do that!")
        elif(message.split(' ')[0].lower() == "quit"):
            if name in globals.authorizedUsers:
                globals.keeprunning = False
                connection.disconnect("My master has killed me!")
            else:
                connection.privmsg(name, "You're not authorized to do that!")
    elif eventname == "nick":
        oldNick = event.source().split('!')[0]
        newNick = event.target()
        
        if oldNick in globals.authorizedUsers:
            # Update the nick of the authorized user
            index = globals.authorizedUsers.index(oldNick)
            globals.authorizedUsers[index] = newNick
        elif newNick in globals.authorizedUsers:
            # Remove the nick of the authorized user - should never happen, but just in case!
            index = globals.authorizedUsers.index(newNick)
            globals.authorizedUsers = globals.authorizedUsers[:index] + globals.authorizedUsers[index+1:]
    elif eventname == "kick":    
        nick = event.arguments()[0]
        
        if nick in globals.authorizedUsers:
            # Remove the nick of the kicked user - there's no way to tell if the next occurrence of this nick is the same user
            index = globals.authorizedUsers.index(nick)
            globals.authorizedUsers = globals.authorizedUsers[:index] + authorizedUsers[index+1:]
    elif eventname == "quit":
        nick = event.source().split('!')[0]
    
        if nick in globals.authorizedUsers:
            index = globals.authorizedUsers.index(nick)
            globals.authorizedUsers = globals.authorizedUsers[:index] + globals.authorizedUsers[index+1:]
    elif eventname == "part":
        nick = event.source().split('!')[0]
    
        if nick in globals.authorizedUsers:
            index = globals.authorizedUsers.index(nick)
            globals.authorizedUsers = globals.authorizedUsers[:index] + globals.authorizedUsers[index+1:]
