import socket, sys, ssl
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


    def __init__ ( self, server = None, port = None, nick = 'lurklib', ident = 'lurklib', real_name = 'The Lurk Internet Relay Chat Library', passwd = None, end_code = '266', ssl_on = False, encoding = 'utf-8', clrf = '\r\n', hooks = {} ):
        '''
        Initial Class Variables.
        '''
        self.index = 0
        self.hooks = hooks
        self.con_msg = []
        self.ircd = ''
        self.clrf = clrf
        self.umodes = ''
        self.cmodes = ''
        self.server = ''
        self.ssl_on = ssl_on
        self.ssl = ssl
        self.buffer = [ ]
        self.s = socket.socket()
        self.fallback_encoding = encoding
        self.encoding = encoding
        self.motd = []
        self.info = {}
        
        self.NOPRIVILEGES = Exception
        self.NOSUCHNICK = Exception
        self.USERONCHANNEL = Exception
        self.NOTONCHANNEL = Exception
        self.USERNOTINCHANNEL = Exception
        self.WILDTOPLEVEL = Exception
        self.NEEDMOREPARAMS = Exception
        self.ALREADYREGISTRED = Exception
        self.NICKCOLLISION = Exception
        self.UNAVAILRESOURCE = Exception
        self.UMODEUNKNOWNFLAG = Exception
        self.NOTOPLEVEL = Exception
        self.RESTRICTED = Exception
        self.CHANOPRIVSNEEDED = Exception
        self.USERSDONTMATCH = Exception
        self.NORECIPIENT = Exception
        self.UNKNOWNMODE = Exception
        self.NOOPERHOST = Exception
        self.NOTEXTTOSEND = Exception
        self.CANNOTSENDTOCHAN = Exception
        self.NICKNAMEINUSE = Exception
        self.TOOMANYTARGETS = Exception
        self.INVITEONLYCHAN = Exception
        self.TOOMANYCHANNELS = Exception
        self.CHANNELISFULL = Exception
        self.BADCHANMASK = Exception
        self.NOSUCHSERVER = Exception
        self.BANNEDFROMCHAN = Exception
        self.BADCHANNELKEY = Exception
        self.NOSUCHCHANNEL = Exception
        self.NONICKNAMEGIVEN = Exception
        self.ERRONEUSNICKNAME = Exception
        self.KEYSET = Exception
        self.PASSWDMISMATCH = Exception
        self.NOCHANMODES = Exception



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
            self.init ( server, port, nick, ident, real_name, passwd, end_code, ssl_on )
            
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
        exec ( 'raise self.' + self.err_replies [ ncode ] + ' ( "' + self.err_replies [ ncode ] + '" )' )
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
                self.rsend ( 'PONG ' + x.split() [1] )
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
            return 'JOIN', ( who ( segments [0] [1:] ), segments [2] [1:] )

        elif segments [1] == 'PART':
            try: return 'PART', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )
            except IndexError: return 'PART', ( who ( segments [0] [1:] ), segments [2], '' )

        elif segments [1] == 'PRIVMSG':
            return 'PRIVMSG', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )
        
        elif segments [1] == 'NOTICE':
            return 'NOTICE', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )

        elif segments [1] == 'MODE':
            try: return 'MODE', ( who ( segments [2] ), segments [2], ' '.join ( segments [3:] ) [1:] )
            except IndexError: return 'MODE', ( segments [2], ' '.join ( segments [3:] ) [1:] )
        
        elif segments [1] == 'KICK':
            return 'KICK', ( who ( segments [0] [1:] ), segments [2], segments [3], ' '.join ( segments [4:] ) [1:] )

        elif segments [1] == 'INVITE':
            return 'INVITE', ( who ( segments [0] [1:] ), segments [2], segments [3] [1:] )

        elif segments [1] == 'NICK':
            return 'NICK', ( who ( segments [0] [1:] ), ' '.join ( segments [2:] ) [1:] )

        elif segments [1] == 'TOPIC':
            return 'TOPIC', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] )

        elif segments [1] == 'QUIT':
            return 'QUIT', ( who ( segments [0] [1:] ), ' '.join ( segments [3:] ) )
        
        else: return 'UNKNOWN', data
    def mainloop ( self ):
        while 1:
            event = self.stream()
            if event [0] in self.hooks.keys():
                self.hooks [ event [0] ] ( event = event [1:] )
            else: pass # raise Unhandled event