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
                ncode = self._raw_recv().split()[1]
                if ncode == '306':
                    self.is_away = True
                elif ncode == '305':
                    self.is_away = False
                else:
                    self._index -= 1

    def rehash(self):
        """
        Rehashes the IRCd's configuration file.
        """
        with self.lock:
            self.send('REHASH')
            if self.readable():
                segments = self._raw_recv().split()
                if segments[1] == '382':
                    pass
                elif segments[1] in self.error_dictionary:
                    self.exception(segments[1])
                else:
                    self._index -= 1

    def die(self, password=''):
        """
        Tells the IRCd to die.
        Optional arguments:
        * password='' - Die command password.
        """
        with self.lock:
            self.send('DIE :%s' % password)
            if self.readable():
                segments = self._raw_recv().split()
                if segments[1] == self.error_dictionary:
                    self.exception(segments[1])
                else:
                    self._index -= 1

    def restart(self, password=''):
        """
        Tells the IRCd to restart.
        Optional arguments:
        * password='' - Restart command password.
        """
        with self.lock:
            self.send('RESTART :%s' % password)
            if self.readable():
                segments = self._raw_recv().split()
                if segments[1] in self.error_dictionary:
                    self.exception(segments[1])
                else:
                    self._index -= 1

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
        self.send('WALLOPS :%s' % msg)

    def userhost(self, nick):
        """
        Runs a userhost on a nick.
        Required arguments:
        * nick - Nick to run a userhost on.
        """
        with self.lock:
            self.send('USERHOST :%s' % nick)
            if self.readable():
                segments = self._raw_recv().split()
                if segments[1] == '302':
                    return ' '.join(segments[3:]).replace(':', '', 1)
                elif segments[1] in self.error_dictionary:
                    self.exception(segments[1])
                else:
                    self._index -= 1

    def ison(self, nick):
        """
        Checks if a nick is on or not.
        Required arguments:
        * nick - Nick to check.
        """
        with self.lock:
            self.send('ISON :%s' % nick)
            if self.readable():
                segments = self._raw_recv().split()
                if segments[1] == '303':
                    return ' '.join(segments[3:]).replace(':', '', 1)
                elif segments[1] in self.error_dictionary:
                    self.exception(segments[1])
                else:
                    self._index -= 1
