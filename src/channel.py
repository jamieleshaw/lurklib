def join ( self, channel, key = None ):
       
        topic = ''
        names = ()
        set_by = ''
        time_set = ''
        
        for x in self.channels:
            if x.lower() == channel:
                raise self.AlreadyInChannel ( 'Already in ' + channel + '.' )
        
        if key != None:
            self.rsend ( 'JOIN ' + channel + ' ' + key )
        else:
            self.rsend ( 'JOIN ' + channel )
        
        while self.readable():
                data = self.recv()
                ncode = data.split() [1]

                if ncode ==  '332':
                    topic = data.split ( None, 4 ) [4] [1:]
                elif ncode == '333':
                    segments = data.split()
                    time_set = self.time.localtime ( int ( segments [5] ) )
                    set_by = self.who_is_it ( segments [4] )
                    
                elif ncode ==  '353':
                    names = data.split() [5:]
                    names [0] = names [0] [1:]
                    names = tuple ( names )
                elif self.find ( data, 'JOIN' ):
                    self.channels.append ( data.split() [2] [1:] )
                    if self.hide_called_events == False: self.buffer.append ( data )
                elif ncode in self.err_replies.keys(): self.exception ( ncode )
                elif ncode == '366': break
                else: self.buffer.append ( data )

        return ( names, topic, set_by, time_set )

def part ( self, channel, reason = None ):

        if reason == None:
                self.rsend ( 'PART ' + channel )
        else:
                self.rsend ( 'PART ' + channel + ' :' + reason )
        
        channels = []
        for x in self.channels: channels.append ( x.lower() )
        if channel.lower() not in channels:
                raise self.NotInChannel ( 'Not in ' + channel + '.' )
        
        if self.readable():
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                self.exception ( ncode )
            elif self.find ( data, 'PART' ):
                self.channels.remove ( data.split() [2] )
                if self.hide_called_events == False: self.buffer.append ( data )
            else: self.buffer.append ( data )

def cmode ( self, channel, modes = '' ):

        if modes == '':
                self.rsend ( 'MODE ' + channel )
                if self.readable(): return self.recv().split() [4]
        else:   self.rsend ( 'MODE ' + channel + ' ' + modes )
        
        if self.readable():
            data = self.recv()
            ncode = data.split() [1]
    
            if ncode in self.err_replies.keys():
                self.exception ( ncode )
            elif self.find ( data, 'MODE' ) and self.hide_called_events:
                pass
            else: self.buffer.append ( data )
            
def banlist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +b' )
        bans = []

        while self.readable():
            
            data = self.recv()
            ncode = data.split() [1]

            if ncode in self.err_replies.keys():
                self.exception ( ncode )
            elif ncode == '367':
                bans.append ( data.split() [4] )
            elif ncode == '368': break
            else: self.buffer.append ( data )
        return tuple ( bans )
def exceptlist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +e' )
        excepts = []

        while self.readable():
            data = self.recv()
            ncode = data.split() [1]

            if ncode in self.err_replies.keys():
                self.exception ( ncode )
            elif ncode == '348':
                excepts.append ( data.split() [4] )
            elif ncode == '349': break
            else: self.buffer.append ( data )

        return tuple ( excepts )
def invitelist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +i' )
        invites = []

        while self.readable():
            data = self.recv()
            ncode = data.split() [1]

            if ncode in self.err_replies.keys():
                self.exception ( ncode )
            elif ncode == '346':
                invites.append ( data.split() [4] )
            elif ncode == '347': break
            else: self.buffer.append ( data )

        return tuple ( invites )
def topic ( self, channel, rtopic = None ):

        if rtopic != None:
            self.rsend ( 'TOPIC ' + channel + ' :' + rtopic )
        else:
            self.rsend ( 'TOPIC ' + channel )
        topic = ''
        set_by = ''
        time_set = ''
        while self.readable():
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                self.exception ( ncode )
            elif ncode == '332':
                topic = data.split ( None, 4 ) [4] [1:]
                self.recv()
            elif self.find ( data, 'TOPIC' ) and self.hide_called_events:
                pass
            elif ncode == '333':
                segments = data.split()
                time_set = self.time.ctime ( int ( segments [5] ) )
                set_by = self.who_is_it ( segments [4] )
            elif ncode == '331': topic = ''
            else: self.buffer.append ( data )
        return topic, set_by, time_set
def names ( self, channel ):
        self.rsend ( 'NAMES ' + channel )
        names = ()

        while self.readable():
            data = self.recv()
            ncode = data.split() [1]

            if ncode == '353':
                names = data.split() [5:]
                names [0] = names [0] [1:]
            elif ncode in self.err_replies.keys():
                self.exception ( ncode )
            elif ncode == '366': break
            else: self.buffer.append ( data )

        return tuple ( names )
def slist ( self ):
  
        self.rsend ( 'LIST' )
        list_info = { }

        while self.readable():
            data = self.recv()
            ncode = data.split() [1]

            if ncode == '322':
                raw_lst = data.split ( None, 5 )
                list_info [ raw_lst [3] ] = ( raw_lst [4], raw_lst [5] [1:] )
            elif ncode == '321':
                pass
            elif ncode in self.err_replies.keys():
                self.exception ( ncode )
            elif ncode == '323': break
            else: self.buffer.append ( data )
        return list_info
def invite ( self, channel, nick ):
        self.rsend ( 'INVITE ' + nick + ' ' + channel )

        while self.readable():
                data = self.recv()
                ncode = data.split() [1]

                if ncode in self.err_replies.keys():
                    self.exception ( ncode )
                elif ncode == '341':
                    pass
                elif ncode == '301':
                    return 'AWAY'
                elif self.find ( data, 'INVITE' ) and self.hide_called_events:
                    pass
                else: self.buffer.append ( data )

def kick ( self, channel, nick, reason = '' ):
        self.rsend ( 'KICK ' + channel + ' ' + nick + ' :' + reason )
        
        channels = []
        for x in self.channels: channels.append ( x.lower() )
        if channel.lower() not in channels:
                raise self.NotInChannel ( 'Not in ' + channel + '.' )
        
        if self.readable():
            data = self.recv()
            ncode = data.split() [1]
    
            if ncode in self.err_replies.keys():
                    self.exception ( ncode )
            elif self.find ( data, 'KICK' ) and self.hide_called_events:
                    pass
            else: self.buffer.append ( data )