import os
import sys

sys.path.append(os.path.dirname(os.getcwd()))

import unittest
import lurklib

class CommonBase(unittest.TestCase):
    def server_rsend(self, msg):
        """
        Send a message to Lurklib
        Required arguments:
        * msg - Message to send.
        """
        self.lurklib_buffer.append(msg)

    def server_send(self, msg):
        """
        Send a message to Lurklib from the server.
        Required arguments:
        * msg - Message to send.
        """
        self.server_rsend(':Lurklib.test %s' % msg)

    def server_nsend(self, ncode, msg):
        """
        Send a numerical code and message to Lurklib.
        Required arguments:
        * ncode - Numeric code to send.
        * msg - Message to send.
        """
        self.server_send('%s Lurklib %s' % (ncode, msg))

    def server_recv(self):
        """ Receive a message from Lurklib. """
        return self.server_buffer.pop(0)

    def lurklib__connect(self, server, port):
        """ Overrides Lurklib's _connect() method.  """
        pass

    def lurklib_send(self, msg):
        """
        Overrides Lurklib's send() method.
        Send a message to the server.
        * msg - Message to send.
        """
        self.server_buffer.append(msg)

    def lurklib_readable(self, timeout=None):
        """ Overrides Lurklib's readable() method. """
        if len(self.lurklib_buffer) > self.lurklib_index:
            return True
        else:
            return False

    def setUp(self):
        """ Setup the mock server and Lurklib. """
        self.server_buffer = []
        self.lurklib_buffer = []
        self.lurklib_index = 0
        lurklib.Client._buffer = self.lurklib_buffer
        lurklib.Client._index = self.lurklib_index
        lurklib.Client._connect = self.lurklib__connect
        lurklib.Client.send = self.lurklib_send
        lurklib.Client.readable = self.lurklib_readable
        self.client = lurklib.Client(server='', hide_called_events=False)
        self.server_recv()
        self.server_recv()


if __name__ == '__main__':
    unittest.main()
