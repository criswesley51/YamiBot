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

#! /usr/bin/python

# Global variables for use by the bot
import globals

# Load the config files
conffile = None
passfile = None

try:
    conffile = open("yamibot.conf", "r")
except IOError, e:
    print "Error opening config file: ", e
    globals.serverData = { "network": "irc.example.com", "port": 6667, "nick": "YamiBot", "name": "YamiIRC Bot" }
    globals.pluginDir = "plugins"
except:
    print "Error handling config file: ", e
else:
    try:
        lines = conffile.readlines()
        for line in lines:
            while '\n' in line: line = line.replace('\n', '')
            while '\r' in line: line = line.replace('\r', '')
            params = line.split()
            if params[0] == "SERVER:": 
                print "SERVER:", params[1]     
                globals.serverData["network"] = params[1]
            if params[0] == "PORT:":        
                print "PORT:", params[1]
                globals.serverData["port"] = int(params[1])
            if params[0] == "NICK:":        
                print "NICK:", params[1]
                globals.serverData["nick"] = params[1]
            if params[0] == "NAME:":        
                fullname = ""
                for param in params[1:]:
                    fullname += ' '
                    fullname += param
                fullname = fullname.lstrip()
                globals.serverData["name"] = fullname
            if params[0] == "PLUGINDIR:":   
                print "PLUGINDIR:", params[1]
                globals.pluginDir = params[1]
            if params[0] == "CHANNELS:":     
                print "CHANNELS:", params[1:]
                globals.serverData["channels"] = params[1:]
        conffile.close()
    except IndexError:
        print "Invalid config file format!"

print "FINAL CONFIG DATA:"
print "SERVER:", globals.serverData
print "PLUGINS:", globals.pluginDir

try:
    passfile = open("password.md5", "r")
except IOError, e:
    print "Error opening password file: ", e
except:
    print "Error handling password file: ", e
else:
    globals.authPassHash = passfile.read()
    passfile.close()

print "Read pass hash:", globals.authPassHash

# Provide code to load and reload all plugins, and load all plugins at start
import os
import sys

for filename in os.listdir(globals.pluginDir):
    if filename.endswith(".py") and not filename.startswith("_"): # Only .py files not starting with _ are loaded
        globals.pluginNames.append(filename[:-3]) # Used slicing to make sure only the file extension is removed, even if ".py" occurs elsewhere in the string

sys.path.append(globals.pluginDir) # Make sure our program can look in the plugins directory

for name in globals.pluginNames:
    globals.importedPlugins[name] = __import__(name)


# Use python-irclib for connection code
import irclib

# Debugging version - set this to False if you don't want to debug
irclib.DEBUG = False

# Create IRC object
irc = irclib.IRC()

# This code passes events to every available plugin
def passToPlugins(eventname, connection, event):
    for plugin in globals.importedPlugins.values():
        try:
            plugin.run(eventname, connection, event)
        except:
            err = sys.exc_info()
            print "DEBUG: Error in plugin", plugin
            print "DEBUG: Error type:", err[0]
            print "DEBUG: Error description:", err[1]
            print "DEBUG: Please check the file for errors!"

# Code below makes sure all events are passed through to plugins - do not modify any code below, instead define behavior in plugins
def handlePrivMsg(connection, event):
    passToPlugins("privmsg", connection, event)

def handleNickChange(connection, event):
    passToPlugins("nick", connection, event)

def handleKick(connection, event):
    passToPlugins("kick", connection, event)

def handleQuit(connection, event): 
    passToPlugins("quit", connection, event)

def handlePart(connection, event):
    passToPlugins("part", connection, event)

def handleStatsKLine(connection, event):
    passToPlugins("statskline", connection, event)

def handleStatsQLine(connection, event):
    passToPlugins("statsqline", connection, event)

def handleStatsNLine(connection, event):
    passToPlugins("statsnline", connection, event)

def handleStatsILine(connection, event):
    passToPlugins("statsiline", connection, event)

def handleStatsCommands(connection, event):
    passToPlugins("statscommands", connection, event)

def handleStatsCLine(connection, event):
    passToPlugins("statscline", connection, event)

def handleTraceReconnect(connection, event):
    passToPlugins("tracereconnect", connection, event)

def handleStatsLinkInfo(connection, event):
    passToPlugins("statslinkinfo", connection, event)

def handleStatsYLine(connection, event):
    passToPlugins("statsyline", connection, event)

