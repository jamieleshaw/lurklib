
def on_other ( event):
    print (event)

import __init__; irc = __init__.irc('localhost', ssl_on=False, hooks={'UNHANDLED': on_other } );

lol = 0

while 1:
    if lol == 2:
        print ( irc.whois ( 'lk' ) )
    print(irc.stream())
    lol += 1