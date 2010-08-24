def who ( self, channel ):
    '''
    who() runs a WHO on the specified channel
    It returns a dictionary, each key is the nick, and each entry contains a list;
    [0] == ident
    [1] == name
    [3] == host

    '''
    self.rsend ( 'WHO ' + channel )
    who_lst = {}
    
    while self.readable():
        data = self.recv()
        ncode = data.split() [1]

        if ncode == '352':
            raw_who = data.split ( None, 10 )
            who_lst [ raw_who [7] ] = ( raw_who [4], raw_who [10], raw_who [5] )
        elif ncode in self.err_replies.keys():
            self.exception ( ncode )
        elif ncode == '315': return who_lst
        else: self.buffer.append ( data )

def whois ( self, nick ):
    '''
    Returns a dictionary;
    IDENT == The user's ident.
    HOST == The user's host.
    NAME == The user's real name.
    SERVER == The server the user is on.
    SERVER_INFO == The name of the server the user is on.
    CHANNELS == A list of channels the user is on.
    IDLE == The user's idle time.
    AWAY, present if the user is away, returns a string containing their away message.
    OP == Present if the user is an IRC operator.
    ETC == Other data sent in response to the WHOIS query.
    '''
    
    self.rsend ( 'WHOIS ' + nick )
    whois_r = {}

    while self.readable():
        data = self.recv()
        info = data.split ( None, 7 )
        ncode = info [1]
        if ncode == '311':
            whois_r = \
                    {
                        'IDENT' : info [4],
                        'HOST' : info [5],
                        'NAME' : info [7] [1:]
                    }
        elif ncode == '312':
            whois_r [ 'SERVER' ] = info [4]
            whois_r [ 'SERVER_INFO' ] = ' '.join ( info [5:] ) [1:]
        elif ncode == '319':
            whois_r [ 'CHANNELS' ] = tuple ( ' '.join ( info [4:] )[1:].split() )
        elif ncode == '317':
            whois_r [ 'IDLE' ] = info [5]
        elif ncode == '301':
            whois_r [ 'AWAY' ] = info [4] [1:]
        elif ncode == '313':
            whois_r [ 'OP' ] = ' '.join ( info [4:] ) [1:]
        elif ncode in self.err_replies.keys(): self.exception ( ncode )
        elif ncode == '318': break
        else:
            if 'ETC' in whois_r.keys():
                whois_r [ 'ETC' ].append ( data.split ( ':', 2 ) [2] )
            else:
                whois_r [ 'ETC' ] = [ data.split ( ':', 2 ) [2] ]

    return whois_r
def whowas ( self, nick ): 
    '''
    Returns a list;
    [0] The user's nick.
    [1] The user's ident.
    [2] The user's host.
    [3] The user's real name.
    '''
    
    self.rsend ( 'WHOWAS ' + nick )
    
    rwhowas = []
    while self.readable():
            data = self.recv()
            ncode = data.split() [1]

            if ncode == '314':
                raw_whowas = data.split()
                rwhowas = ( raw_whowas [3], raw_whowas [4], raw_whowas [5], raw_whowas [7] [1:] )
            elif ncode in self.err_replies.keys():
                self.exception ( ncode )
            elif ncode == '312': pass
            elif ncode == '369': return rwhowas
            else: self.buffer.append ( data )
