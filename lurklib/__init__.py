#    This file is part of Lurklib.
#    Copyright (C) 2010  Jamie Shaw (LK-)
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

""" High level abstraction Lurklib file. """

from __future__ import with_statement
from . import core

__version__ = '0.6.0.2'


class Client(core._Core):
    """ High level IRC abstraction class """
    def process_once(self, timeout=0.01):
        """
        Handles an event and calls it's handler
        Optional arguments:
        * timeout=0.01 - Wait for an event until the timeout is reached.
        """
        event = self.recv(timeout)
        if event != None:
            exec('self.on_%s(%s)' % (event[0].lower(), event[1]))

    def mainloop(self):
        """
        Handles events and calls their handler for infinity.
        """
        while self.keep_going:
            with self.lock:
                if self.on_auto and not self.readable(2):
                    self.on_auto()
                    self.on_auto = None
                if self.keep_going == False:
                    break
                self.process_once()

    def on_auto(self, event):
        pass

    def on_join(self, event):
        pass

    def on_part(self, event):
        pass

    def on_privmsg(self, event):
        pass

    def on_ctcp(self, event):
        pass

    def on_notice(self, event):
        pass

    def on_ctcp_reply(self, event):
        pass

    def on_mode(self, event):
        pass

    def on_kick(self, event):
        pass

    def on_invite(self, event):
        pass

    def on_nick(self, event):
        pass

    def on_topic(self, event):
        pass

    def on_quit(self, event):
        pass

    def on_lusers(self, event):
        pass

    def on_error(self, event):
        pass

    def on_unknown(self, event):
        pass
