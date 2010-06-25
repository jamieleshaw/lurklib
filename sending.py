def msg ( self, target, message ):
    '''
    msg() accepts, 2 arguments, a target and a message to send.
    '''
    self.rsend ( 'PRIVSMG ' + target + ' :' + message )

def notice ( self, target, message ):
    '''
    notice() accepts, 2 arguments, a target and a message to send.
    '''
    self.rsend ( 'NOTICE ' + target + ' :' + message )
