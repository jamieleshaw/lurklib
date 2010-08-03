# lurklib functions work as follows; all data recvieved in relation to a;
# called function should be proccessed by the function itself, before return;
# control to the outside codosphere, this is good because, it means a lurklib;
# function can be called directly after another without;
# having to call stream(), which in the long run is alot cleaner, and simpler; however always call stream() after connecting.
#
# TODO;
# Doc Strings
# Fix connection system - join the broken motd parts
# stream() should handle returns things like the topic and /names upon sajoin
# make it so the irc connection can be init'ed via __init__
# change stream()'s return value thingy, so it returns a set or w/e
# Hooks based event handling
# Add a Debug mode system thingy

# Make code look shiny e.g. fix spacing and such
# sending.py - Completed
# channel.py - Completed except where noted
# connection.py - Completed
# uqueries.py - Completed
# Maybe/Idea: Convert all while 1's to for x in range() for safety/stabilty.
import socket, sys, re
sys.path.append ( './lurklib' )
# Import IRC Sub-Modules

import connection
import channel
import uqueries
import squeries
import sending

class irc:
    '''
    LK's IRC Class.
    '''
    # Put them in this namespace...I'm sure there is a cleaner way of doing this, but I've haven't found it yet...
    for x in dir ( connection ): exec ( x + ' = connection.' + x )
    for x in dir ( channel ): exec ( x + ' = channel.' + x )
    for x in dir ( uqueries ): exec ( x + ' = uqueries.' + x )
    for x in dir ( squeries ): exec ( x + ' = squeries.' + x )
    for x in dir ( sending ) : exec ( x + ' = sending.' + x )

    def __init__ ( self, encoding = 'utf-8', clrf = '\r\n' ):
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
        self.network = ''
        self.buffer = [ ]
        self.s = socket.socket()
        self.fallback_encoding = encoding
        self.encoding = encoding
        self.motd = []

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
        try: data = bytes ( msg + self.clrf, self.encoding )
        except LookupError: data = bytes ( msg + self.clrf, self.fallback_encoding )
        self.s.send ( data )
        return msg
    def mcon ( self ):
        sdata = self.s.recv ( 4096 )
        try: sdata = sdata.decode ( self.encoding )
        except LookupError: sdata = sdata.decode ( self.fallback_encoding )

        lines = sdata.split ( self.clrf )
        for x in lines:
            if x.find ( 'PING :' ) == 0:
                self.rsend ( 'PONG ' + x.split() [1] )
                self.mcon()
            elif x == '':
                break
            else: self.buffer.append ( x )
    def recv ( self ):
        msg = ''
        if self.index == len ( self.buffer ): self.mcon()
        elif len ( self.buffer ) >= 50:
            self.index, self.buffer = 0, []
            self.mcon()
        msg = self.buffer [ self.index ]
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
                return [ nick, ident, host ]
            except IndexError: return who
        data = self.recv()
        segments = data.split()
        
        if segments [1] == 'JOIN':
            return { 'JOIN' : [ who ( segments [0] [1:] ), segments [2] [1:] ] }

        elif segments [1] == 'PART':
            try: return { 'PART' : [ who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] ] }
            except IndexError: return { 'PART' : [ who ( segments [0] [1:] ), segments [2], '' ] }

        elif segments [1] == 'PRIVMSG':
            return { 'PRIVMSG' : [ who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] ] }

        elif segments [1] == 'NOTICE':
            return { 'NOTICE' : [ who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] ] }

        elif segments [1] == 'MODE':
            try: return { 'MODE' : [ who ( segments [2] ), segments [2], ' '.join ( segments [3:] ) [1:] ] }
            except IndexError: return { 'MODE' : [ segments [2], ' '.join ( segments [3:] ) [1:] ] }
        
        elif segments [1] == 'KICK':
            return { 'KICK' : [ who ( segments [0] [1:] ), segments [2], segments [3], ' '.join ( segments [4:] ) [1:] ] }

        elif segments [1] == 'INVITE':
            return { 'INVITE' : [ who ( segments [0] [1:] ), segments [2], segments [3] [1:] ] }

        elif segments [1] == 'NICK':
            return { 'NICK' : [ who ( segments [0] [1:] ), ' '.join ( segments [2:] ) [1:] ] }

        elif segments [1] == 'TOPIC':
            return { 'TOPIC' : [ who ( segments [0] [1:] ), segments [2], ' '.join ( segments [3:] ) [1:] ] }

        elif segments [1] == 'QUIT':
            return { 'QUIT' : [ who ( segments [0] [1:] ), ' '.join ( segments [3:] ) ] }
        
        else: return data
        
    def test ( self ):
        '''
        test() may be removed at some point, it tests the irc class on a localhost ircd.
        '''
        self.init ( 'localhost', 6667, 'LurkTest123', 'lurklib', 'lurklib' )
        print ( 'Connected' )
        #print ( self.con_msg )
        for x in self.buffer: print ( x )
        while 1:
            try: print ( self.recv() )
            except KeyboardInterrupt:
                self.disconnect()
                break
