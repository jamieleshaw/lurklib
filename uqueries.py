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
    data = self.recv()
    while data.find ( '315' ) == -1:
            if data.find ( '352' ) != -1:
                raw_who = data.split ( None, 10 )
                who_lst [ raw_who [7] ] = [ raw_who [4], raw_who [10], raw_who [5] ]
            data = self.recv()
    return who_lst
def whois ( self, nick ):
        '''
        whois() accepts, one parameter, a Nickname, it runs a whois on the User.
        '''
        err_replies = {
            '431' : 'ERR_NONICKNAMEGIVEN',
            '401' : 'ERR_NOSUCHNICK' }
        self.rsend ( 'WHOIS ' + nick )
        whois_r = { 'ETC': [] }
        data = self.recv()
        while data.find ( '318' ) == -1:
            info = data.split ( None, 7 )
            if data.find ( '311' ) != -1:
                whois_r = \
                        {
                            'IDENT' : info [4],
                            'HOST' : info [5],
                            'NAME' : info [7] [1:]
                        }
            elif data.find ( '312' ) != -1:
                whois_r [ 'SERVER' ] = info [4]
                whois_r [ 'SERVER_INFO' ] = ' '.join ( info [5:] ) [1:]
            elif data.find ( '319' ) != -1:
                whois_r [ 'CHANNELS' ] = ''.join ( info [4:] )[1:].split()
            elif data.find ( '317' ) != -1:
                whois_r [ 'IDLE' ] = info [5]
            elif data.find ( '301' ) != -1:
                whois_r [ 'AFK' ] = info [4] [1:]
            elif data.find ( '313' ) != -1:
                whois_r [ 'OP' ] = True
            elif data.split() [1] in err_replies.keys(): return [ False, data.split() [1] ]
            else: whois_r [ 'ETC' ].append ( data )
            data = self.recv()
        return whois_r
def whowas ( self, nick ):
    self.rsend ( 'WHOWAS ' + nick )
