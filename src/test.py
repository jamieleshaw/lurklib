def on_msg ( event ): print (event)
def other ( event):
    print (event)
import __init__; irc = __init__.irc('localhost', hooks={'UNHANDLED': other, 'PRIVMSG':on_msg}, hide_called_events = False);
irc.join ( '#lawl')
irc.mainloop()