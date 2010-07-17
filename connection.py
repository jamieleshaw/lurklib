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
        data = self.recv()
        while 1:
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

                                        if self.find ( x, 'CASEMAPPING' ):
                                                self.encoding = x.split ( '=' ) [1]
                elif self.find ( data, '251' ):
                        pass
                elif self.find ( data, '255' ):
                        pass
                elif self.find ( data, '265' ):
                        pass
                elif self.find ( data, '266' ):
                        pass
                elif self.find ( data, '375' ):
                        pass
                elif self.find ( data, '372' ):
                        self.motd.append ( data.split ( None, 4 ) [4] )
                elif self.find ( data, '376' ):
                        break
                elif self.find ( data, '422' ):
                        break
                data = self.recv()
                self.con_msg.append ( data )
        con_lock = self.init_junk_count
        while con_lock != 0:
                self.con_msg.append ( self.pdata() )
                con_lock -= 1

        if self.motd != []:
                return True
        return False
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
        err_replies = {
                '431' : 'ERR_NONICKNAMEGIVEN',
                '433' : 'ERR_NICKNAMEINUSE',
                '437' : 'ERR_UNAVAILRESOURCE',
                '432' : 'ERR_ERRONEUSNICKNAME',
                '436' : 'ERR_NICKCOLLISION',
                '484' : 'ERR_RESTRICTED'
                }
        self.rsend ( 'NICK ' + nick )

        data = self.recv()
        if data.split() [1] in err_replies.keys():
                return False
        else: self.buffer.append ( data )
        return True
def ident ( self, ident, real_name ):
        '''
        ident() is used at startup to send your ident and real name.
        '''
        err_replies = {
                '461' : 'ERR_NEEDMOREPARAMS',
                '462' : 'ERR_ALREADYREGISTRED'
                }
        self.rsend ( 'USER ' + ident + ' 0 * :' + real_name )
        
        data = self.recv()
        if data.split() [1] in err_replies.keys():
                return False
        else: self.buffer.append ( data )
        return True
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
