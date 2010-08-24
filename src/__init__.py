import socket, sys, ssl, time
sys.path.append ( './lurklib' )
__version__ = 'Alpha 1.5'
# Import IRC Sub-Modules
import connection
import channel
import uqueries
import squeries
import sending

class irc:

    for x in dir ( connection ): exec ( x + ' = connection.' + x )
    for x in dir ( channel ): exec ( x + ' = channel.' + x )
    for x in dir ( uqueries ): exec ( x + ' = uqueries.' + x )
    for x in dir ( squeries ): exec ( x + ' = squeries.' + x )
    for x in dir ( sending ) : exec ( x + ' = sending.' + x )


    def __init__ ( self, server = None, port = None, nick = 'lurklib', ident = 'lurklib', real_name = 'The Lurk Internet Relay Chat Library', passwd = None, ssl_on = False, encoding = 'UTF-8', clrf = '\r\n', hooks = {}, hide_called_events = True, ctcps = None ):
        '''
        Initial Class Variables.
        '''
        self.current_nick = nick
        self.index = 0
        self.hooks = hooks
        self.hide_called_events = hide_called_events
        self.con_msg = []
        self.ircd = ''
        self.lusers = {}
        self.clrf = clrf
        self.umodes = ''
        self.cmodes = ''
        self.server = ''
        self.ssl_on = ssl_on
        self.ssl = ssl
        self.buffer = []
        self.s = socket.socket()
        self.fallback_encoding = encoding
        self.encoding = encoding
        self.motd = []
        self.info = {}
        self.channels = []
        self.time = time
        if ctcps == None:
            self.ctcps = { \
             'VERSION' : 'The Lurk Internet Relay Chat Library : ' + __version__,
             'SOURCE' : 'http://codeshock.org/',
             'PING' : 1,
             'TIME' : self.time.asctime,
             }
        else: self.ctcps = ctcps

        
        self.IRCError = Exception
        self.NOPRIVILEGES = self.IRCError
        self.NOSUCHNICK = self.IRCError
        self.USERONCHANNEL = self.IRCError
        self.NOTONCHANNEL = self.IRCError
        self.USERNOTINCHANNEL = self.IRCError
        self.WILDTOPLEVEL = self.IRCError
        self.NEEDMOREPARAMS = self.IRCError
        self.ALREADYREGISTRED = self.IRCError
        self.NICKCOLLISION = self.IRCError
        self.UNAVAILRESOURCE = self.IRCError
        self.UMODEUNKNOWNFLAG = self.IRCError
        self.NOTOPLEVEL = self.IRCError
        self.RESTRICTED = self.IRCError
        self.CHANOPRIVSNEEDED = self.IRCError
        self.USERSDONTMATCH = self.IRCError
        self.NORECIPIENT = self.IRCError
        self.UNKNOWNMODE = self.IRCError
        self.NOOPERHOST = self.IRCError
        self.NOTEXTTOSEND = self.IRCError
        self.CANNOTSENDTOCHAN = self.IRCError
        self.NICKNAMEINUSE = self.IRCError
        self.TOOMANYTARGETS = self.IRCError
        self.INVITEONLYCHAN = self.IRCError
        self.TOOMANYCHANNELS = self.IRCError
        self.CHANNELISFULL = self.IRCError
        self.BADCHANMASK = self.IRCError
        self.NOSUCHSERVER = self.IRCError
        self.BANNEDFROMCHAN = self.IRCError
        self.BADCHANNELKEY = self.IRCError
        self.NOSUCHCHANNEL = self.IRCError
        self.NONICKNAMEGIVEN = self.IRCError
        self.ERRONEUSNICKNAME = self.IRCError
        self.KEYSET = self.IRCError
        self.PASSWDMISMATCH = self.IRCError
        self.NOCHANMODES = self.IRCError
        self.AlreadyInChannel = Exception
        self.NotInChannel = Exception
        self.UnhandledEvent = Exception


        self.err_replies = { \
                    '407' : 'TOOMANYTARGETS',
                    '402' : 'NOSUCHSERVER',
                    '476' : 'BADCHANMASK',
                    '474' : 'BANNEDFROMCHAN',
                    '443' : 'USERONCHANNEL',
                    '442' : 'NOTONCHANNEL',
                    '441' : 'USERNOTINCHANNEL',
                    '461' : 'NEEDMOREPARAMS',
                    '472' : 'UNKNOWNMODE',
                    '473' : 'INVITEONLYCHAN',
                    '405' : 'TOOMANYCHANNELS',
                    '471' : 'CHANNELISFULL',
                    '403' : 'NOSUCHCHANNEL',
                    '477' : 'NOCHANMODES',
                    '401' : 'NOSUCHNICK',
                    '475' : 'BADCHANNELKEY',
                    '437' : 'UNAVAILRESOURCE',
                    '467' : 'KEYSET',
                    '482' : 'CHANOPRIVSNEEDED',
                    '431' : 'NONICKNAMEGIVEN',
                    '433' : 'NICKNAMEINUSE',
                    '432' : 'ERRONEUSNICKNAME',
                    '436' : 'NICKCOLLISION',
                    '484' : 'RESTRICTED',
                    '462' : 'ALREADYREGISTRED',
                    '411' : 'NORECIPIENT',
                    '404' : 'CANNOTSENDTOCHAN',
                    '414' : 'WILDTOPLEVEL',
                    '412' : 'NOTEXTTOSEND',
                    '413' : 'NOTOPLEVEL',
                    '491' : 'NOOPERHOST',
                    '464' : 'PASSWDMISMATCH',
                    '501' : 'UMODEUNKNOWNFLAG',
                    '502' : 'USERSDONTMATCH',
                    '481' : 'NOPRIVILEGES' }
        
        
        if server != None:
            self.init ( server, port, nick, ident, real_name, passwd, ssl_on )
            
    def find ( self, haystack, needle ):
        '''
        Returns False, if needle is not found in the haystack, if the needle is found in the haystack it returns True.
        '''
        qstatus = haystack.find ( needle )
        if qstatus == -1:
            return False
        elif qstatus != -1:
            return True
    def exception ( self, ncode ):
        exec ( 'raise self.' + self.err_replies [ ncode ] + ' ( "IRCError: ' + self.err_replies [ ncode ] + '" )' )
    def rsend ( self, msg ):
        '''
        rsend() provides, a raw interface to the socket allowing the sending of raw data.
        '''
        msg = msg + self.clrf
        try: data = bytes ( msg, self.encoding )
        except LookupError: data = bytes ( msg, self.fallback_encoding )
        if self.ssl_on: self.s.write ( data )
        else: self.s.send ( data )
        return msg
    def mcon ( self ):
        sdata = ' '
        while sdata [-1] != self.clrf [-1]:
                    if sdata == ' ': sdata = ''
                    if self.ssl_on:
                        try: sdata = sdata + self.s.read ( 4096 ).decode ( self.encoding )
                        except LookupError: sdata = sdata + self.s.read ( 4096 ).decode ( self.fallback_encoding )
                    else:
                        try: sdata = sdata + self.s.recv ( 4096 ).decode ( self.encoding )
                        except LookupError: sdata = sdata + self.s.recv ( 4096 ).decode ( self.fallback_encoding )
                    
        lines = sdata.split ( self.clrf )
        for x in lines:
            if x.find ( 'PING :' ) == 0:
                self.rsend ( x.replace ( 'PING', 'PONG' ) )
            if x != '': self.buffer.append ( x )
    def recv ( self ):
        if self.index == len ( self.buffer ): self.mcon()
        if self.index >= 199:
            self.resetbuffer()
            self.mcon()
        msg = self.buffer [ self.index ]
        while self.find ( msg, 'PING :' ):
            self.index += 1
            try:
                msg = self.buffer [ self.index ]
            except IndexError:
                self.mcon()
                self.index -= 1

        self.index += 1
        return msg
    def readable ( self ):
        self.s.setblocking ( 0 )
        try:
            self.mcon()
            rvalue = True
        except socket.error:
            self.time.sleep ( 1 )
            try:
                self.mcon()
                rvalue = True
            except socket.error:
                if self.index == len ( self.buffer ): rvalue = False
                else: rvalue = True
        self.s.setblocking ( 1 )
        return rvalue
    
    def resetbuffer ( self ):
        self.index, self.buffer = 0, []
    def who_is_it ( self, who ):
        try:
            host = who.split ( '@', 1 )
            nickident = host [0].split ( '!', 1 )
            nick = nickident [0]
            ident = nickident [1]
            host = host [1]
            return ( nick, ident, host )
        except IndexError: return who
    def stream ( self ):

        data = self.recv()
        segments = data.split()

        if segments [1] == 'JOIN':
            who = self.who_is_it ( segments [0] [1:] )
            channel = segments [2] [1:]
            if channel not in self.channels:
                
                topic = ''
                names = ()
                set_by = ''
                time_set = ''
                data = self.recv()
                while 1:
                        ncode = data.split() [1]
        
                        if self.find ( data, '332' ):
                                topic = data.split ( None, 4 ) [4] [1:]
                        elif self.find ( data, '333' ):
                            segments = data.split()
                            time_set = self.time.ctime ( int ( segments [5] ) )
                            set_by = self.who_is_it ( segments [4] )
                            
                        elif self.find ( data, '353' ):
                                names = data.split() [5:]
                                names [0] = names [0] [1:]
                                names = tuple ( names )
                        elif self.find ( data, 'JOIN' ):
                            self.channels.append ( data.split() [2] [1:] )
                            if self.hide_called_events == False: self.buffer.append ( data )
                        elif ncode in self.err_replies.keys(): self.exception ( ncode )
                        elif ncode == '366': break
                        else: self.buffer.append ( data )
                        data = self.recv()
                return ( topic, names, set_by, time_set )
                
            return 'JOIN', who, channel
        elif segments [1] == 'PART':
            try: return 'PART', ( self.who_is_it ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )
            except IndexError: return 'PART', ( self.who_is_it ( segments [0] [1:] ), segments [2], '' )

        elif segments [1] == 'PRIVMSG':
            who = self.who_is_it ( segments [0] [1:] )
            msg = ' '.join ( segments [3:] ) [1:]
            rvalue = 'PRIVMSG', ( who, segments [2], msg )
            
            if msg.find ( '\001' ) == 0:
                rctcp = self.ctcp_decode ( msg ).upper()
                segments = rctcp.split()
                for ctcp in self.ctcps.keys():
                    if ctcp == segments [0] and self.ctcps [ ctcp ] != None:
                        if hasattr ( self.ctcps [ ctcp ], '__call__'):
                            response = str ( self.ctcps [ ctcp ] () )
                        else:
                            try: response = ctcp + ' ' + segments [ int ( self.ctcps [ ctcp ] ) ]
                            except ValueError: response = self.ctcps [ ctcp ]
                        self.notice ( who [0], self.ctcp_encode ( response ) )
                        break
                return 'CTCP', ( rvalue [1] [:2], rctcp )
            else: return rvalue
        elif segments [1] == 'NOTICE':
            msg = ' '.join ( segments [3:] ) [1:]
            if msg.find ( '\001' ) == 0:
                msg = self.ctcp_decode( msg )
                return 'CTCP_REPLY', ( self.who_is_it ( segments [0] [1:] ), segments [2], msg )
            return 'NOTICE', ( self.who_is_it ( segments [0] [1:] ), segments [2], msg )

        elif segments [1] == 'MODE':
            try: return 'MODE', ( self.who_is_it ( segments [2] ), ' '.join ( segments [3:] ) )
            except IndexError: return 'MODE', ( segments [2], ' '.join ( segments [3:] ) [1:] )
        
        elif segments [1] == 'KICK':
            if self.current_nick == segments [3]: self.channels.remove ( segments [2] )
            return 'KICK', ( self.who_is_it ( segments [0] [1:] ), segments [2], segments [3], ' '.join ( segments [4:] ) [1:] )

        elif segments [1] == 'INVITE':
            return 'INVITE', ( self.who_is_it ( segments [0] [1:] ), segments [2], segments [3] [1:] )

        elif segments [1] == 'NICK':
            who = self.who_is_it ( segments [0] [1:] )
            new_nick = ' '.join ( segments [2:] )
            if self.current_nick == who [0]: self.current_nick = new_nick
            return 'NICK', ( who, new_nick )

        elif segments [1] == 'TOPIC':
            return 'TOPIC', ( self.who_is_it ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )

        elif segments [1] == 'QUIT':
            return 'QUIT', ( self.who_is_it ( segments [0] [1:] ), ' '.join ( segments [2:] [1:] ) )
       
        elif segments [1] == '251':
            self.lusers [ 'USERS' ] = segments [5]
            self.lusers [ 'INVISIBLE' ] = segments [8]
            self.lusers [ 'SERVERS' ] = segments [11]
            return self.stream()
        
        elif segments [1] == '252':
            self.lusers [ 'OPERATORS' ] = segments [3]
            return self.stream()
        
        elif segments [1] == '254':
            self.lusers [ 'CHANNELS' ] = segments [3]
            return self.stream()
        
        elif segments [1] == '255':
            self.lusers [ 'CLIENTS' ] = segments [5]
            self.lusers [ 'LSERVERS' ] = segments [8]
            return self.stream()
        
        elif segments [1] == '265':
            self.lusers [ 'LOCALUSERS' ] = segments [6]
            self.lusers [ 'LOCALMAX' ] = segments [8]
            return self.stream()
        
        elif segments [1] == '266':
            self.lusers [ 'GLOBALUSERS' ] = segments [6]
            self.lusers [ 'GLOBALMAX' ] = segments [8]
            return ( 'LUSERS', self.lusers )

        elif segments [1] in self.err_replies.keys():
            self.exception ( segments [1] )
        
        else: return 'UNKNOWN', data


        
    def mainloop ( self ):
        def handler():
            event = self.stream()
            if event [0] in self.hooks.keys():
                self.hooks [ event [0] ] ( event = event [1] )
            elif 'UNHANDLED' in self.hooks.keys():
                self.hooks [ 'UNHANDLED' ] ( event )
            else: raise self.UnhandledEvent ('Unhandled Event') 
        while 1:
            if self.readable() == False and 'AUTO' in self.hooks.keys():
                self.hooks [ 'AUTO' ] ()
                del self.hooks [ 'AUTO' ]
            handler()
            
    def set_hook ( self, trigger, method ):
        self.hooks [ trigger ] = method
    
    def remove_hook ( self, trigger ):
        del self.hooks [ trigger ]
    
    # CTCP methods
    
    def ctcp_encode ( self, msg ):
        return '\001' + msg + '\001'
    def ctcp_decode ( self, msg ):
        return msg.replace ( '\001', '' )