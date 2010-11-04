#!/usr/bin/env python3
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

""" Lurklib unit testing. """

import unittest
import threading
import socket
import sys
import lurklib

sys.path.append('tests/')

from connection import ConnectionTest
from channel import ChannelTest


class IRCD(threading.Thread):
    def run(self):
        self._socket = socket.socket()
        self.buffer = []
        self.index = 0
        self._socket.bind(('0.0.0.0', 6667))
        self._socket.listen(1)
        self.socket = self._socket.accept()[0]

    def rsend(self, msg):
        """
        Send a raw message with the clrf appended to it.
        Required arguments:
        * msg - Message to send.
        """
        data = bytes('%s\r\n' % msg, 'UTF-8')
        self.socket.send(data)

    def send(self, msg):
        """
        Send a a IRC message from the server.
        Required arguments:
        * msg - Message to send.
        """
        self.rsend(':lurklib.test.net %s' % msg)

    def nsend(self, ncode, msg):
        """
        Send an IRC numeric and message.
        Required arguments:
        * ncode - IRC numeric to send.
        * msg - Message to send.
        """
        self.send('%s Lurklib %s' % (ncode, msg))

    def recv(self):
        """ Receive an IRC message. """
        if self.index >= len(self.buffer):
            data = self.socket.recv(4096).decode('UTF-8')
            lines = data.split('\r\n')
            for line in lines:
                if line != '':
                    self.buffer.append(line)
        msg = self.buffer[self.index]
        self.index += 1
        return msg


class BaseTest(unittest.TestCase):
    ircd = IRCD()
    ircd.start()
    irc = lurklib.IRC('localhost', nick='Lurklib')


class TestLurklib(BaseTest, ConnectionTest, ChannelTest):
    pass

if __name__ == '__main__':
    unittest.main()
