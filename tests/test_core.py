import unittest
from commonbase import CommonBase


class Test_Core(CommonBase):
    def test___init__(self):
        pass

    def test_compare(self):
        pass

    def test_ctcp_decode(self):
        pass

    def test_ctcp_encode(self):
        pass

    def test_find(self):
        pass

    def test_readable(self):
        pass

    def test__resetbuffer(self):
        pass

    def test_stepback(self):
        pass

    def test__mcon(self):
        pass

    def test__raw_recv(self):
        self.server_rsend('ABCD')
        self.assertEqual(self.client._raw_recv(), 'ABCD')
        self.assertEqual(1, self.client._index)
        self.assertEqual('ABCD', self.client._buffer[0])

    def test__recv(self):
        self.server_rsend(':Test PRIVMSG #Test :A B C D')
        self.assertEqual(self.client._recv(), \
                         [':Test', 'PRIVMSG', '#Test', ':A B C D'])
        self.client.stepback()
        self.assertEqual(self.client._recv(True), \
                         [':Test', 'PRIVMSG', '#Test', 'A B C D'])

    def test_send(self):
        pass

    def test_recv(self):
        pass

if __name__ == '__main__':
    unittest.main()
