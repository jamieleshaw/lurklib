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

""" Channel-related interaction file. """

from __future__ import with_statement


class _Channel(object):
    """ Channel-related interaction class. """
    def is_in_channel(self, channel, should_be=True):
        """
        Find out if you are in a channel.
        Required arguments:
        * channel - Channel to check whether you are in it or not.
        * should_be - If True, raise an exception if you aren't in the channel;
                    If False, raise an exception if you are in the channel.
        """
        with self.lock:
            for channel_ in self.channels:
                if self.compare(channel_, channel):
                    if not should_be:
                        raise \
                    self.AlreadyInChannel('LurklibError: AlreadyInChannel')
                    return None
            if should_be:
                raise self.NotInChannel('LurklibError: NotInChannel')

    def join_(self, channel, key=None, process_only=False):
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
            self.is_in_channel(channel, False)
            if not process_only:
                if key:
                    self.send('JOIN %s %s' % (channel, key))
                else:
                    self.send('JOIN %s' % channel)

            while self.readable(4):
                msg = self._recv(rm_colon=True, \
                                 expected_replies=('332', '333', \
                                                   '353', 'JOIN', '366'))

                if msg[0] == '332':
                    topic = msg[2].split(':', 1)[1]
                elif msg[0] == '333':
                    set_by, time_set = msg[2].split(' ', 3)[1:]
                    if not self.UTC:
                        time_set = self._m_time.localtime(int(time_set))
                    else:
                        time_set = self._m_time.gmtime(int(time_set))
                    set_by = self._from_(set_by)

                elif msg[0] == '353':
                    users.extend(msg[2].split(':', 1)[1].split())
                elif msg[0] == 'JOIN':
                    channel = msg[1]
                    self.channels[channel] = {}
                    if not self.hide_called_events:
                        self.stepback(append=True)
                elif msg[0] == '366':
                    break
            self.channels[channel] = {}
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

    def part(self, channel, reason=''):
        """
        Part a channel.
        Required arguments:
        * channel - Channel to part.
        Optional arguments:
        * reason='' - Reason for parting.
        """
        with self.lock:
            self.is_in_channel(channel)

            self.send('PART %s :%s' % (channel, reason))
            msg = self._recv(expected_replies=('PART',))
            if msg[0] == 'PART':
                del self.channels[msg[1]]
                if not self.hide_called_events:
                    self.stepback()

    def cmode(self, channel, modes=''):
        """
        Sets or gets the channel mode.
        Required arguments:
        * channel - Channel to set/get modes of.
        Optional arguments:
        * modes='' - Modes to set.
            If not specified return the modes of the channel.
        """
        with self.lock:
            self.is_in_channel(channel)

            if not modes:
                    self.send('MODE %s' % channel)
                    modes = ''
                    mode_set_time = None
                    while self.readable():
                        msg = self._recv(rm_colon=True, \
                        expected_replies=('324', '329'))
                        if msg[0] == '324':
                            modes = msg[2].split()[1].replace('+', '', 1)
                        elif msg[0] == '329':
                            mode_set_time = self._m_time.localtime( \
                                                        int(msg[2].split()[1]))
                    return modes, mode_set_time
            else:
                self.send('MODE %s %s' % (channel, modes))

                if self.readable():
                    msg = self._recv(expected_replies=('MODE',), \
                                         ignore_unexpected_replies=True)
                    if msg[0]:
                        mode = msg[2]
                        self.parse_cmode_string(mode, msg[1])
                        if not self.hide_called_events:
                            self.stepback()

    def banlist(self, channel):
        """
        Get the channel banlist.
        Required arguments:
        * channel - Channel of which to get the banlist for.
        """
        with self.lock:
            self.is_in_channel(channel)

            self.send('MODE %s b' % channel)
            bans = []

            while self.readable():
                msg = self._recv(expected_replies=('367', '368'))
                if msg[0] == '367':
                    banmask, who, timestamp = msg[2].split()[1:]
                    bans.append((self._from_(banmask), who, \
                                 self._m_time.localtime(int(timestamp))))
                elif msg[0] == '368':
                    break
            return bans

    def exceptlist(self, channel):
        """
        Get the channel exceptlist.
        Required arguments:
        * channel - Channel of which to get the exceptlist for.
        """
        with self.lock:
            self.is_in_channel(channel)

            self.send('MODE %s e' % channel)
            excepts = []

            while self.readable():
                msg = self._recv(expected_replies=('348', '349'))

                if msg[0] == '348':
                    exceptmask, who, timestamp = msg[2].split()[1:]
                    excepts.append((self._from_(exceptmask), who, \
                                    self._m_time.localtime(int(timestamp))))
                elif msg[0] == '349':
                    break

            return excepts

    def invitelist(self, channel):
        """
        Get the channel invitelist.
        Required arguments:
        * channel - Channel of which to get the invitelist for.
        """
        with self.lock:
            self.is_in_channel(channel)

            self.send('MODE %s i' % channel)
            invites = []

            while self.readable():
                msg = self._recv(expected_replies=('346', '347'))

                if msg[0] == '346':
                    invitemask, who, timestamp = msg[2].split()[1:]
                    invites.append((self._from_(invitemask), who, \
                                    self._m_time.localtime(int(timestamp))))
                elif msg[0] == '347':
                    break

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
            self.is_in_channel(channel)

            if topic:
                self.send('TOPIC %s :%s' % (channel, topic))
                if self.readable():
                    msg = self._recv(expected_replies=('TOPIC',))
                    if msg[0] == 'TOPIC' and self.hide_called_events:
                        channel = msg[1]
                        self.channels[channel]['TOPIC'] = \
                        msg[2].replace(':', '', 1)
                        if not self.hide_called_events:
                            self.stepback()
            else:
                topic = ''
                set_by = ''
                time_set = ''
                self.send('TOPIC %s' % channel)
                while self.readable():
                    msg = self._recv(expected_replies=('332', '333', '331'))
                    if msg[0] == '332':
                        topic = msg[2].split(':', 1)[1]
                    elif msg[0] == '333':
                        set_by, time_set = msg[2].split()[1:]
                        if self.UTC == False:
                            time_set = self._m_time.localtime(int(time_set))
                        else:
                            time_set = self._m_time.gmtime(int(time_set))
                        set_by = self._from_(set_by)
                    elif msg[0] == '331':
                        topic = ''

                return topic, set_by, time_set

    def names(self, channel):
        """
        Get a list of users in the channel.
        Required arguments:
        * channel - Channel to get list of users for.
        """
        with self.lock:
            self.is_in_channel(channel)

            self.send('NAMES %s' % channel)
            names = []

            while self.readable():
                msg = self._recv(expected_replies=('353', '366'))

                if msg[0] == '353':
                    new_names = msg[2].split()[2:]
                    new_names[0] = new_names[0].replace(':', '', 1)
                    names.extend(new_names)
                elif msg[0] == '366':
                    channel = msg[2].split()[0]
                    break

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

    def list_(self):
        """ Gets a list of channels on the server. """
        with self.lock:
            self.send('LIST')
            list_ = {}

            while self.readable():
                msg = self._recv(expected_replies=('322', '321', '323'))

                if msg[0] == '322':
                    channel, usercount, modes, topic = msg[2].split(' ', 3)
                    modes = modes.replace(':', '', 1).replace(':', '', 1)
                    modes = modes.replace('[', '').replace( \
                                                    ']', '').replace('+', '')
                    list_[channel] = usercount, modes, topic
                elif msg[0] == '321':
                    pass
                elif msg[0] == '323':
                    break

            return list_

    def invite(self, channel, nick):
        """
        Invite someone to a channel.
        Required arguments:
        * channel - Channel to invite them to.
        * nick - Nick to invite.
        """
        with self.lock:
            self.is_in_channel(channel)

            self.send('INVITE %s %s' % (nick, channel))

            while self.readable():
                    msg = self._recv(expected_replies=('341', '301'))

                    if msg[0] == '341':
                        pass
                    elif msg[0] == '301':
                        away_msg = msg[2].split()[1].replace(':', '', 1)
                        return 'AWAY', away_msg

    def kick(self, channel, nick, reason=''):
        """
        Kick someone from a channel.
        Required arguments:
        * channel - Channel to kick them from.
        * nick - Nick to kick.
        Optional arguments:
        * reason - Reason for the kick.
        """
        with self.lock:
            self.is_in_channel(channel)

            self.send('KICK %s %s :%s' % (channel, nick, reason))

            if self.readable():
                msg = self._recv(expected_replies=('KICK',))

                if msg[0] == 'KICK':
                    channel = msg[1]
                    if not self.hide_called_events:
                        self.stepback()

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
