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

""" Declares variables and standard modules needed by Lurklib etc. """
import socket
import time
import ssl as tls
from select import select
from threading import RLock
try:
    import socks
except ImportError:
    pass

class _Variables(object):
    """ Set Lurklib module variables/objects. """
    _m_socket = socket
    _select = select
    _m_tls = tls
    _m_time = time
    _m_proxy = socks

    _crlf = '\r\n'
    priv_types = ('~', '&', '@', '%', '+')

    def __init__(self):
        """ Set instance-specific variables/objects. """
        self._buffer = []
        self._index = 0

        self._socket = self._m_socket.socket()

        self.motd = []
        self.version = {}
        self.channels = {}

        self.keep_going = False
        self.con_msg = []
        self.ircd = ''
        self.is_away = False
        self.lusers = {}
        self.connected = False
        self.server = ''
        self.umodes = ''
        self.cmodes = ''
        self.server = ''
        self.lock = RLock()
