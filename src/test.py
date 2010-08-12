def other ( event):
    print (event)
import __init__; irc = __init__.irc('irc.codeshock.org', ssl_on=True, hooks={'UNHANDLED': other } );
for x in irc.con_msg: print (x)
irc.rsend ( 'LUSERS')
irc.mainloop()