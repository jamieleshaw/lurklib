import __init__
print ( 'Connecting' )
irc = __init__.irc('localhost')

print ( 'Connected' )
for x in irc.con_msg: print ( x )
print ( irc.info )
while 1:
    try: print ( irc.recv() )
    except KeyboardInterrupt:
        irc.disconnect()
        break