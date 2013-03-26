YamiBot is an IRC bot that handles its entire behavior using plugins

Every .py file *not* starting with _ in the plugins directory is loaded

All modules are required to contain *at least* a run() function, taking three arguments:
 - The event type (a string)
 - The connection the event originated from
 - The event itself

The connection object and the event object are defined in the module irclib.
Make sure you have python-irclib installed and every module does import irclib!

SETTING UP YAMIBOT:
There is a config file in this directory named "yamibot.conf.example". Rename this to
"yamibot.conf", and edit it to suit your needs.

Run "passhash.py" to set YamiBot's administrator password.

USING YAMIBOT:
An example plugin named "PrivMsg.py" is included in the plugins directory. All it does
is respond to a private message saying "hello" with the text "Hi!". Please test that
this works correctly. Also, a plugin named "admin.py" is included for administrative
tasks.

By default, you can authenticate as administrator via private message in the format "auth <password>".
If the format is incorrect, YamiBot will help you on your way a bit. YamiBot will also
provide feedback about the success or failure of authenticating.

If you write a plugin that needs to access the bot's global variables (e.g. the admin password), be sure
to include "import globals" at the top of the file, and use the format "globals.<varname>" throughout
the plugin. See the "admin" plugin for an example.
