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

""" Server related queries. """

from __future__ import with_statement


class _ServerQueries(object):
    """ Defines server related queries. """
    def get_motd(self, server=None):
        """
        Gets the server's MOTD.
        Optional arguments:
        * server=None - Server to get the MOTD of.
        """
        with self.lock:
            if not server:
                self.send('MOTD')
            else:
                self.send('MOTD %s' % server)

            motd = []
            while self.readable():
                msg = self._recv(expected_replies=('375', '372', '376', '422'), item_slice=(1, None))
                if msg[0] == '375':
                    pass
                elif msg[0] == '372':
                    motd.append(msg[2].replace(':', '', 1))
                elif msg[0] == '376':
                    break
                elif msg[0] == '422':
                    break
            self.motd = tuple(self.motd)
            return motd

    def get_lusers(self, mask=None, target=None):
        """
        Get the LUSERS information.
        Optional arguments:
        * mask=None - Mask to get LUSERS information of.
        * target=None - Forward the query.
        """
        with self.lock:
            if not mask:
                self.send('LUSERS')
            elif not target and mask:
                self.send('LUSERS %s' % mask)
            else:
                self.send('LUSERS %s %s' % (mask, target))
            while self.readable():
                msg = self._recv(expected_replies=('250', '251', '252', '254', '255', '265', '266'), item_slice=(1, None))
                segments = msg[2].split()
                if msg[0] == '250':
                    self.lusers['HIGHESTCONNECTIONS'] = segments[3]
                    self.lusers['TOTALCONNECTIONS'] = segments[9][1:]
                elif msg[0] == '251':
                    self.lusers['USERS'] = segments[2]
                    self.lusers['INVISIBLE'] = segments[5]
                    self.lusers['SERVERS'] = segments[8]

                elif msg[0] == '252':
                    self.lusers['OPERATORS'] = segments[0]

                elif msg[0] == '254':
                    self.lusers['CHANNELS'] = segments[0]

                elif msg[0] == '255':
                    self.lusers['CLIENTS'] = segments[2]
                    self.lusers['LSERVERS'] = segments[5]

                elif msg[0] == '265':
                    self.lusers['LOCALUSERS'] = segments[3]
                    self.lusers['LOCALMAX'] = segments[5]

                elif msg[0] == '266':
                    self.lusers['GLOBALUSERS'] = segments[3]
                    self.lusers['GLOBALMAX'] = segments[5]
                    break
            return self.lusers

    def get_version(self, target=None):
        """
        Get the servers VERSION information.
        Optional arguments:
        * target=None - Server to get the VERSION information of.
        """
        with self.lock:
            if not target:
                self.send('VERSION')
            else:
                self.send('VERSION %s' % target)

            while self.readable():
                msg = self._recv(expected_replies=('351', '005'), item_slice=(1, None))
                version = msg[2].replace(' :are supported by this server', '')
                version = version.split()
                for info in version:
                        try:
                            info = info.split('=')
                            name = info[0]
                            value = info[1]
                            self.version[name] = value

                            if name == 'CHARSET':
                                self.encoding = value
                        except IndexError:
                            self.version[info[0]] = True

            return self.version

    def stats(self, query=None, target=None):
        """
        Get the server's STATS information.
        Optional arguments:
        * query=None - STATS Query.
        * target=None - Target server.
        """
        with self.lock:
            if not query:
                self.send('STATS')
            elif not target and query:
                self.send('STATS %s' % query)
            else:
                self.send('STATS %s %s' % (query, target))
            stat_lines = []
            while self.readable():
                msg = self._recv()
                if msg[1] == '219':
                    break
                else:
                    stat_lines.append(msg[3].replace(':', '', 1))
            return stat_lines

    def links(self, r_server=None, mask=None):
        """
        Get LINKS information.
        Optional arguments:
        * r_server=None - Forward the query to this server.
        * mask=None - Match mask servers.
        """
        with self.lock:
            if not r_server:
                self.send('LINKS')
            elif not mask and r_server:
                self.send('LINKS %s' % r_server)
            else:
                self.send('LINKS %s %s' % (r_server, mask))
            links = {}
            while self.readable():
                msg = self._recv(expected_replies=('364', '365'))[1:]
                segments = msg[2].split()
                if msg[0] == '364':
                    server = segments[0]
                    desc = ' '.join(segments[3:])
                    links[server] = desc
                elif msg[0] == '365':
                    break
            return links

    def time(self, target=None):
        """
        Get server time.
        Optional arguments:
        * target=None - Target server.
        """
        with self.lock:
            if target:
                self.send('TIME %s' % target)
            else:
                self.send('TIME')
            time = self._recv(rm_colon=True, expected_replies=('391'), \
                              default_rvalue='', item_slice=3)
            if time:
                time = time.split(':', 1)[1]
            return time

    def s_connect(self, server, port, r_server=None):
        """
        Link a server.
        Required arguments:
        * server - Server to link with.
        * port - Port to use.
        Optional arguments:
        * r_server=None - Link r_server with server.
        """
        with self.lock:
            if not r_server:
                self.send('CONNECT %s %s' % (server, port))
            else:
                self.send('CONNECT %s %s %s' % (server, port, r_server))
            if self.readable():
                ncode = self._raw_recv().split()[1]
                if ncode in self.error_dictionary:
                    self.exception(ncode)
                else:
                    self._index -= 1

    def trace(self, target):
        """
        Run a trace on a target
        Required arguments:
        * target - Who to trace.
        """
        with self.lock:
            self.send('TRACE ' + target)
            rvalue = []
            while self.readable():
                data = self._raw_recv()
                segments = data.split()
                if segments[1] == '262':
                    break
                else:
                    rvalue.append(' '.join(segments[4:]).replace(':', '', 1))
            return rvalue

    def admin(self, server=None):
        """
        Get the admin information.
        Optional arguments:
        * server=None - Get admin information for -
            server instead of the current server.
        """
        with self.lock:
            if not server:
                self.send('ADMIN')
            else:
                self.send('ADMIN %s' % server)
            rvalue = []
            while self.readable():
                data = self._raw_recv()
                segments = data.split()
                admin_ncodes = '257', '258', '259'
                if segments[1] == '256':
                    pass
                elif segments[1]  in admin_ncodes:
                    rvalue.append(' '.join(segments[3:])[1:])
                else:
                    self._buffer.append(data)
            return rvalue

    def s_info(self, server=None):
        """
        Runs the INFO command on a server.
        Optional arguments:
        * server=None - Get INFO for server instead of the current server.
        """
        with self.lock:
            if not server:
                self.send('INFO')
            else:
                self.send('INFO %s' % server)
            sinfo = []
            while self.readable():
                data = self._raw_recv()
                segments = data.split()
                if segments[1] == '371':
                    sinfo.append(' '.join(segments[3:])[1:])
                elif segments[1] == '374':
                    break
                else:
                    self._buffer.append(data)
            return sinfo

    def servlist(self, mask=None, type=None):
        """
        Runs the servlist command.
        Optional arguments:
        * mask=None - Mask
        * type=None - Type.
        """
        with self.lock:
            if not mask:
                self.send('SERVLIST')
            elif not type and mask:
                self.send('SERVLIST %s' % mask)
            else:
                self.send('SERVLIST %s %s' % (mask, type))

            servs = []
            while self.readable():
                data = self._raw_recv()
                segments = data.split()
                if segments[1] == '234':
                    servs.append(' '.join(segments[3:]).replace(':', '', 1))
                elif segments[1] == '235':
                    break
                else:
                    self._buffer.append(data)
            return servs

    def squery(self, sname, msg):
        """
        Send a SQUERY.
        Required arguments:
        * sname - Service name.
        * msg - Message to send.
        """
        with self.lock:
            self.send('SQUERY %s :%s' % (sname, msg))
            if self.readable():
                data = self._raw_recv()
                ncode = data.split()[1]
                if ncode in self.error_dictionary:
                    self.exception(ncode)
                else:
                    self._index -= 1

    def kill(self, nick, reason=''):
        """
        Kill someone
        Required arguments:
        * nick - Nick to kill.
        Optional arguments:
        * reason='' - Reason for killing them.
        """
        with self.lock:
            self.send('KILL ' + nick + ' :' + reason)

            if self.readable():
                data = self._raw_recv()
                ncode = data.split()[1]
                if ncode in self.error_dictionary:
                    self.exception(ncode)
                else:
                    self._index -= 1
