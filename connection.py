def connect ( self, server, port ):
        '''
        connect() starts the socket connection with the server, use init() instead.
        '''
        self.s.connect ( ( server, port ) )

def init ( self, server, port, nick, ident, real_name, passwd = None ):
        '''
        init() starts the socket connection with the server, and sets your nick/ident/real name, optionally a password may be specified for the PASS command..
        '''
        self.connect ( server, port )
        if passwd != None:
            self.passw ( passwd )
        self.nick ( nick )
        self.ident ( ident, real_name )

def passw ( self, passwd ):
        '''
        passw() sends a PASS <password>, message to the server, it has one required argument the password.
        Returns, False if it fails.
        '''
        self.rsend ( 'PASS ' + passwd )

def nick ( self, nick ):
        '''
        nick() is either used to set your nick upon connection to the IRC server, or used to change your nick in the current connection.
        '''
        self.rsend ( 'NICK ' + nick )

def ident ( self, ident, real_name ):
        '''
        ident() is used at startup to send your ident and real name.
        '''
        self.rsend ( 'USER ' + ident + ' 0 * :' + real_name )

def oper ( self, name, password ):
        self.rsend ( 'OPER ' + name + ' ' + password )

def umode ( self, nick, modes ):
        self.rsend ( 'MODE ' + nick + ' ' + modes )

def service ( self ):
        # Not Implemented, because, I haven't seen this yet....
        pass

def quit ( self, reason = None ):
        '''
        quit() sends the QUIT command to the server, optionally a quit message may be specified, use disconnect() instead.
        '''
        if reason == None:
            self.rsend ( 'QUIT' )
        else:
            self.rsend ( 'QUIT :' + reason )

def disconnect ( self, reason = None ):
        '''
        disconnect(), sends the quit message to the server, optionally a quit message may be specified, it also closes the socket connection.
        '''
        self.quit ( reason )
        self.s.close()

def squit ( self, server, msg ):
        self.rsend ( 'SQUIT ' + server + ' :' + msg )
