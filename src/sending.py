def msg ( self, target, message ):

    self.rsend ( 'PRIVMSG ' + target + ' :' + message )
    if self.readable():
        data = self.recv()
        ncode = data.split() [1]
        if ncode in self.err_replies.keys():
            return ( 'AWAY', data.split ( None, 3 ) [3] [1:] )
            
def notice ( self, target, message ):

    self.rsend ( 'NOTICE ' + target + ' :' + message )
    if self.readable():
        data = self.recv()
        ncode = data.split() [1]
        if ncode in self.err_replies.keys():
            return ( 'AWAY', data.split ( None, 3 ) [3] [1:] )