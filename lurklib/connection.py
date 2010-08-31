def connect ( self, server, port, ssl_on = False ):
        '''
        connect() opens a socket connection with a server.
        '''
        if ssl_on == True:
            self.s = self.ssl.wrap_socket ( self.s )
        self.s.connect ( ( server, port ) )
        self.ssl_on = ssl_on

def init ( self, server, port = None, nick = 'lurklib', ident = 'lurklib', real_name = 'The Lurk Internet Relay Chat Library', passwd = None, ssl_on = False ):
        '''
        init() starts the socket connection with the server, and sets your nick/ident/real name, optionally a password may be specified for the PASS command, as-well as processing numerics etc.
        '''
        if ssl_on:
            if port == None:
                port = 6697
            self.connect ( server, port, True )
        else:
            if port == None:
                port = 6667
            
            self.connect ( server, port )
        while self.readable():
            data = self.recv()
            if self.find ( data, 'NOTICE' ):
                    self.server = data.split() [0] [1:]
                    data = ( 'NOTICE', ' '.join ( data.split() [3:] ) [1:] )
            self.con_msg.append ( data )
        
        if passwd != None:
                self.passwd ( passwd )
        self.nick ( nick )
        self.ident ( ident, real_name )
        
        while 1:
                data = self.recv()
                ncode = data.split() [1]
                if ncode == '001':
                    data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '002':
                    data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '003':
                    data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '004':
                    info = data.split()
                    self.server = info [3]
                    self.ircd = info [4]
                    self.umodes = info [5]
                    self.cmodes = info [6]
                    data = ' '.join ( data.split() [3:] )
                elif ncode == '005':
                    info = data.split() [3:]
                    for x in info:
                            try:
                                x = x.split ( '=' )
                                name = x [0]
                                value = x [1]
                                self.info [ name ] = value
                        
                                if name == 'CHARSET': self.encoding = value
                            except IndexError: 
                                self.info [ x [0] ] = True
                    data = ' '.join ( data.split() [3:] )
                elif ncode == '251':
                    data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '252':
                    data = ' '.join ( data.split() [3:] )
                elif ncode == '254':
                    data = ' '.join ( data.split() [3:] )
                elif ncode == '255':
                    data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '265':
                    data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '266':
                    data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '375':
                    data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '042':
                    data = ' '.join ( data.split() [3:] )
                elif ncode == '372':
                    self.motd.append ( data.split ( None, 3 ) [3] [1:] )
                    data = data.split ( ' ', 3 ) [3] [1:]
                elif ncode == '376':
                    data = ' '.join ( data.split() [3:] ) [1:]
                    self.con_msg.append ( data )
                    self.connected = True
                    break
                elif ncode == '422':
                    data = ' '.join ( data.split() [3:] ) [1:]
                    self.con_msg.append ( data )
                    self.connected = True
                    break
                elif self.find ( data, 'NOTICE' ):
                    self.server = data.split() [0] [1:]
                    data = ( 'NOTICE', ' '.join ( data.split() [3:] ) [1:] )
                else: self.buffer.append ( data )
                self.con_msg.append ( data )

        self.motd = tuple ( self.motd )
        self.con_msg = tuple ( self.con_msg )

def passwd ( self, passw ):
        '''
        passwd() sends a PASS <password>, message to the server, it has one required argument the password.
        '''
        self.rsend ( 'PASS :' + passw )
        
        if self.readable():
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                    self.exception ( ncode )
            else: self.index -= 1

def nick ( self, nick ):
        '''
        nick() is either used to set your nick upon connection to the IRC server, or used to change your nick in the current connection.
        '''
        self.rsend ( 'NICK :' + nick )
        self.current_nick = nick
        if self.readable():
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                    self.exception ( ncode )
            elif data.split() [1] == 'NICK' and self.hide_called_events: pass
            else: self.index -= 1
def ident ( self, ident, real_name ):
        '''
        ident() is used at startup to send your ident and real name.
        '''

        self.rsend ( 'USER ' + ident + ' 0 * :' + real_name )
        if self.readable():
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                    self.exception ( ncode )
            else: self.index -= 1

def oper ( self, name, password ):
    '''
    oper() accepts two arguments, oper name & password
    '''
    
    self.rsend ( 'OPER ' + name + ' ' + password )
    snomasks = ''
    new_umodes = ''
    if self.readable():
            data = self.recv()
            ncode = data.split() [1]

            if ncode in self.err_replies.keys():
                    self.exception ( ncode )
            elif self.find ( data, 'MODE' ):
                    new_umodes = data.split() [-1] [1:]
            elif ncode == '381':
                    return ( new_umodes, snomasks )
            elif ncode == '008':
                    snomasks = data.split ( '(' ) [1].split ( ')' ) [0]
            else: self.buffer.append ( data )
def umode ( self, nick, modes = '' ):
    '''
    umode() accepts a nick and optionally modes to set.
    If no modes are specified, it returns your current umodes.
    '''
    if modes == '':
        self.rsend ( 'MODE ' + nick )
        modes = []
        while self.readable(): modes.append ( self.recv().split() [4:] )
        return modes
        
    else: self.rsend ( 'MODE ' + nick + ' ' + modes )
    while self.readable():
            data = self.recv()

            ncode = data.split() [1]

            if ncode in self.err_replies.keys():
                    self.exception ( ncode )
            elif ncode == '221':
                    return data.split() [3] [1:]
            elif self.find ( data, 'MODE' ) and self.hide_called_events:
                    pass
            else: self.buffer.append ( data )
def service ( self ):
        pass

def quit ( self, reason = None ):
        '''
        quit() sends the QUIT command to the server, optionally a quit message may be specified, use end() instead.
        '''
        if reason == None:
            self.rsend ( 'QUIT' )
        else:
            self.rsend ( 'QUIT :' + reason )

def end ( self, reason = None ):
        '''
        end(), sends the quit message to the server, optionally a quit message may be specified, it also closes the socket connection.
        '''
        self.quit ( reason )
        self.keep_going = False
        self.s.shutdown ( 2 )
        self.s.close()
        
def squit ( self, server, msg ):
    '''
    squit() squits the specified server.
    '''
    self.rsend ( 'SQUIT ' + server + ' :' + msg )
    while self.readable():
            data = self.recv()
            ncode = data.split() [1]

            if ncode in self.err_replies.keys():
                    self.exception ( ncode )
                
            elif self.find ( data, 'SQUIT' ) and self.hide_called_events:
                    pass
            else: self.buffer.append ( data )
