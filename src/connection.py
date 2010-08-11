def connect ( self, server, port ):
        '''
        connect() starts the socket connection with the server, use init() instead.
        '''
        self.s.connect ( ( server, port ) )

def init ( self, server, port, nick, ident, real_name, passwd = None, end_code = '266' ):
        '''
        init() starts the socket connection with the server, and sets your nick/ident/real name, optionally a password may be specified for the PASS command.
        '''
        self.connect ( server, port )
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
                    info = data.split()
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
                        pass
                elif ncode == '375':
                        data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '042':
                        data = ' '.join ( data.split() [3:] )
                elif ncode == '372':
                        self.motd.append ( data.split ( None, 3 ) [3] [1:] )
                        data = data.split ( ' ', 3 ) [3]
                elif ncode == '376':
                        data = ' '.join ( data.split() [3:] ) [1:]
                elif ncode == '422':
                        pass
                elif self.find ( data, 'NOTICE' ):
                        data = ( 'NOTICE', ' '.join ( data.split() [3:] ) [1:] )
                if ncode == end_code: break
                self.con_msg.append ( data )

        self.motd = tuple ( self.motd )
        self.con_msg = tuple ( self.con_msg )

def passwd ( self, passw ):
        '''
        passd() sends a PASS <password>, message to the server, it has one required argument the password.
        Returns True on success, False on fail.
        '''
        self.rsend ( 'PASS ' + passw )
        
        for x in range ( 2 ):
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                    return ncode
            else: self.buffer.append ( data )
def nick ( self, nick ):
        '''
        nick() is either used to set your nick upon connection to the IRC server, or used to change your nick in the current connection.
        Returns True on success, False on fail.
        '''
        self.rsend ( 'NICK ' + nick )

        for x in range ( 2 ):
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                    return ncode
            else: self.buffer.append ( data )
def ident ( self, ident, real_name ):
        '''
        ident() is used at startup to send your ident and real name.
        Returns True on success, False on fail.
        '''

        self.rsend ( 'USER ' + ident + ' 0 * :' + real_name )
        for x in range ( 2 ):
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                    return ncode
            else: self.buffer.append ( data )
def oper ( self, name, password ):
        self.rsend ( 'OPER ' + name + ' ' + password )
        snomasks = ''
        new_umodes = ''
        while 1:
                data = self.recv()
                ncode = data.split() [1]

                if ncode in self.err_replies.keys():
                        return ncode
                elif self.find ( data, 'MODE' ):
                        new_umodes = data.split() [-1] [1:]
                elif ncode == '381':
                        return [ new_umodes, snomasks ]
                elif ncode == '008':
                        snomasks = data.split ( '(' ) [1].split ( ')' ) [0]
                else: self.buffer.append ( data )
def umode ( self, nick, modes = '' ):
        self.rsend ( 'MODE ' + nick + ' ' + modes )
        while 1:
                data = self.recv()

                ncode = data.split() [1]

                if ncode in self.err_replies.keys():
                        return ncode
                elif ncode == '221':
                        return data.split() [3] [1:]
                elif self.find ( data, 'MODE' ):
                        return True
                else: self.buffer.append ( data )
def service ( self ):
        # Not yet done..obviously
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
        while 1:
                data = self.recv()
                ncode = data.split() [1]

                if ncode in self.err_replies.keys():
                        return ncode
                    
                elif self.find ( data, 'SQUIT' ):
                        return True
                else: self.buffer.append ( data )
