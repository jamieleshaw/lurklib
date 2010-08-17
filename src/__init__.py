import socket, sys, ssl, threading
sys.path.append ( './lurklib' )
# Import IRC Sub-Modules

import connection
import channel
import uqueries
import squeries
import sending

class irc:

    # Put them in this namespace...I'm sure there is a cleaner way of doing this, but I've haven't found it yet...
    for x in dir ( connection ): exec ( x + ' = connection.' + x )
    for x in dir ( channel ): exec ( x + ' = channel.' + x )
    for x in dir ( uqueries ): exec ( x + ' = uqueries.' + x )
    for x in dir ( squeries ): exec ( x + ' = squeries.' + x )
    for x in dir ( sending ) : exec ( x + ' = sending.' + x )


    def __init__ ( self, server = None, port = None, nick = 'lurklib', ident = 'lurklib', real_name = 'The Lurk Internet Relay Chat Library', passwd = None, ssl_on = False, encoding = 'utf-8', clrf = '\r\n', hooks = {}, hide_called_events = True ):
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
        self.threading = threading
        self.buffer = [ ]
        self.s = socket.socket()
        self.fallback_encoding = encoding
        self.encoding = encoding
        self.motd = []
        self.info = {}
        
        self.join_event_generated_internally = False # var to make sure the sajoin detection doesn't conflict with hide_called_events = False
        
        
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
    def resetbuffer ( self ):
        self.index, self.buffer = 0, []
    def stream ( self ):
        '''
        stream() == Main function etc
        '''
        def who ( who ):
            try:
                host = who.split ( '@', 1 )
                nickident = host [0].split ( '!', 1 )
                nick = nickident [0]
                ident = nickident [1]
                host = host [1]
                return ( nick, ident, host )
            except IndexError: return who
        data = self.recv()
        segments = data.split()
        if segments [1] == 'JOIN':
            who_is_it = who ( segments [0] [1:] )
            
            if who_is_it [0] == self.current_nick and self.join_event_generated_internally == False:
                data = self.recv()
                topic = ''
                names = ()
                while 1:
                    if self.find ( data, '332' ):
                        topic = data.split ( None, 4 ) [4] [1:]
                    elif self.find ( data, '333' ):
                        # implement topic, setter and time set collection
                        pass
                    elif self.find ( data, '353' ):
                        names = data.split() [5:]
                        names [0] = names [0] [1:]
                    elif self.find ( data, '366' ):
                        break
                    data = self.recv() 
                return 'JOIN', who_is_it, segments [2] [1:], topic, tuple ( names )
            #if self.hide_called_events == False: self.join_event_generated_internally = False
            else: return 'JOIN', who_is_it, segments [2] [1:]
        elif segments [1] == 'PART':
            try: return 'PART', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )
            except IndexError: return 'PART', ( who ( segments [0] [1:] ), segments [2], '' )

        elif segments [1] == 'PRIVMSG':
            
            privmsg = 'PRIVMSG', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )
            if privmsg [1] [2].find ( '\001' ) == 0:
                if privmsg [1] [2].find ( 'VERSION' ) != -1:
                    self.notice ( privmsg [1] [0] [0], '\001VERSION The Lurk Internet Relay Chat Library : Alpha 1\001' )
                elif privmsg [1] [2].find ( 'SOURCE' ) != -1:
                    self.notice ( privmsg [1] [0] [0], '\001SOURCE irc.codeshock.org/6697:SSL -> #lurklib\001' )
                return 'CTCP', ( privmsg [1] [0], privmsg [1] [2] )
            else: return privmsg
        elif segments [1] == 'NOTICE':
            return 'NOTICE', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )

        elif segments [1] == 'MODE':
            try: return 'MODE', ( who ( segments [2] ), ' '.join ( segments [3:] ) )
            except IndexError: return 'MODE', ( segments [2], ' '.join ( segments [3:] ) [1:] )
        
        elif segments [1] == 'KICK':
            return 'KICK', ( who ( segments [0] [1:] ), segments [2], segments [3], ' '.join ( segments [4:] ) [1:] )

        elif segments [1] == 'INVITE':
            return 'INVITE', ( who ( segments [0] [1:] ), segments [2], segments [3] [1:] )

        elif segments [1] == 'NICK':
            return 'NICK', ( who ( segments [0] [1:] ), ' '.join ( segments [2:] ) )

        elif segments [1] == 'TOPIC':
            return 'TOPIC', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )

        elif segments [1] == 'QUIT':
            return 'QUIT', ( who ( segments [0] [1:] ), ' '.join ( segments [2:] [1:] ) )
        
        elif segments [1] == '396':
            return 'VHOST', segments [3]
       
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
        
        elif segments [1] == '301':
            return ( 'AWAY', data.split ( None, 3 ) [3] [1:] )
        
        elif segments [1] in self.err_replies.keys():
            self.exception ( segments [1] )
        
        else: return 'UNKNOWN', data

    def auto ( self, function, args = (), delay = 0.2 ):
        
        auto_timer = self.threading.Timer ( delay, function, args )
        auto_timer.start()
        
    def mainloop ( self ):
        while 1:
            event = self.stream()
            if event [0] in self.hooks.keys():
                self.hooks [ event [0] ] ( event = event [1] )
            elif 'UNHANDLED' in self.hooks.keys():
                self.hooks [ 'UNHANDLED' ] ( event )
            else: raise self.UnhandledEvent ('Unhandled Event')
    def set_hook ( self, trigger, method ):
        self.hooks [ trigger ] = method
    
    def remove_hook ( self, trigger ):
        del self.hooks [ trigger ]