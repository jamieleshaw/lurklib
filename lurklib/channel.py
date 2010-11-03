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

""" Channel-related interaction file. """

from __future__ import with_statement


class _Channel(object):
    """ Channel-related interaction class. """
    def is_in_channel(self, channel):
        """
        Find out if you are in a channel.
        Required arguments:
        * channel - Channel to check whether you are in it or not.
        """
        for channel_ in self.channels:
            if self.compare(channel_, channel):
                return True
        return False

    def join(self, channel, key=None, process_only=False):
        """
        Joins a channel.
        Returns a tuple of information regarding the channel.
        Channel Information:
        * [0] - A tuple containing /NAMES.
        * [1] - Channel topic.
        * [2] - Tuple containing information regarding of whom set the topic.
        * [3] - Time object about when the topic was set.
        Required arguments:
        * channel - The channel to join.
        Optional arguments:
        * key=None - Channel key.
        * process_only=False - Only process a join, don't request one.
        """

        with self.lock:
            topic = ''
            users = []
            set_by = ''
            time_set = ''
            if self.is_in_channel(channel):
                raise \
                    self.AlreadyInChannel('LurklibError: AlreadyInChannel')
            if process_only == False:
                if key != None:
                    self.send('JOIN %s %s' % (channel, key))
                else:
                    self.send('JOIN %s' % channel)

            while self.readable(4):
                msg = self.recv(True)

                if msg[1] == '332':
                    topic = msg[3].split(':', 1)[1]
                elif msg[1] == '333':
                    set_by, time_set = msg[3].split(' ', 3)[1:]
                    if self.UTC == False:
                        time_set = self._m_time.localtime(int(time_set))
                    else:
                        time_set = self._m_time.gmtime(int(time_set))
                    set_by = self._from_(set_by)

                elif msg[1] == '353':
                    users.extend(msg[3].split(':', 1)[1].split())
                elif msg[1] == 'JOIN':
                    channel = msg[2]
                    self.channels[channel] = {}
                    if self.hide_called_events == False:
                        self._buffer.append(msg)
                elif msg[1] == '366':
                    break
                else:
                    self._buffer.append(msg)

            self.channels[channel]['USERS'] = {}
            for user in users:
                prefix = ''
                if user[0] in self.priv_types:
                    prefix = user[0]
                    user = user[1:]
                if prefix == '~':
                    self.channels[channel]['USERS'][user] = \
                    ['~', '', '', '', '']
                elif prefix == '&':
                    self.channels[channel]['USERS'][user] = \
                    ['', '&', '', '', '']
                elif prefix == '@':
                    self.channels[channel]['USERS'][user] = \
                    ['', '', '@', '', '']
                elif prefix == '%':
                    self.channels[channel]['USERS'][user] = \
                    ['', '', '', '%', '']
                elif prefix == '+':
                    self.channels[channel]['USERS'][user] = \
                    ['', '', '', '', '+']
                else:
                    self.channels[channel]['USERS'][user] = \
                    ['', '', '', '', '']
        return users, topic, set_by, time_set

    def part(self, channel, reason=None):
        """
        Part a channel.
        Required arguments:
        * channel - Channel to part.
        Optional arguments:
        * reason - Reason for parting.
        """
        with self.lock:
            if self.is_in_channel(channel) == False:
                raise self.NotInChannel('LurklibError: NotInChannel')

            if reason == None:
                self.send('PART %s' % channel)
            else:
                self.send('PART %s :%s' % (channel, reason))

            if self.readable():
                data = self._recv()
                ncode = data.split()[1]
                if ncode in self.error_dictionary:
                    self.exception(ncode)
                elif self.find(data, 'PART'):
                    del self.channels[data.split()[2]]
                    if self.hide_called_events == False:
                        self._buffer.append(data)
                else:
                    self._index -= 1

    def cmode(self, channel, modes=''):
        """
        Sets or gets the channel mode.
        Required arguments:
        * channel - Channel to set/get modes of.
        Optional arguments:
        * modes - Modes to set.
            If not specified return the modes of the channel.
        """
        with self.lock:
            if self.is_in_channel(channel) == False:
                raise self.NotInChannel('LurklibError: NotInChannel')

            if modes == '':
                    self.send('MODE %s' % channel)
                    if self.readable():
                        data = self._recv().split()[4]
                        return data.replace('+', '').replace(':', '', 1)
            else:
                self.send('MODE %s %s' % (channel, modes))

                if self.readable():
                    data = self._recv()
                    segments = data.split()
                    ncode = segments[1]

                    if ncode in self.error_dictionary:
                        self.exception(ncode)
                    elif self.find(data, 'MODE'):
                        channel = data.split()[2].replace(':', '', 1)
                        mode = ' '.join(segments[3:]).replace(':', '', 1)
                        self.parse_cmode_string(mode, channel)
                        if self.hide_called_events == False:
                            self._buffer.append(data)
                    else:
                        self._index -= 1

    def banlist(self, channel):
        """
        Get the channel banlist.
        Required arguments:
        * channel - Channel of which to get the banlist for.
        """
        with self.lock:
            if self.is_in_channel(channel) == False:
                raise self.NotInChannel('LurklibError: NotInChannel')

            self.send('MODE %s b' % channel)
            bans = []

            while self.readable():
                data = self._recv()
                ncode = data.split()[1]

                if ncode in self.error_dictionary:
                    self.exception(ncode)
                elif ncode == '367':
                    bans.append(data.split()[4])
                elif ncode == '368':
                    break
                else:
                    self._buffer.append(data)
            return bans

    def exceptlist(self, channel):
        """
        Get the channel exceptlist.
        Required arguments:
        * channel - Channel of which to get the exceptlist for.
        """
        with self.lock:
            if self.is_in_channel(channel) == False:
                raise self.NotInChannel('LurklibError: NotInChannel')

            self.send('MODE %s e' % channel)
            excepts = []

            while self.readable():
                data = self._recv()
                ncode = data.split()[1]

                if ncode in self.error_dictionary:
                    self.exception(ncode)
                elif ncode == '348':
                    excepts.append(data.split()[4])
                elif ncode == '349':
                    break
                else:
                    self._buffer.append(data)

            return excepts

    def invitelist(self, channel):
        """
        Get the channel invitelist.
        Required arguments:
        * channel - Channel of which to get the invitelist for.
        """
        with self.lock:
            if self.is_in_channel(channel) == False:
                raise self.NotInChannel('LurklibError: NotInChannel')

            self.send('MODE %s i' % channel)
            invites = []

            while self.readable():
                data = self._recv()
                ncode = data.split()[1]

                if ncode in self.error_dictionary:
                    self.exception(ncode)
                elif ncode == '346':
                    invites.append(data.split()[4])
                elif ncode == '347':
                    break
                else:
                    self._buffer.append(data)

            return invites

    def topic(self, channel, topic=None):
        """
        Sets/gets the channel topic.
        Required arguments:
        * channel - Channel to set/get the topic for.
        Optional arguments:
        * topic - Topic to set.
            If not specified the current channel topic will be returned.
        """
        with self.lock:
            if self.is_in_channel(channel) == False:
                raise self.NotInChannel('LurklibError: NotInChannel')

            topic = ''
            set_by = ''
            time_set = ''
            if topic != None:
                self.send('TOPIC %s :%s' % (channel, topic))
                if self.readable():
                    data = self._recv()
                    ncode = data.split()[1]
                    if ncode in self.error_dictionary:
                        self.exception(ncode)
                    elif self.find(data, 'TOPIC') and self.hide_called_events:
                        channel = data.split()[2].replace(':', '', 1)
                        self.channels[channel]['TOPIC'] = topic
                        if self.hide_called_events == False:
                            self._buffer.append(data)
                    else:
                        self._index -= 1
            else:
                self.send('TOPIC %s' % channel)
                while self.readable():
                    data = self._recv()
                    ncode = data.split()[1]
                    if ncode in self.error_dictionary:
                        self.exception(ncode)
                    elif ncode == '332':
                        topic = data.split(None, 4)[4].replace(':', '', 1)
                        self._recv()
                    elif self.find(data, 'TOPIC'):
                        channel = data.split()[2].replace(':', '', 1)
                        self.channels[channel]['TOPIC'] = topic
                        if self.hide_called_events == False:
                            self._buffer.append(data)
                    elif ncode == '333':
                        segments = data.split()
                        if self.UTC == False:
                            time_set = self._m_time.localtime(int(segments[5]))
                        else:
                            time_set = self._m_time.gmtime(int(segments[5]))
                        set_by = self._from_(segments[4])
                    elif ncode == '331':
                        topic = ''
                    else:
                        self._buffer.append(data)

            return topic, set_by, time_set

    def names(self, channel):
        """
        Get a list of users in the channel.
        Required arguments:
        * channel - Channel to get list of users for.
        """
        with self.lock:
            if self.is_in_channel(channel) == False:
                raise self.NotInChannel('LurklibError: NotInChannel')

            self.send('NAMES %s' % channel)
            names = []

            while self.readable():
                data = self._recv()
                ncode = data.split()[1]

                if ncode == '353':
                    new_names = data.split()[5:]
                    new_names[0] = new_names[0].replace(':', '', 1)
                    try:
                        names.append = new_names
                    except NameError:
                        names = new_names
                elif ncode in self.error_dictionary:
                    self.exception(ncode)
                elif ncode == '366':
                    channel = data.split()[3]
                    break
                else:
                    self._buffer.append(data)
            for name in names:
                prefix = ''
                if name[0] in self.priv_types:
                    prefix = name[0]
                    name = name[1:]
                if prefix == '~':
                    self.channels[channel]['USERS'][name] = \
                    ['~', '', '', '', '']
                elif prefix == '&':
                    self.channels[channel]['USERS'][name] = \
                    ['', '&', '', '', '']
                elif prefix == '@':
                    self.channels[channel]['USERS'][name] = \
                    ['', '', '@', '', '']
                elif prefix == '%':
                    self.channels[channel]['USERS'][name] = \
                    ['', '', '', '%', '']
                elif prefix == '+':
                    self.channels[channel]['USERS'][name] = \
                    ['', '', '', '', '+']
                else:
                    self.channels[channel]['USERS'][name] = \
                    ['', '', '', '', '']
            return names

    def slist(self):
        """ Gets a list of channels on the server. """
        with self.lock:
            self.send('LIST')
            list_ = {}

            while self.readable():
                data = self._recv()
                ncode = data.split()[1]

                if ncode == '322':
                    raw_lst = data.split(None, 6)
                    modes = raw_lst[5].replace(':', '', 1)
                    modes = modes.replace('[', '').replace(']', '')
                    list_[raw_lst[3]] = raw_lst[4], modes, raw_lst[6]
                elif ncode == '321':
                    pass
                elif ncode in self.error_dictionary:
                    self.exception(ncode)
                elif ncode == '323':
                    break
                else:
                    self._buffer.append(data)
            return list_

    def invite(self, channel, nick):
        """
        Invite someone to a channel.
        Required arguments:
        * channel - Channel to invite them to.
        * nick - Nick to invite.
        """
        with self.lock:
            if self.is_in_channel(channel) == False:
                raise self.NotInChannel('LurklibError: NotInChannel')

            self.send('INVITE %s %s' % (nick, channel))

            while self.readable():
                    data = self._recv()
                    ncode = data.split()[1]

                    if ncode in self.error_dictionary:
                        self.exception(ncode)
                    elif ncode == '341':
                        pass
                    elif ncode == '301':
                        away_msg = data.split(None, 3)[3].replace(':', '', 1)
                        return 'AWAY', away_msg
                    elif self.find(data, 'INVITE') and self.hide_called_events:
                        pass
                    else:
                        self._buffer.append(data)

    def kick(self, channel, nick, reason=''):
        """
        Kick someone from a channel.
        Required arguments:
        * channel - Channel to kick them fromn.
        * nick - Nick to kick.
        Optional arguments:
        * reason - Reason for the kick.
        """
        with self.lock:
            if self.is_in_channel(channel) == False:
                raise self.NotInChannel('LurklibError: NotInChannel')

            self.send('KICK %s %s :%s' % (channel, nick, reason))

            if self.readable():
                data = self._recv()
                ncode = data.split()[1]

                if ncode in self.error_dictionary:
                        self.exception(ncode)
                elif self.find(data, 'KICK'):
                    channel = data.split()[2]
                    if self.hide_called_events == False:
                        self._buffer.append(data)
                else:
                    self._index -= 1
            if self.compare(self.current_nick, nick):
                del self.channels[channel]

    def parse_cmode_string(self, mode_string, channel):
        """
        Parse a channel mode string and update the IRC.channels dictionary.
        Required arguments:
        * mode_string - Mode string to parse.
        * channel - Channel of which the modes were set.
        """
        with self.lock:
            modes = mode_string.split()
            targets = modes[1:]
            modes = modes[0][1:].split()

            if mode_string[0] == '+':
                plus_mode = True
            else:
                plus_mode = False
            for mode in modes:
                if mode in self.priv_types:
                    target = targets[modes.index(mode)]
                    if plus_mode:
                        if mode == 'q':
                            self.channels[channel]['USERS'][target][0] = '~'
                        elif mode == 'a':
                            self.channels[channel]['USERS'][target][1] = '&'
                        elif mode == 'o':
                            self.channels[channel]['USERS'][target][2] = '@'
                        elif mode == 'h':
                            self.channels[channel]['USERS'][target][3] = '%'
                        elif mode == 'v':
                            self.channels[channel]['USERS'][target][4] = '+'
                    else:
                        if mode == 'q':
                            self.channels[channel]['USERS'][target][0] = ''
                        elif mode == 'a':
                            self.channels[channel]['USERS'][target][1] = ''
                        elif mode == 'o':
                            self.channels[channel]['USERS'][target][2] = ''
                        elif mode == 'h':
                            self.channels[channel]['USERS'][target][3] = ''
                        elif mode == 'v':
                            self.channels[channel]['USERS'][target][4] = ''
