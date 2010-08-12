def on_msg ( event ): print (event)
def other ( event):
    print (event)
import __init__; irc = __init__.irc('localhost', hooks={'UNHANDLED': other, 'PRIVMSG':on_msg}, end_of_init_extends_to_lusers = True);
irc.join ( '#lawl')
irc.mainloop()