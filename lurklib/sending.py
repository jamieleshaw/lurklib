#    This file is part of Lurklib.
#    Copyright(C) 2011  LK-
#
#    Lurklib is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#    Lurklib is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Lurklib.  If not, see <http://www.gnu.org/licenses/>.

""" File for sending-related things. """

from __future__ import with_statement


class _Sending(object):
    """ Defines PRIVMSG and NOTICE methods. """
    def privmsg(self, target, message):
        """
        Sends a PRIVMSG to someone.
        Required arguments:
        * target - Who to send the message to.
        * message - Message to send.
        """
        with self.lock:
            self.send('PRIVMSG ' + target + ' :' + message)
            if self.readable():
                msg = self._recv(expected_replies=('301',))
                if msg[0] == '301':
                    return 'AWAY', msg[2].split(None, 1)[1].replace(':', '', 1)

    def notice(self, target, message):
        """
        Sends a NOTICE to someone.
        Required arguments:
        * target - Who to send the message to.
        * message - Message to send.
        """
        with self.lock:
            self.send('NOTICE ' + target + ' :' + message)
            if self.readable():
                msg = self._recv(expected_replies=('301',))
                if msg[0] == '301':
                    return 'AWAY', msg[2].split(None, 1)[1].replace(':', '', 1)