def handleEndOfStats(connection, event):
    passToPlugins("endofstats", connection, event)

def handleNoOperHost(connection, event):
    passToPlugins("nooperhost", connection, event)

def handleNoServiceHost(connection, event):
    passToPlugins("noservicehost", connection, event)

def handleTooManyTargets(connection, event):
    passToPlugins("toomanytargets", connection, event)

def handleWasNoSuchNick(connection, event):
    passToPlugins("wasnosuchnick", connection, event)

def handleInviteList(connection, event):
    passToPlugins("invitelist", connection, event)

def handleEndOfInviteList(connection, event):
    passToPlugins("endofinvitelist", connection, event)

def handleNoSuchChannel(connection, event):
    passToPlugins("nosuchchannel", connection, event)

def handleInviting(connection, event):
    passToPlugins("inviting", connection, event)

def handleSummoning(connection, event):
    passToPlugins("summoning", connection, event)

def handleExceptList(connection, event):
    passToPlugins("exceptlist", connection, event)

def handleEndOfExceptList(connection, event):
    passToPlugins("endofexceptlist", connection, event)

def handleNoOrigin(connection, event):
    passToPlugins("noorigin", connection, event)

def handleTryAgain(connection, event):
    passToPlugins("tryagain", connection, event)

def handleEndOfTrace(connection, event):
    passToPlugins("endoftrace", connection, event)

def handleTraceLog(connection, event):
    passToPlugins("tracelog", connection, event)

def handleNGlobal(connection, event):
    passToPlugins("n_global", connection, event)

def handleNLocal(connection, event):
    passToPlugins("n_local", connection, event)

def handleNotOnChannel(connection, event):
    passToPlugins("notonchannel", connection, event)

def handleNoAdminInfo(connection, event):
    passToPlugins("noadmininfo", connection, event)

def handleNoMOTD(connection, event):
    passToPlugins("nomotd", connection, event)

def handleFileError(connection, event):
    passToPlugins("fileerror", connection, event)

def handleWildTopLevel(connection, event):
    passToPlugins("wildtoplevel", connection, event)

def handleUnavailResource(connection, event):
    passToPlugins("unavailresource", connection, event)

def handleNoRecipient(connection, event):
    passToPlugins("norecipient", connection, event)

def handleNoTextToSend(connection, event):
    passToPlugins("notexttosend", connection, event)
    
def handleNoTopLevel(connection, event):
    passToPlugins("notoplevel", connection, event)

def handleInfo(connection, event):
    passToPlugins("info", connection, event)

def handleInfoStart(connection, event):
    passToPlugins("infostart", connection, event)

def handleMOTD(connection, event):
    passToPlugins("motd", connection, event)

def handleMOTDStart(connection, event):
    passToPlugins("motdstart", connection, event)

def handleEndOfInfo(connection, event):
    passToPlugins("endofinfo", connection, event)

def handleMOTD2(connection, event):
    passToPlugins("motd2", connection, event)

def handleEndOfMOTD(connection, event):
    passToPlugins("endofmotd", connection, event)

def handleWhoisChannels(connection, event):
    passToPlugins("whoischannels", connection, event)

def handleEndOfWhois(connection, event):
    passToPlugins("endofwhois", connection, event)

def handleWhoisOperator(connection, event):
    passToPlugins("whoisoperator", connection, event)

def handleWhoisServer(connection, event):
    passToPlugins("whoisserver", connection, event)

def handleWhoisUser(connection, event):
    passToPlugins("whoisuser", connection, event)

def handleWhoisIdle(connection, event):
    passToPlugins("whoisidle", connection, event)

def handleWhoisChanop(connection, event):
    passToPlugins("whoischanop", connection, event)

def handleEndOfWho(connection, event):
    passToPlugins("endofwho", connection, event)

def handleWhoWasUser(connection, event):
    passToPlugins("whowasuser", connection, event)

def handleUsers(connection, event):
    passToPlugins("users", connection, event)

def handleUsersStart(connection, event):
    passToPlugins("usersstart", connection, event)

def handleTime(connection, event):
    passToPlugins("time", connection, event)

def handleNoUsers(connection, event):
    passToPlugins("nousers", connection, event)

def handleEndOfUsers(connection, event):
    passToPlugins("endofusers", connection, event)

def handleUserOnChannel(connection, event):
    passToPlugins("useronchannel", connection, event)

