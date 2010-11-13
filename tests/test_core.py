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

    def test__recv_(self):
        self.server_rsend('ABCD')
        self.assertEqual(self.client._recv_(), 'ABCD')

    def test__recv(self):
        pass

    def test_send(self):
        pass

    def test_recv(self):
        pass

if __name__ == '__main__':
    unittest.main()
