import __init__

def notice ( event ):
    print ( event)
irc = __init__.irc('localhost', hooks = {'NOTICE': notice})
irc.mainloop()
