
def on_other ( event):
    print (event)

import __init__; irc = __init__.irc('localhost', ssl_on=False, hooks={'UNHANDLED': on_other } );
print(irc.auto ( irc.join, ('#channel',), delay = 3))





irc.mainloop()