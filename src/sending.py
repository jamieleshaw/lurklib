def msg ( self, target, message ):

    self.rsend ( 'PRIVMSG ' + target + ' :' + message )
    data = self.recv()
    ncode = data.split() [1]

    if ncode in self.err_replies.keys():
            return ncode
    elif ncode == '301':
        return [ 'AWAY', data.split ( None, 3 ) [3] [1:] ]
    else: self.index -= 1
    return True
def notice ( self, target, message ):

    self.rsend ( 'NOTICE ' + target + ' :' + message )
    data = self.recv()
    ncode = data.split() [1]

    if ncode in self.err_replies.keys():
            return ncode
    elif ncode == '301':
        return [ 'AWAY', data.split ( None, 3 ) [3] [1:] ]
    else: self.index -= 1
    return True
