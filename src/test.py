import __init__
irc = __init__.irc()
print ( 'Connecting' )
irc.init ( 'localhost', 6667, 'LurkTest', 'lurklib', 'lurklib' )
print ( 'Connected' )
for x in irc.con_msg: print ( x )
print ( irc.info )
while 1:
    try: print ( irc.recv() )
    except KeyboardInterrupt:
        irc.disconnect()
        break