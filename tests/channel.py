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


class ChannelTest:
    def test_11(self):
        """ Test is_in_channel() method. """
        self.assertFalse(self.irc.is_in_channel('#channel'))

    def test_12(self):
        """ Test join() method. """
        self.ircd.rsend(':Lurklib!user@host JOIN #Test')
        self.ircd.nsend('332', '#Test :TheTopic')
        self.ircd.nsend('333', '#Test TopicBot 1279950991')
        self.ircd.nsend('353', '= #Bots :@TopicBot Lurklib')
        self.ircd.nsend('366', '#Bots :End of /NAMES list.')
        self.assertEqual(str(self.irc.join('#Test')), \
                         """(['@TopicBot', 'Lurklib'], 'TheTopic',""" + \
                         """ 'TopicBot', time.struct_time(tm_ye""" + \
                         """ar=2010, tm_mon=7, tm_mday=24,""" + \
                         """ tm_hour=15, tm_min=56, """ + \
                         """tm_sec=31, tm_wday=5, tm_yday=205, tm_isdst=0))""")
        self.assertEqual(self.ircd.recv(), 'JOIN #Test')
        self.assertEqual(self.irc.channels, \
                         {'#Test': {'USERS': \
                                    {'Lurklib': ['', '', '', '', ''], \
                            'TopicBot': ['', '', '@', '', '']}}})

    def test_13(self):
        """ Test part() method. """
        pass

    def test_14(self):
        """ Test cmode() method. """

    def test_15(self):
        """ Test banlist() method. """
        pass

    def test_16(self):
        """ Test exceptlist() method. """
        pass

    def test_17(self):
        """ Test invitelist() method. """
        pass

    def test_18(self):
        """ Test topic() method. """
        pass

    def test_19(self):
        """ Test names() method. """
        pass

    def test_20(self):
        """ Test list_() method. """

    def test_30(self):
        """ Test invite() method. """

    def test_31(self):
        """ Test kick() method. """

    def test_32(self):
        """ Test parse_cmode_string() method. """
        pass
