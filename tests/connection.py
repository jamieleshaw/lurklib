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


class ConnectionTest:
    def test_1(self):
        """
        Test _init() method.
        Other methods tested:
        * _register()
            * _connect()
            * _nick()
            * _user()
        """
        self.assertEqual(self.ircd.recv(), 'NICK :Lurklib')
        self.assertEqual(self.ircd.recv(), \
                         'USER Lurklib 0 * :' + \
                         'The Lurk Internet Relay Chat Library')

    def test_2(self):
        """ Test _password() method. """
        pass

    def test_3(self):
        """ Test nick() method. """
        self.ircd.nsend('433', 'NewNick :Nick in use.')
        self.irc.nick(('NewNick', 'Lurklib'))
        self.assertEqual(self.ircd.recv(), 'NICK :NewNick')
        self.assertEqual(self.ircd.recv(), 'NICK :Lurklib')

    def test_4(self):
        """ Test oper() method. """
        pass

    def test_5(self):
        """ Test umode() method. """
        pass

    def test_6(self):
        """ Test squit() method. """
        pass

    def test_7(self):
        """ Test latency() method. """
        pass

    def test_99(self):
        """
        Test quit() method.
        Other methods tested:
        * _quit()
        """
        self.irc.quit('Bye.')
        self.assertEqual(self.ircd.recv(), 'QUIT :Bye.')
