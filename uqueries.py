def who ( self, target ):
    pass

def whois ( self, nick ):
        '''
        whois() accepts, one parameter, a Nickname, it runs a whois on the User.
        '''

        self.rsend ( 'WHOIS ' + nick )

def whowas ( self, nick ):
    self.rsend ( 'WHOWAS ' + nick )
