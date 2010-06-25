def join ( self, channel, key = None ):
        '''
        join() joins the specified channel, optionally a channel key may be specified.
        join() returns a list [0] is the channel topic and [1] is a list containing all nicks in the channel.
        '''
        topic = ''
        names = []
        if key != None:
            self.rsend ( 'JOIN ' + channel + ' ' + key )
        else:
            self.rsend ( 'JOIN ' + channel )
        data = self.recv()
        while data.find ( '366' ) == -1:
                data = self.recv()
                segs = data.split()
                if data.find ( '332' ) != -1:
                     topic = data.split( ' ', 4) [4] [1:]
                elif data.find ( '353' ) != -1:
                        names = data.split( ' ', 5 ) [5]
                        names = names [0] [1:] + names [1:]
                        names = names.split()
                elif segs [1] != '332' and segs [1] != '353' and segs[1] != 366:
                        self.code = int ( data.split() [1] )
                        return False
        return [ topic, names ]
def part ( self, channel, reason = None ):
    '''
    part() part's a channel, optionally a part message may be specified.
    '''
    if reason == None:
        self.rsend ( 'PART ' + channel )
    else:
        self.rsend ( 'PART ' + channel + ' :' + reason )
    if data.find ( 'PART' ) == -1:
            self.code = int ( data.split() [1] )
            return False
def cmode ( self, channel, modes = '' ):
        '''
        cmode() sets channel modes, it accepts two arguments, the channel, and the modes to set.
        '''
        if modes == '':
                self.rsend ( 'MODE ' + channel )
                return self.recv().split() [4]
        else:   self.rsend ( 'MODE ' + channel + ' ' + modes )
        data = self.recv()
        if data.find ( 'MODE' ) == -1:
                self.code = int ( data.split() [1] )
                return False
        self.buffer.append ( data )
        
def banlist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +b' )
        data = self.recv()
        bans = []
        while data.find ( '368' ) == -1:
                rban = data.split()
                if rban [1] != '367':
                        self.code = int ( rban [1] )
                        return False
                bans.append ( rban [4] )

def exceptlist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +e' )
        data = self.recv()
        excepts = []
        while data.find ( '349' ) == -1:
                rexcept = data.split()
                if rexcept [1] != '348':
                        self.code = int ( rexcept [1] )
                        return False
                excepts.append ( rexcept [4] )
def invitelist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +i' )
        data = self.recv()
        invites = []
        while data.find ( '347' ) == -1:
                rinvites = data.split()
                if rinvites [1] != '346':
                        self.code = int ( rinvites [1] )
                        return False
                rinvites.append ( rinvites [4] )

def topic ( self, channel, rtopic = None ):
        '''
        topic(), accepts 2 arguments, channel is required, and rtopic can optionally be specified, if you want to change the topic of the given channel;
        returns the topic
        '''
        if rtopic != None:
            self.rsend ( 'TOPIC ' + channel + ' :' + rtopic )
        else:
            self.rsend ( 'TOPIC ' + channel )
        topic = ''
        data = self.recv()
        while data.find ( '333' ) == -1:
                data = self.recv()
                if data.find ( '332' ) != -1:
                        topic = data.split( ' ', 4 ) [4] [1:]
                else:
                        self.code = int ( data.split() [1] )
                        return False
        return topic
def names ( self, channel ):
        '''
        names(), accepts one argument the name of the channel to list the nicks in, it returns a list of the nicks in the specified channel;
        if there are no nicks or the channel doesn't exist, it returns a empty list.
        '''
        self.rsend ( 'NAMES ' + channel )
        names = []
        data = self.recv()
        while data.find ( '366' ) == -1:
                data = self.recv()
                if data.find ( '353' ) != -1:
                        names = data.split( ' ', 5 ) [5]
                        names = names [0] [1:] + names [1:]
                        names = names.split()
                else:
                        self.code = int ( data.split() [1] )
                        return False
        return names
def slist ( self ):
        '''
        slist(), Runs a LIST on the server.;
        '''
        self.rsend ( 'LIST' )
        list_info = { }
        data = self.recv()
        while data.find ( '323' ) == -1:
                data = self.recv()
                if data.find ( '322' ) != -1:
                        p = data.split ( ' ', 6 )
                        channel = p [3]
                        count = p [4]
                        modes = p [5] [3:]
                        modes = modes [:-1]
                        topic = p [6]
                        list_info [ channel ] = [ count, modes, topic ]
                else:
                        self.code = int ( data.split() [1] )
                        return False
        return list_info
def invite ( self, channel, nick ):
    self.rsend ( 'INVITE ' + nick + ' ' + channel )
    data = self.recv()
    if data.find ( '341' ) == -1:
            self.code = int ( data.split() [1] )
            return False
def kick ( self, channel, nick, reason = '' ):
    self.rsend ( 'KICK ' + channel + ' ' + nick + ' :' + reason )
    data = self.recv()
    if data.find ( 'KICK' ) == -1:
            self.code = int ( data.split() [1] )
            return False
