#!/usr/bin/env python3
#    This file is part of Lurklib.
#    Copyright (C) 2011  LK-
#
#    Lurklib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Lurklib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Lurklib.  If not, see <http://www.gnu.org/licenses/>.

""" Lurklib usage example. """

SERVER = 'irc.darchoods.net'

import lurklib


class HelloBot(lurklib.Client):
    def on_connect(self):
        """ Join #bots upon connecting. """
        self.join_('#bots')

    def on_chanmsg(self, from_, channel, message):
        """ Event handlers for channel messages. """
        if message == 'hello':
            self.privmsg(channel, 'Hello, %s!' % from_[0])
            print('%s said hello!' % from_[0])

        elif message == '!quit':
            self.quit('Bye!')

if __name__ == '__main__':
    # Connect to IRC, and assign the returned lurklib.Client object, \
    # to the HELLOBOT variable.
    HELLOBOT = HelloBot(server=SERVER, nick=('HelloBot', 'HelloBot-'))

    # Enter Lurklib's main loop which will keep you connected to IRC -
    # and call the specified hooks when necessary.
    HELLOBOT.mainloop()
