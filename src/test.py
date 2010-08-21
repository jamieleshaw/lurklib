
def on_other ( event):
    print (event)
def IDUNNOLOL(): print ( irc.join ( '#aaa' ) )
import __init__; irc = __init__.irc('localhost', ssl_on=False, hooks={'UNHANDLED': on_other, 'AUTO': IDUNNOLOL } );

irc.mainloop()