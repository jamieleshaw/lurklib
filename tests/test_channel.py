import unittest
from commonbase import CommonBase


class test__Channel(CommonBase):
    def test_banlist(self):
        pass

    def test_cmode(self):
        pass

    def test_exceptlist(self):
        pass

    def test_invite(self):
        pass

    def test_invitelist(self):
        pass

    def test_is_in_channel(self):
        pass

    def test_join(self):
        """ Test join() method. """
        self.server_rsend(':Lurklib!user@host JOIN #Test')
        self.server_nsend('332', '#Test :TheTopic')
        self.server_nsend('333', '#Test TopicBot 1279950991')
        self.server_nsend('353', '= #Test :@TopicBot Lurklib')
        self.server_nsend('366', '#Test :End of /NAMES list.')
        self.assertEqual(str(self.client.join('#Test')), \
                         """(['@TopicBot', 'Lurklib'], 'TheTopic',""" + \
                         """ 'TopicBot', time.struct_time(tm_ye""" + \
                         """ar=2010, tm_mon=7, tm_mday=24,""" + \
                         """ tm_hour=15, tm_min=56, """ + \
                         """tm_sec=31, tm_wday=5, tm_yday=205, tm_isdst=0))""")
        self.assertEqual(self.server_recv(), 'JOIN #Test')
        self.assertEqual(self.client.channels, \
                         {'#Test': {'USERS': \
                                    {'Lurklib': ['', '', '', '', ''], \
                            'TopicBot': ['', '', '@', '', '']}}})
        self.assertEqual(self.client.recv(), [':Lurklib!user@host', 'JOIN', '#Test'])

    def test_kick(self):
        pass

    def test_list_(self):
        pass

    def test_names(self):
        pass

    def test_parse_cmode_string(self):
        pass

    def test_part(self):
        pass

    def test_topic(self):
        pass

if __name__ == '__main__':
    unittest.main()
