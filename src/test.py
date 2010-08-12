def other ( event):
    print (event)
def msg (event):
    print(event)
import __init__; irc = __init__.irc('irc.codeshock.org', ssl_on=True, hooks={'UNHANDLED': other } );
for x in irc.con_msg: print (x)
irc.set_hook ( 'PRIVMSG', msg)
irc.mainloop()