def handleEndOfBanList(connection, event):
    passToPlugins("endofbanlist", connection, event)

def handleEndOfWhoWas(connection, event):
    passToPlugins("endofwhowas", connection, event)

def handleEndOfNames(connection, event):
    passToPlugins("endofnames", connection, event)

def handleBanList(connection, event):
    passToPlugins("banlist", connection, event)

def handleLinks(connection, event):
    passToPlugins("links", connection, event)

def handleEndOfLinks(connection, event):
    passToPlugins("endoflinks", connection, event)

def handleClosing(connection, event):
    passToPlugins("closing", connection, event)

def handleCloseEnd(connection, event):
    passToPlugins("closeend", connection, event)

def handleKillDone(connection, event):
    passToPlugins("killdone", connection, event)

def handleNone(connection, event):
    passToPlugins("none", connection, event)

def handleAway(connection, event):
    passToPlugins("away", connection, event)

def handleUserHost(connection, event):
    passToPlugins("userhost", connection, event)

def handleIsOn(connection, event):
    passToPlugins("ison", connection, event)

def handleUnAway(connection, event):
    passToPlugins("unaway", connection, event)

def handleNowAway(connection, event):
    passToPlugins("nowaway", connection, event)

def handleNoLogin(connection, event):
    passToPlugins("nologin", connection, event)

def handleStatsHLine(connection, event):
    passToPlugins("statshline", connection, event)

def handleRehashing(connection, event):
    passToPlugins("rehashing", connection, event)

def handleStatsLLine(connection, event):
    passToPlugins("statslline", connection, event)

def handleSummonDisabled(connection, event):
    passToPlugins("summondisabled", connection, event)

def handleStatsOLine(connection, event):
    passToPlugins("statsoline", connection, event)

def handleStatsUptime(connection, event):
    passToPlugins("statsuptime", connection, event)

def handleYoureOper(connection, event):
    passToPlugins("youreoper", connection, event)

def handleNickCollision(connection, event):
    passToPlugins("nickcollision", connection, event)

def handleMyPortIs(connection, event):
    passToPlugins("myportis", connection, event)

def handleErroneusNickname(connection, event):
    passToPlugins("erroneusnickname", connection, event)

def handleNicknameInUse(connection, event):
    passToPlugins("nicknameinuse", connection, event)

def handleNoNicknameGiven(connection, event):
    passToPlugins("nonicknamegiven", connection, event)

def handleNotRegistered(connection, event):
    passToPlugins("notregistered", connection, event)

def handleNoTopic(connection, event):
    passToPlugins("notopic", connection, event)

def handleTopicInfo(connection, event):
    passToPlugins("topicinfo", connection, event)

def handleTopic(connection, event):
    passToPlugins("topic", connection, event)

def handleAdminLoc2(connection, event):
    passToPlugins("adminloc2", connection, event)

def handleAdminEmail(connection, event):
    passToPlugins("adminemail", connection, event)

def handleLUserOp(connection, event):
    passToPlugins("luserop", connection, event)

def handleLUserUnknown(connection, event):
    passToPlugins("luserunknown", connection, event)

def handleLUserConns(connection, event):
    passToPlugins("luserconns", connection, event)

def handleLUserClient(connection, event):
    passToPlugins("luserclient", connection, event)

def handleAdminMe(connection, event):
    passToPlugins("adminme", connection, event)

def handleAdminLoc1(connection, event):
    passToPlugins("adminloc1", connection, event)

def handleLUserChannels(connection, event):
    passToPlugins("luserchannels", connection, event)

def handleLUserMe(connection, event):
    passToPlugins("luserme", connection, event)

def handleTooManyChannels(connection, event):
    passToPlugins("toomanychannels", connection, event)

def handleCannotSendToChan(connection, event):
    passToPlugins("cannotsendtochan", connection, event)

def handleUsersDontMatch(connection, event):
    passToPlugins("usersdontmatch", connection, event)

def handleNoSuchServer(connection, event):
    passToPlugins("nosuchserver", connection, event)

def handleNoSuchNick(connection, event):
    passToPlugins("nosuchnick", connection, event)

def handleYoureBannedCreep(connection, event):
    passToPlugins("yourebannedcreep", connection, event)

def handlePasswdMismatch(connection, event):
    passToPlugins("passwdmismatch", connection, event)

def handleKeyset(connection, event):
    passToPlugins("keyset", connection, event)

