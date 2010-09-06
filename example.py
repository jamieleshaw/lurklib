import lurklib

def on_auto():
    ''' Join #bots and print it's information out. '''
    for x in range(20): print (irc.join ('#bots%d' %x))
    
def on_privmsg (event):
    ''' An event argument must be accepted by all hooked method, except the AUTO hook. '''
    if event [2].lower() == 'hello':
        irc.msg (event [1], 'Hello, %s!' % event [0] [0])
        print ('%s said hello!' % event [0] [0])
    elif event [2].lower() == '!quit':
        irc.end ('Bye!')

def on_unhandled (event):
    ''' This method will be called, when their isn't a method specified for said event. '''
    print (event)

''' Specify our hooks, and the method to be called when said hook is triggered. '''
hooks = { \
         'PRIVMSG' : on_privmsg,
         'AUTO' : on_auto,
         'UNHANDLED' : on_unhandled
         }
''' Connect to IRC, and assign the irc object, to the irc variable. '''
irc = lurklib.irc (server='localhost', nick='HelloBot', hooks=hooks)

''' Enter lurklib's mainloop which will keep you connected to IRC, and process events, and call the specified hooks when necessary. '''
irc.mainloop()
