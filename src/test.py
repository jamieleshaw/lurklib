def on_msg ( event ): print (event)
def other ( event):
    print (event)
import __init__; irc = __init__.irc('irc.codeshock.org', hooks={'UNHANDLED': other, 'PRIVMSG':on_msg});
irc.mainloop()