def handleYouWillBeBanned(connection, event):
    passToPlugins("youwillbebanned", connection, event)

def handleNeedMoreParams(connection, event):
    passToPlugins("needmoreparams", connection, event)

def handleNoPermForHost(connection, event):
    passToPlugins("nopermforhost", connection, event)

def handleAlreadyRegistered(connection, event):
    passToPlugins("alreadyregistered", connection, event)

def handleUModeIs(connection, event):
    passToPlugins("umodeis", connection, event)

def handleUsersDisabled(connection, event):
    passToPlugins("usersdisabled", connection, event)

def handleUModeUnknownFlag(connection, event):
    passToPlugins("umodeunknownflag", connection, event)

def handleServList(connection, event):
    passToPlugins("servlist", connection, event)

def handleServListEnd(connection, event):
    passToPlugins("servlistend", connection, event)

def handleServiceInfo(connection, event):
    passToPlugins("serviceinfo", connection, event)

def handleEndOfServices(connection, event):
    passToPlugins("endofservices", connection, event)

def handleService(connection, event):
    passToPlugins("service", connection, event)

def handleUserNotInChannel(connection, event):
    passToPlugins("usernotinchannel", connection, event)

def handleList(connection, event):
    passToPlugins("list", connection, event)

def handleListEnd(connection, event):
    passToPlugins("listend", connection, event)

def handleListStart(connection, event):
    passToPlugins("liststart", connection, event)

def handleChannelModeIs(connection, event):
    passToPlugins("channelmodeis", connection, event)

def handleBadChanMask(connection, event):
    passToPlugins("badchanmask", connection, event)

def handleChannelCreate(connection, event):
    passToPlugins("channelcreate", connection, event)

def handleNoChanModes(connection, event):
    passToPlugins("nochanmodes", connection, event)

def handleTraceConnecting(connection, event):
    passToPlugins("traceconnecting", connection, event)

def handleTraceLink(connection, event):
    passToPlugins("tracelink", connection, event)

def handleTraceUnknown(connection, event):
    passToPlugins("traceunknown", connection, event)

def handleTraceHandshake(connection, event):
    passToPlugins("tracehandshake", connection, event)

def handleTraceUser(connection, event):
    passToPlugins("traceuser", connection, event)

def handleTraceOperator(connection, event):
    passToPlugins("traceoperator", connection, event)

def handleTraceService(connection, event):
    passToPlugins("traceservice", connection, event)

def handleTraceServer(connection, event):
    passToPlugins("traceserver", connection, event)

def handleTraceClass(connection, event):
    passToPlugins("traceclass", connection, event)

def handleTraceNewType(connection, event):
    passToPlugins("tracenewtype", connection, event)

def handleBadChannelKey(connection, event):
    passToPlugins("badchannelkey", connection, event)

def handleCreated(connection, event):
    passToPlugins("created", connection, event)

def handleYourHost(connection, event):
    passToPlugins("yourhost", connection, event)

def handleWelcome(connection, event):
    passToPlugins("welcome", connection, event)

def handleFeatureList(connection, event):
    passToPlugins("featurelist", connection, event)

def handleMyInfo(connection, event):
    passToPlugins("myinfo", connection, event)

def handleBannedFromChan(connection, event):
    passToPlugins("bannedfromchan", connection, event)

def handleUniqOpPrivsNeeded(connection, event):
    passToPlugins("uniqopprivsneeded", connection, event)

def handleRestricted(connection, event):
    passToPlugins("restricted", connection, event)

def handleCantKillServer(connection, event):
    passToPlugins("cantkillserver", connection, event)

def handleChanOPrivsNeeded(connection, event):
    passToPlugins("chanoprivsneeded", connection, event)

def handleNoPrivileges(connection, event):
    passToPlugins("noprivileges", connection, event)

def handleUnknownMode(connection, event):
    passToPlugins("unknownmode", connection, event)

def handleInviteOnlyChan(connection, event):
    passToPlugins("inviteonlychan", connection, event)

def handleChannelIsFull(connection, event):
    passToPlugins("channelisfull", connection, event)

def handleNamReply(connection, event):
    passToPlugins("namreply", connection, event)

def handleWhoReply(connection, event):
    passToPlugins("whoreply", connection, event)

def handleVersion(connection, event):
    passToPlugins("version", connection, event)

def handleUnknownCommand(connection, event):
    passToPlugins("unknowncommand", connection, event)

