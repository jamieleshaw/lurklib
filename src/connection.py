def connect ( self, server, port ):
        '''
        connect() starts the socket connection with the server, use init() instead.
        '''
        self.s.connect ( ( server, port ) )

def init ( self, server, port, nick, ident, real_name, passwd = None ):
        '''
        init() starts the socket connection with the server, and sets your nick/ident/real name, optionally a password may be specified for the PASS command.
        '''
        self.connect ( server, port )
        if passwd != None:
                self.passwd ( passwd )
        nstatus = self.nick ( nick )
        if nstatus != True:
                return nstatus
        
        identstatus = self.ident ( ident, real_name )
        if identstatus != True:
                return identstatus
        while 1:
                data = self.recv()

                if self.find ( data, '001' ):
                        pass
                elif self.find ( data, '002' ):
                        pass
                elif self.find ( data, '003' ):
                        pass
                elif self.find ( data, '004' ):
                        info = data.split()
                        self.server = info [3]
                        self.ircd = info [4]
                        self.umodes = info [5]
                        self.cmodes = info [6]
                elif self.find ( data, '005' ):
                        if self.network == '':
                                info = data.split()
                                for x in info:
                                        if self.find ( x, 'NETWORK' ):
                                                self.network = x.split ( '=' ) [1]          
                                        elif self.find ( x, 'CHARSET' ):
                                                self.encoding = x.split ( '=' ) [1]
                elif self.find ( data, '251' ):
                        pass
                elif self.find ( data, '255' ):
                        pass
                elif self.find ( data, '265' ):
                        pass
                elif self.find ( data, '266' ):
                        break
                elif self.find ( data, '375' ):
                        pass
                elif self.find ( data, '042' ):
                        pass
                elif self.find ( data, '372' ):
                        self.motd.append ( data.split ( None, 3 ) [3] [1:] )
                elif self.find ( data, '376' ):
                        pass
                elif self.find ( data, '422' ):
                        pass
                elif self.find ( data, 'NOTICE' ):
                        #self.index -= 1
                        #data = self.stream()
                        pass
                self.con_msg.append ( data )
                self.motd = tuple ( self.motd )
        return True

def passwd ( self, passw ):
        '''
        passd() sends a PASS <password>, message to the server, it has one required argument the password.
        Returns True on success, False on fail.
        '''
        self.rsend ( 'PASS ' + passw )
        
        data = self.recv()
        ncode = data.split() [1]
        if ncode in self.err_replies.keys():
                return ncode
        elif self.find ( data, 'NOTICE' ) == False: self.index -= 1
        return True
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
