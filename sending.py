def msg ( self, target, message ):

    self.rsend ( 'PRIVSMG ' + target + ' :' + message )
    data = self.recv()
    try: ncode = data.split() [1]
    except IndexError: self.buffer.append ( data )
    if ncode in self.err_replies.keys():
            return [ False, ncode ]
    else: self.buffer.append ( data )
    return True
def notice ( self, target, message ):

    self.rsend ( 'NOTICE ' + target + ' :' + message )
    try: ncode = data.split() [1]
    except IndexError: self.buffer.append ( data )
    if ncode in self.err_replies.keys():
            return [ False, ncode ]
    else: self.buffer.append ( data )
    return True