def handleBanListFull(connection, event):
    passToPlugins("banlistfull", connection, event)

def handleDCCConnect(connection, event):
    passToPlugins("dcc_connect", connection, event)

def handleDCCDisconnect(connection, event):
    passToPlugins("dcc_disconnect", connection, event)

def handleDCCMsg(connection, event):
    passToPlugins("dccmsg", connection, event)

def handleDisconnect(connection, event):
    passToPlugins("disconnect", connection, event)

def handleCTCP(connection, event):
    passToPlugins("ctcp", connection, event)

def handleCTCPReply(connection, event):
    passToPlugins("ctcpreply", connection, event)

def handleError(connection, event):
    passToPlugins("error", connection, event)

def handleJoin(connection, event):  
    passToPlugins("join", connection, event)

def handleMode(connection, event):
    passToPlugins("mode", connection, event)

def handlePing(connection, event):
    passToPlugins("ping", connection, event)

def handlePrivNotice(connection, event):
    passToPlugins("privnotice", connection, event)

def handlePubMsg(connection, event):
    passToPlugins("pubmsg", connection, event)

def handlePubNotice(connection, event):
    passToPlugins("pubnotice", connection, event)

irc.add_global_handler("statskline",        handleStatsKLine)
irc.add_global_handler("statsqline",        handleStatsQLine)
irc.add_global_handler("statsnline",        handleStatsNLine)
irc.add_global_handler("statsiline",        handleStatsILine)
irc.add_global_handler("statscommands",     handleStatsCommands)
irc.add_global_handler("statscline",        handleStatsCLine)
irc.add_global_handler("tracereconnect",    handleTraceReconnect)
irc.add_global_handler("statslinkinfo",     handleStatsLinkInfo)
irc.add_global_handler("statsyline",        handleStatsYLine)
irc.add_global_handler("endofstats",        handleEndOfStats)
irc.add_global_handler("nooperhost",        handleNoOperHost)
irc.add_global_handler("noservicehost",     handleNoServiceHost)
irc.add_global_handler("toomanytargets",    handleTooManyTargets)
irc.add_global_handler("wasnosuchnick",     handleWasNoSuchNick)
irc.add_global_handler("invitelist",        handleInviteList)
irc.add_global_handler("endofinvitelist",   handleEndOfInviteList)
irc.add_global_handler("nosuchchannel",     handleNoSuchChannel)
irc.add_global_handler("inviting",          handleInviting)
irc.add_global_handler("summoning",         handleSummoning)
irc.add_global_handler("exceptlist",        handleExceptList)
irc.add_global_handler("endofexceptlist",   handleEndOfExceptList)
irc.add_global_handler("noorigin",          handleNoOrigin)
irc.add_global_handler("tryagain",          handleTryAgain)
irc.add_global_handler("endoftrace",        handleEndOfTrace)
irc.add_global_handler("tracelog",          handleTraceLog)
irc.add_global_handler("n_global",          handleNGlobal)
irc.add_global_handler("n_local",           handleNLocal)
irc.add_global_handler("notonchannel",      handleNotOnChannel)
irc.add_global_handler("noadmininfo",       handleNoAdminInfo)
irc.add_global_handler("nomotd",            handleNoMOTD)
irc.add_global_handler("fileerror",         handleFileError)
irc.add_global_handler("wildtoplevel",      handleWildTopLevel)
irc.add_global_handler("unavailresource",   handleUnavailResource)
irc.add_global_handler("norecipient",       handleNoRecipient)
irc.add_global_handler("notexttosend",      handleNoTextToSend)
irc.add_global_handler("notoplevel",        handleNoTopLevel)
irc.add_global_handler("info",              handleInfo)
irc.add_global_handler("infostart",         handleInfoStart)
irc.add_global_handler("motd",              handleMOTD)
irc.add_global_handler("motdstart",         handleMOTDStart)
irc.add_global_handler("endofinfo",         handleEndOfInfo)
irc.add_global_handler("motd2",             handleMOTD2)
irc.add_global_handler("endofmotd",         handleEndOfMOTD)
irc.add_global_handler("whoischannels",     handleWhoisChannels)
irc.add_global_handler("endofwhois",        handleEndOfWhois)
irc.add_global_handler("whoisoperator",     handleWhoisOperator)
irc.add_global_handler("whoisserver",       handleWhoisServer)
irc.add_global_handler("whoisuser",         handleWhoisUser)
irc.add_global_handler("whoisidle",         handleWhoisIdle)
irc.add_global_handler("whoischanop",       handleWhoisChanop)
irc.add_global_handler("endofwho",          handleEndOfWho)
irc.add_global_handler("whowasuser",        handleWhoWasUser)
irc.add_global_handler("users",             handleUsers)
irc.add_global_handler("usersstart",        handleUsersStart)
irc.add_global_handler("time",              handleTime)
irc.add_global_handler("nousers",           handleNoUsers)
irc.add_global_handler("endofusers",        handleEndOfUsers)
irc.add_global_handler("useronchannel",     handleUserOnChannel)
irc.add_global_handler("endofbanlist",      handleEndOfBanList)
irc.add_global_handler("endofwhowas",       handleEndOfWhoWas)
irc.add_global_handler("endofnames",        handleEndOfNames)
irc.add_global_handler("banlist",           handleBanList)
irc.add_global_handler("links",             handleLinks)
irc.add_global_handler("endoflinks",        handleEndOfLinks)
irc.add_global_handler("closing",           handleClosing)
irc.add_global_handler("closeend",          handleCloseEnd)
irc.add_global_handler("killdone",          handleKillDone)
irc.add_global_handler("none",              handleNone)
irc.add_global_handler("away",              handleAway)
irc.add_global_handler("userhost",          handleUserHost)
irc.add_global_handler("ison",              handleIsOn)
irc.add_global_handler("unaway",            handleUnAway)
irc.add_global_handler("nowaway",           handleNowAway)
irc.add_global_handler("nologin",           handleNoLogin)
irc.add_global_handler("statshline",        handleStatsHLine)
irc.add_global_handler("rehashing",         handleRehashing)
irc.add_global_handler("statslline",        handleStatsLLine)
irc.add_global_handler("summondisabled",    handleSummonDisabled)
irc.add_global_handler("statsoline",        handleStatsOLine)
irc.add_global_handler("statsuptime",       handleStatsUptime)
irc.add_global_handler("youreoper",         handleYoureOper)
irc.add_global_handler("nickcollision",     handleNickCollision)
irc.add_global_handler("myportis",          handleMyPortIs)
irc.add_global_handler("erroneusnickname",  handleErroneusNickname)
irc.add_global_handler("nicknameinuse",     handleNicknameInUse)
irc.add_global_handler("nonicknamegiven",   handleNoNicknameGiven)
irc.add_global_handler("notregistered",     handleNotRegistered)
irc.add_global_handler("notopic",           handleNoTopic)
irc.add_global_handler("topicinfo",         handleTopicInfo)
irc.add_global_handler("topic",             handleTopic)
irc.add_global_handler("adminloc2",         handleAdminLoc2)
irc.add_global_handler("adminemail",        handleAdminEmail)
irc.add_global_handler("luserop",           handleLUserOp)
irc.add_global_handler("luserunknown",      handleLUserUnknown)
irc.add_global_handler("luserconns",        handleLUserConns)
irc.add_global_handler("luserclient",       handleLUserClient)
irc.add_global_handler("adminme",           handleAdminMe)
irc.add_global_handler("adminloc1",         handleAdminLoc1)
irc.add_global_handler("luserchannels",     handleLUserChannels)
irc.add_global_handler("luserme",           handleLUserMe)
irc.add_global_handler("toomanychannels",   handleTooManyChannels)
irc.add_global_handler("cannotsendtochan",  handleCannotSendToChan)
irc.add_global_handler("usersdontmatch",    handleUsersDontMatch)
irc.add_global_handler("nosuchserver",      handleNoSuchServer)
irc.add_global_handler("nosuchnick",        handleNoSuchNick)
irc.add_global_handler("yourebannedcreep",  handleYoureBannedCreep)
irc.add_global_handler("passwdmismatch",    handlePasswdMismatch)
irc.add_global_handler("keyset",            handleKeyset)
irc.add_global_handler("youwillbebanned",   handleYouWillBeBanned)
irc.add_global_handler("needmoreparams",    handleNeedMoreParams)
irc.add_global_handler("nopermforhost",     handleNoPermForHost)
irc.add_global_handler("alreadyregistered", handleAlreadyRegistered)
irc.add_global_handler("umodeis",           handleUModeIs)
irc.add_global_handler("usersdisabled",     handleUsersDisabled)
irc.add_global_handler("umodeunknownflag",  handleUModeUnknownFlag)
irc.add_global_handler("servlist",          handleServList)
irc.add_global_handler("servlistend",       handleServListEnd)
irc.add_global_handler("serviceinfo",       handleServiceInfo)
irc.add_global_handler("endofservices",     handleEndOfServices)
irc.add_global_handler("service",           handleService)
irc.add_global_handler("usernotinchannel",  handleUserNotInChannel)
irc.add_global_handler("list",              handleList)
irc.add_global_handler("listend",           handleListEnd)
irc.add_global_handler("liststart",         handleListStart)
irc.add_global_handler("channelmodeis",     handleChannelModeIs)
irc.add_global_handler("badchanmask",       handleBadChanMask)
irc.add_global_handler("channelcreate",     handleChannelCreate)
irc.add_global_handler("nochanmodes",       handleNoChanModes)
irc.add_global_handler("traceconnecting",   handleTraceConnecting)
irc.add_global_handler("tracelink",         handleTraceLink)
irc.add_global_handler("traceunknown",      handleTraceUnknown)
irc.add_global_handler("tracehandshake",    handleTraceHandshake)
irc.add_global_handler("traceuser",         handleTraceUser)
irc.add_global_handler("traceoperator",     handleTraceOperator)
irc.add_global_handler("traceservice",      handleTraceService)
irc.add_global_handler("traceserver",       handleTraceServer)
irc.add_global_handler("traceclass",        handleTraceClass)
irc.add_global_handler("tracenewtype",      handleTraceNewType)
irc.add_global_handler("badchannelkey",     handleBadChannelKey)
irc.add_global_handler("created",           handleCreated)
irc.add_global_handler("yourhost",          handleYourHost)
irc.add_global_handler("welcome",           handleWelcome)
irc.add_global_handler("featurelist",       handleFeatureList)
irc.add_global_handler("myinfo",            handleMyInfo)
irc.add_global_handler("bannedfromchan",    handleBannedFromChan)
irc.add_global_handler("uniqopprivsneeded", handleUniqOpPrivsNeeded)
irc.add_global_handler("restricted",        handleRestricted)
irc.add_global_handler("cantkillserver",    handleCantKillServer)
irc.add_global_handler("chanoprivsneeded",  handleChanOPrivsNeeded)
irc.add_global_handler("noprivileges",      handleNoPrivileges)
irc.add_global_handler("unknownmode",       handleUnknownMode)
irc.add_global_handler("inviteonlychan",    handleInviteOnlyChan)
irc.add_global_handler("channelisfull",     handleChannelIsFull)
irc.add_global_handler("namreply",          handleNamReply)
irc.add_global_handler("whoreply",          handleWhoReply)
irc.add_global_handler("version",           handleVersion)
irc.add_global_handler("unknowncommand",    handleUnknownCommand)
irc.add_global_handler("banlistfull",       handleBanListFull)
irc.add_global_handler("dcc_connect",       handleDCCConnect)
irc.add_global_handler("dcc_disconnect",    handleDCCDisconnect)
irc.add_global_handler("dccmsg",            handleDCCMsg)
irc.add_global_handler("disconnect",        handleDisconnect)
irc.add_global_handler("ctcp",              handleCTCP)
irc.add_global_handler("ctcpreply",         handleCTCPReply)
irc.add_global_handler("error",             handleError)
irc.add_global_handler("join",              handleJoin)
irc.add_global_handler("kick",              handleKick)
irc.add_global_handler("mode",              handleMode)
irc.add_global_handler("part",              handlePart)
irc.add_global_handler("ping",              handlePing)
irc.add_global_handler("privmsg",           handlePrivMsg)
irc.add_global_handler("privnotice",        handlePrivNotice)
irc.add_global_handler("pubmsg",            handlePubMsg)
irc.add_global_handler("pubnotice",         handlePubNotice)
irc.add_global_handler("quit",              handleQuit)
irc.add_global_handler("nick",              handleNickChange)

# Create server object, connect and join channels. Repeat for every server
try:
    newServer = irc.server()
    newServer.connect(globals.serverData["network"], globals.serverData["port"], globals.serverData["nick"], ircname = globals.serverData["name"])
    for channel in globals.serverData["channels"]:
        newServer.join(channel)
except:
    print "Error connecting to server:"
    print "Type:", sys.exc_info()[0]
    print "Description:", sys.exc_info()[1]

# Control loop
while(globals.keeprunning):
    irc.process_once()
