# TODO;
# Implement Sub-Modules, accoriding to RFC,
import socket, sys, threading
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

    def __init__ ( self, encoding = 'utf-8', init_junk_count = 0 ):
        '''
        Initial Class Variables.
        '''
        self.index = 0
        self.con_msg = []
        self.ircd = ''
        self.umodes = ''
        self.cmodes = ''
        self.server = ''
        self.network = ''
        self.buffer = [ ]
        self.s = socket.socket()
        self.encoding = encoding
        self.init_junk_count = init_junk_count
        self.motd = []

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
        if self.find ( msg, 'PING' ) == True: msg = self.recv()
        return msg
    def pdata ( self ):
        '''
        pdata() is the overall receival function, it can return anything, it calls other functions, to PING/PONG and update the buffer etc.
        it proccess, incoming socket data.
        '''
        return self.recv()
    def test ( self ):
        '''
        test() may be removed at some point, it tests the irc class on a localhost ircd.
        '''
        self.init ( 'localhost', 6667, 'test', 'testident', 'Mr. Name' )
        print ( 'Connected' )
        print ( self.network )
        while 1:
            print ( self.recv() )


