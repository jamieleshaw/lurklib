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

    def __init__ ( self, server = None, port = None, nick = 'lurklib', ident = 'lurklib', real_name = 'The Lurk Internet Relay Chat Library', passwd = None, end_code = '266', ssl_on = False, encoding = 'utf-8', clrf = '\r\n' ):
        '''
        Initial Class Variables.
        '''
        self.index = 0
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

        self.err_replies = { \
            '407' : 'ERR_TOOMANYTARGETS',
            '402' : 'ERR_NOSUCHSERVER',
##            'ERR_TOOMANYMATCHES' : 'ERR_TOOMANYMATCHES',
            '476' : 'ERR_BADCHANMASK',
            '474' : 'ERR_BANNEDFROMCHAN',
            '443' : 'ERR_USERONCHANNEL',
            '442' : 'ERR_NOTONCHANNEL',
            '441' : 'ERR_USERNOTINCHANNEL',
            '461' : 'ERR_NEEDMOREPARAMS',
            '472' : 'ERR_UNKNOWNMODE',
            '473' : 'ERR_INVITEONLYCHAN',
            '405' : 'ERR_TOOMANYCHANNELS',
            '471' : 'ERR_CHANNELISFULL',
            '403' : 'ERR_NOSUCHCHANNEL',
            '477' : 'ERR_NOCHANMODES',
            '401' : 'ERR_NOSUCHNICK',
            '475' : 'ERR_BADCHANNELKEY',
            '437' : 'ERR_UNAVAILRESOURCE',
            '467' : 'ERR_KEYSET',
            '482' : 'ERR_CHANOPRIVSNEEDED',
            '431' : 'ERR_NONICKNAMEGIVEN',
            '433' : 'ERR_NICKNAMEINUSE',
            '432' : 'ERR_ERRONEUSNICKNAME',
            '436' : 'ERR_NICKCOLLISION',
            '484' : 'ERR_RESTRICTED',
            '462' : 'ERR_ALREADYREGISTRED',
            '411' : 'ERR_NORECIPIENT',
            '404' : 'ERR_CANNOTSENDTOCHAN',
            '414' : 'ERR_WILDTOPLEVEL',
            '412' : 'ERR_NOTEXTTOSEND',
            '413' : 'ERR_NOTOPLEVEL',
            '491' : 'ERR_NOOPERHOST',
            '464' : 'ERR_PASSWDMISMATCH',
            '501' : 'ERR_UMODEUNKNOWNFLAG',
            '502' : 'ERR_USERSDONTMATCH',
            '481' : 'ERR_NOPRIVILEGES' }
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

        msg = self.buffer [ self.index ]
        while self.find ( msg, 'PING :' ):
            self.index += 1
            try:
                msg = self.buffer [ self.index ]
            except IndexError:
                self.mcon()
        self.index += 1
        return msg
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
                print ( 'AAA' )
                return [ nick, ident, host ]
            except IndexError: return who
        segments = self.recv().split()
        
        if segments [1] == 'JOIN':
            return ( 'JOIN', ( who ( segments [0] [1:] ), segments [2] [1:] ) )

        elif segments [1] == 'PART':
            try: return ( 'PART', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] ) )
            except IndexError: return { 'PART' : [ who ( segments [0] [1:] ), segments [2], '' ] }

        elif segments [1] == 'PRIVMSG':
            return ( 'PRIVMSG', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] ) )
        
        elif segments [1] == 'NOTICE':
            return ( 'NOTICE', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] ) )

        elif segments [1] == 'MODE':
            try: return ( 'MODE', ( who ( segments [2] ), segments [2], ' '.join ( segments [3:] ) [1:] ) )
            except IndexError: return { 'MODE' : [ segments [2], ' '.join ( segments [3:] ) [1:] ] }
        
        elif segments [1] == 'KICK':
            return ( 'KICK', ( who ( segments [0] [1:] ), segments [2], segments [3], ' '.join ( segments [4:] ) [1:] ) )

        elif segments [1] == 'INVITE':
            return ( 'INVITE', ( who ( segments [0] [1:] ), segments [2], segments [3] [1:] ) )

        elif segments [1] == 'NICK':
            return ( 'NICK', ( who ( segments [0] [1:] ), ' '.join ( segments [2:] ) [1:] ) )

        elif segments [1] == 'TOPIC':
            return ( 'TOPIC', ( who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] ) )

        elif segments [1] == 'QUIT':
            return ( 'QUIT', ( who ( segments [0] [1:] ), ' '.join ( segments [3:] ) ) )
        
        else: return data