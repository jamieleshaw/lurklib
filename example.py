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

""" Lurklib usage example. """

SERVER = 'localhost'

import lurklib


def on_auto():
    """ Join #bots and print it's information out. """
    print(IRC.join('#bots'))


def on_privmsg(event):
    '''
    An event argument must be accepted by all hooked methods -
    except the AUTO hook.
    '''
    if event[2].lower() == 'hello':
        IRC.privmsg(event[1], 'Hello, %s!' % event[0][0])
        print('%s said hello!' % event[0][0])
    elif event[2].lower() == '!quit':
        IRC.quit('Bye!')


def on_unhandled(event):
    """
    This method will be called -
    when their isn't a method specified for said event.
    """
    print(event)

# Specify our hooks, and the method to be called when said hook is triggered.
HOOKS = { \
         'PRIVMSG': on_privmsg,
         'AUTO': on_auto,
         'UNHANDLED': on_unhandled
         }
# Connect to IRC, and assign the returned IRC object, to the IRC variable.
IRC = lurklib.IRC(server=SERVER, nick=('HelloBot', 'HelloBot-'),
                  hooks=HOOKS)

# Enter lurklib's mainloop which will keep you connected to IRC -
# and call the specified hooks when necessary.
IRC.mainloop()
