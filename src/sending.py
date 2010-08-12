def msg ( self, target, message ):

    self.rsend ( 'PRIVMSG ' + target + ' :' + message )

def notice ( self, target, message ):

    self.rsend ( 'NOTICE ' + target + ' :' + message )
