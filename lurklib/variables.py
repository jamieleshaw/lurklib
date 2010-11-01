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

""" Declares variables and standard modules needed by Lurklib etc. """
import socket
import time
import sys
import select
from threading import RLock
try: import ssl
except ImportError: ssl = None

class _Variables(object):
    """ Sets the default values for Lurklib's runtime variables. """
    ssl = ssl
    buffer = []
    m_socket = socket
    m_select = select
    m_sys = sys
    s = m_socket.socket()

    motd = []
    version = {}
    channels = {}
    m_time = time
    keep_going = False
    con_msg = []
    ircd = ''
    is_away = False

    lusers = {}
    priv_types = ('~', '&', '@', '%', '+')
    connected = False
    server = ''
    umodes = ''
    cmodes = ''
    server = ''
    lock = RLock()
    index = 0