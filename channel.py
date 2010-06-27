def join ( self, channel, key = None ):
        '''
        join() joins the specified channel, optionally a channel key may be specified.
        join() returns a list [0] is the channel topic and [1] is a list containing all nicks in the channel.
        If it fails, to join the channel it will, [0] will be False, and [1] will be the error code.
        '''
        err_replies = {
                '461' : 'ERR_NEEDMOREPARAMS',
                '473' : 'ERR_INVITEONLYCHAN',
                '471' : 'ERR_CHANNELISFULL',
                '403' : 'ERR_NOSUCHCHANNEL',
                '407' : 'ERR_TOOMANYTARGETS',
                '474' : 'ERR_BANNEDFROMCHAN',
                '475' : 'ERR_BADCHANNELKEY',
                '476' : 'ERR_BADCHANMASK',
                '405' : 'ERR_TOOMANYCHANNELS',
                '437' : 'ERR_UNAVAILRESOURCE'
                }
                
        topic = ''
        names = []
        if key != None:
            self.rsend ( 'JOIN ' + channel + ' ' + key )
        else:
            self.rsend ( 'JOIN ' + channel )
        data = self.recv()
        while data.find ( '366' ) == -1:
                if data.find ( 'JOIN :' + channel ) != -1:
                        self.buffer.append ( data )
                elif data.find ( '332' ) != -1:
                        topic = data.split ( None, 4 ) [4] [1:]
                elif data.find ( '333' ) != -1:
                        # implement topic, setter and time set collection
                        pass
                elif data.find ( '353' ) != -1:
                        names = data.split() [5:]
                        names [0] = names [0] [1:]
                elif data.split() [1]in err_replies.keys(): return [ False, data.split() [1] ]
                data = self.recv()
        return [ topic, names ]
def part ( self, channel, reason = None ):
        '''
        part() part's a channel, optionally a part message may be specified.
        On success, True is returned, on failure, [0] is False and [1] is the error code.
        '''
        err_replies = {
            '461' : 'ERR_NEEDMOREPARAMS',
            '442' : 'ERR_NOTONCHANNEL',
            '403' : 'ERR_NOSUCHCHANNEL'
            }
        if reason == None:
                self.rsend ( 'PART ' + channel )
        else:
                self.rsend ( 'PART ' + channel + ' :' + reason )
        data = self.recv()
        while 1:
                if data.split() [1] in err_replies.keys() or data.find ( 'PART' ) != -1:
                        if data.split() [1] in err_replies.keys():
                                return [ False, data.split() [1] ]
                        elif data.find ( 'PART' ) != -1:
                                self.buffer.append ( data )
                        break
                data = self.recv()
        return True
def cmode ( self, channel, modes = '' ):
        '''
        cmode() sets channel modes, it accepts two arguments, the channel, and the modes to set.
        '''
        err_replies = {
                '461' : 'ERR_NEEDMOREPARAMS',
                '477' : 'ERR_NOCHANMODES',
                '441' : 'ERR_USERNOTINCHANNEL',
                '467' : 'ERR_KEYSET',
                '482' : 'ERR_CHANOPRIVSNEEDED',
                '472' : 'ERR_UNKNOWNMODE',
                }
        if modes == '':
                self.rsend ( 'MODE ' + channel )
                return self.recv().split() [4]
        else:   self.rsend ( 'MODE ' + channel + ' ' + modes )
        
        data = self.recv()
        while 1:
                if data.split() [1] in err_replies.keys() or data.find ( 'MODE' ) != -1:
                        if data.split() [1] in err_replies.keys():
                                return [ False, data.split() [1] ]
                        elif data.find ( 'MODE' ) != -1:
                                self.buffer.append ( data )
                        break
                data = self.recv()
        
def banlist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +b' )
        bans = []
        data = self.recv()
        while data.find ( '368' ) == -1:
                if data.find ( '367' ) != -1:
                        bans.append ( data.split() [4] )
                data = self.recv()
        return bans
def exceptlist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +e' )
        excepts = []
        data = self.recv()
        while data.find ( '349' ) == -1:
                if data.find ( '348' ) != -1:
                        excepts.append ( data.split() [4] )
                data = self.recv()
        return excepts
def invitelist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +i' )
        invites = []
        data = self.recv()
        while data.find ( '347' ) == -1:
                if data.find ( '346' ) != -1:
                        invites.append ( data.split() [4] )
                data = self.recv()
        return invites
def topic ( self, channel, rtopic = None ):
        '''
        topic(), accepts 2 arguments, channel is required, and rtopic can optionally be specified, if you want to change the topic of the given channel;
        returns the topic
        '''
        err_replies = {
                '461' : 'ERR_NEEDMOREPARAMS',
                '482' : 'ERR_CHANOPRIVSNEEDED',
                '442' : 'ERR_NOTONCHANNEL',
                '477' : 'ERR_NOCHANMODES'
                }
        if rtopic != None:
            self.rsend ( 'TOPIC ' + channel + ' :' + rtopic )
        else:
            self.rsend ( 'TOPIC ' + channel )
        topic = None
        while topic == None:
                data = self.recv()
                if data.split() [1] in err_replies.keys():
                        return [ False, data.split() [1] ]
                elif data.find ( 'TOPIC' ) != -1:
                        topic = ''
                        self.buffer.append ( data )
                elif data.find ( '332' ) != -1:
                        topic = data.split ( None, 4 ) [4] [1:]
                        self.recv()
                elif data.find ( '333' ) != -1:
                        # implement topic, setter and time set collection
                        pass
                elif data.find ( '331' ) != -1: topic = ''
        return topic
def names ( self, channel ):
        '''
        names(), accepts one argument the name of the channel to list the nicks in, it returns a list of the nicks in the specified channel;
        if there are no nicks or the channel doesn't exist, it returns a empty list.
        '''
        replies = {
                353 : 'RPL_NAMEREPLY',
                402 : 'ERR_NOSUCHSERVER',
                366 : 'REPL_ENDOFNAMES'
                }
        self.rsend ( 'NAMES ' + channel )
        names = []
  
def slist ( self ):
        '''
        slist(), Runs a LIST on the server.;
        '''
        replies = {
                321 : 'RPL_LISTSTART',
                322 : 'RPL_LIST',
                323 : 'RPL_LISTEND',
                402 : 'ERR_NOSUCHSERVER'
                }
        
        self.rsend ( 'LIST' )
        list_info = { }
def invite ( self, channel, nick ):
        replies = {
                461 : 'ERR_NEEDMOREPARAMS',
                442 : 'ERR_NOTONCHANNEL',
                341 : 'RPL_INVITING',
                401 : 'ERR_NOSUCHNICK',
                443 : 'ERR_USERONCHANNEL',
                301 : 'RPL_AWAY'
                }
        self.rsend ( 'INVITE ' + nick + ' ' + channel )
def kick ( self, channel, nick, reason = '' ):
        replies = {
                461 : 'ERR_NEEDMOREPARAMS',
                476 : 'ERR_BADCHANMASK',
                441 : 'ERR_USERNOTINCHANNEL',
                403 : 'ERR_NOSUCHCHANNEL',
                482 : 'ERR_CHANOPRIVSNEEDED',
                442 : 'ERR_NOTONCHANNEL'
                }
        self.rsend ( 'KICK ' + channel + ' ' + nick + ' :' + reason )
