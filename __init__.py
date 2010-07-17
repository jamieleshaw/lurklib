# TODO;
# Implement Sub-Modules, accoriding to RFC,
# Impove/implement return collections
# Do not call one irc lib directly after another, well it stuffs it up a little.
import socket, sys
sys.path.append ( './irc' )
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
    
    def __init__ ( self ):
        '''
        Initial Class Variables.
        '''
        self.index = 0
        self.buffer = [ ]
        self.s = socket.socket()
        self.encoding = 'ascii'

    def rsend ( self, msg ):
        '''
        rsend() provides, a raw interface to the socket allowing the sending of raw data.
        '''
        self.s.send ( bytes ( msg + '\r\n', self.encoding ) )    
    
    def mcon ( self ):
        sdata = self.s.recv ( 4096 ).decode ( self.encoding )
        lines = sdata.split ( '\r\n' )
        for x in lines:
            if x.find ( 'PING' ) != -1: self.rsend ( 'PONG ' + x.split() [1] )
            if x != '': self.buffer.append ( x )
    def recv ( self ):
        msg = ''
        if self.index == len ( self.buffer ): self.mcon()
        if len ( self.buffer ) >= 100:
            self.index, self.buffer = 0, []
            self.mcon()
        if self.buffer [ self.index ] != '': msg =  self.buffer [ self.index ]
        self.index += 1
        return msg
    def pdata ( self ):
        '''
        pdata() is the overall receival function, it can return anything, it calls other functions, to PING/PONG and update the buffer etc.
        it proccess, incoming socket data.
        '''
    def test ( self ):
        '''
        test() may be removed at some point, it tests the irc class on a localhost ircd.
        '''
        self.init ( 'localhost', 6667, 'test', 'testident', 'Mr. Name' )
        done = 0
        while 1:
            if done == 5:
                #print ( self.join ( '#teast' ) )
                pass
            if done == 7:
                print ( self.links (  ) )
            print ( self.recv() )
            done += 1
