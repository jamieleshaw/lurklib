import __init__

def msg ( event ):
    print ( event)
irc = __init__.irc('localhost', hooks = {'PRIVMSG': msg})
irc.mainloop()
