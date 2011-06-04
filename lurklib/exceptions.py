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

""" Exceptions and such. """


class _Exceptions(object):
    """
    Exception data and such is defined here, including -
    error_dictionary - Maps IRC error codes to their Lurklib exception.
    The IRC exceptions are also defined here.
    """
    error_dictionary = { \
                    '407': 'TooManyTargets',
                    '402': 'NoSuchServer',
                    '476': 'BadChanMask',
                    '474': 'BannedFromChan',
                    '443': 'UserOnChannel',
                    '442': 'NotOnChannel',
                    '441': 'UserNotInChannel',
                    '461': 'NeedMoreParams',
                    '472': 'UnknownMode',
                    '473': 'InviteOnlyChan',
                    '405': 'TooManyChannels',
                    '471': 'ChannelIsFull',
                    '403': 'NoSuchChannel',
                    '477': 'NoChanModes',
                    '401': 'NoSuchNick',
                    '475': 'BadChannelKey',
                    '437': 'UnavailReSource',
                    '467': 'KeySet',
                    '482': 'ChanOPrivsNeeded',
                    '431': 'NoNickNameGiven',
                    '433': 'NicknameInUse',
                    '432': 'ErrorneusNickname',
                    '436': 'NickCollision',
                    '484': 'Restricted',
                    '462': 'AlreadyRegistred',
                    '411': 'NoRecipient',
                    '404': 'CannotSendToChan',
                    '414': 'WildTopLevel',
                    '412': 'NoTextToSend',
                    '413': 'NoTopLevel',
                    '491': 'NoOperHost',
                    '464': 'PasswdMismatch',
                    '501': 'UmodeUnknownFlag',
                    '502': 'UsersDontMatch',
                    '481': 'NoPrivileges',
                    '483': 'CantKillServer'
                    }

    class LurklibError(Exception):
        pass

    class NotImplemented(Exception):
        pass

    class IRCError(LurklibError):
        pass

    class NoPrivileges(IRCError):
        pass

    class NoSuchNick(IRCError):
        pass

    class UserOnChannel(IRCError):
        pass

    class NotOnChannel(IRCError):
        pass

    class UserNotInChannel(IRCError):
        pass

    class WildTopLevel(IRCError):
        pass

    class NeedMoreParams(IRCError):
        pass

    class AlreadyRegistred(IRCError):
        pass

    class NickCollision(IRCError):
        pass

    class UnavailReSource(IRCError):
        pass

    class UmodeUnknownFlag(IRCError):
        pass

    class NoTopLevel(IRCError):
        pass

    class Restricted(IRCError):
        pass

    class ChanOPrivsNeeded(IRCError):
        pass

    class UsersDontMatch(IRCError):
        pass

    class NoRecipient(IRCError):
        pass

    class UnknownMode(IRCError):
        pass

    class NoOperHost(IRCError):
        pass

    class NoTextToSend(IRCError):
        pass

    class CannotSendToChan(IRCError):
        pass

    class NicknameInUse(IRCError):
        pass

    class TooManyTargets(IRCError):
        pass

    class InviteOnlyChan(IRCError):
        pass

    class TooManyChannels(IRCError):
        pass

    class ChannelIsFull(IRCError):
        pass

    class BadChanMask(IRCError):
        pass

    class NoSuchServer(IRCError):
        pass

    class BannedFromChan(IRCError):
        pass

    class BadChannelKey(IRCError):
        pass

    class NoSuchChannel(IRCError):
        pass

    class CantKillServer(IRCError):
        pass

    class NoNickNameGiven(IRCError):
        pass

    class ErrorneusNickname(IRCError):
        pass

    class KeySet(IRCError):
        pass

    class PasswdMismatch(IRCError):
        pass

    class NoChanModes(IRCError):
        pass

    class AlreadyInChannel(LurklibError):
        pass

    class NotInChannel(LurklibError):
        pass

    class UnhandledEvent(LurklibError):
        pass

    def exception(self, ncode):
        """
        Looks up the exception in error_dictionary and raises it.
        Required arguments:
        * ncode - Error numerical code.
        """
        error = self.error_dictionary[ncode]
        error_msg = self._buffer[self._index - 1].split(None, 3)[3]
        exec('raise self.%s("%s: %s")' % (error, error, error_msg))
