import unittest
from commonbase import CommonBase


class test__ServerQueries(CommonBase):
    def test_admin(self):
        pass

    def test_get_lusers(self):
        pass

    def test_get_motd(self):
        pass

    def test_kill(self):
        pass

    def test_links(self):
        pass

    def test_s_connect(self):
        pass

    def test_s_info(self):
        pass

    def test_servlist(self):
        pass

    def test_squery(self):
        pass

    def test_stats(self):
        pass

    def test_time(self):
        self.server_nsend('391', \
                          'Lurklib.test :Saturday' + \
                          ' November 13 2010 -- 17:02 +11:00')
        self.assertEqual(self.client.time(), \
                         'Saturday November 13 2010 -- 17:02 +11:00')

    def test_trace(self):
        pass

    def test_version(self):
        pass

if __name__ == '__main__':
    unittest.main()
