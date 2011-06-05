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

""" Defines optional IRC-things. """

from __future__ import with_statement


class _Optional(object):
    """ Defines optional IRC protocol features. """
    def away(self, msg=''):
        """
        Sets/unsets your away status.
        Optional arguments:
        * msg='' - Away reason.
        """
        with self.lock:
            self.send('AWAY :%s' % msg)
            if self.readable():
                msg = self._recv(expected_replies=('306', '305'))
                if msg[0] == '306':
                    self.is_away = True
                elif msg[0] == '305':
                    self.is_away = False

    def rehash(self):
        """
        Rehashes the IRCd's configuration file.
        """
        with self.lock:
            self.send('REHASH')
            if self.readable():
                msg = self._recv(expected_replies=('382',))
                if msg[0] == '382':
                    pass

    def die(self, password=''):
        """
        Tells the IRCd to die.
        Optional arguments:
        * password='' - Die command password.
        """
        with self.lock:
            self.send('DIE :%s' % password, error_check=True)

    def restart(self, password=''):
        """
        Tells the IRCd to restart.
        Optional arguments:
        * password='' - Restart command password.
        """
        with self.lock:
            self.send('RESTART :%s' % password, error_check=True)

    def summon(self):
        """ Not implemented. """
        pass

    def users(self):
        """ Not implemented. """
        pass

    def operwall(self, msg):
        """
        Sends a wallops message.
        Required arguments:
        * msg - Message to send.
        """
        self.send('WALLOPS :%s' % msg, error_check=True)

    def userhost(self, nicks):
        """
        Runs a userhost on a nick.
        Required arguments:
        * nick - Nick to run a userhost on.
        """
        with self.lock:
            self.send('USERHOST :%s' % nicks)
            userhosts = []
            if self.readable():
                msg = self._recv(expected_replies=('302',))
                if msg[0] == '302':
                    userhosts = msg[2].replace(':', '', 1).split()
            return userhosts

    def ison(self, nicks):
        """
        Checks if a nick is on or not.
        Returns list of nicks online.
        Required arguments:
        * nick - Nick to check.
        """
        with self.lock:
            self.send('ISON :%s' % ' '.join(nicks))
            online_nicks = []
            if self.readable():
                msg = self._recv(expected_replies=('303',))
                if msg[0] == '303':
                    online_nicks = msg[2].replace(':', '', 1).split()
            return online_nicks
