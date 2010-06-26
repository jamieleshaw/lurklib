def join ( self, channel, key = None ):
        '''
        join() joins the specified channel, optionally a channel key may be specified.
        join() returns a list [0] is the channel topic and [1] is a list containing all nicks in the channel.
        '''
        replies = {
                461 : 'ERR_NEEDMOREPARAMS',
                473 : 'ERR_INVITEONLYCHAN',
                471 : 'ERR_CHANNELISFULL',
                403 : 'ERR_NOSUCHCHANNEL',
                407 : 'ERR_TOOMANYTARGETS',
                332 : 'RPL_TOPIC',
                474 : 'ERR_BANNEDFROMCHAN',
                475 : 'ERR_BADCHANNELKEY',
                476 : 'ERR_BADCHANMASK',
                405 : 'TOOMANYCHANNELS',
                437 : 'ERR_UNAVAILRESOURCE'
                }
                
        topic = ''
        names = []
        if key != None:
            self.rsend ( 'JOIN ' + channel + ' ' + key )
        else:
            self.rsend ( 'JOIN ' + channel )
def part ( self, channel, reason = None ):
    '''
    part() part's a channel, optionally a part message may be specified.
    '''
    replies = {
            461 : 'ERR_NEEDMOREPARAMS',
            442 : 'ERR_NOTONCHANNEL',
            403 : 'ERR_NOSUCHCHANNEL'
            }
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
        replies = {
                461 : 'ERR_NEEDMOREPARAMS',
                477 : 'ERR_NOCHANMODES',
                441 : 'ERR_USERNOTINCHANNEL',
                324 : 'RPL_CHANNELMODEIS',
                367 : 'RPL_BANLIST',
                348 : 'RPL_EXCEPTLIST',
                346 : 'RPL_INVITELIST',
                325 : 'RPL_UNIQOPIS',
                467 : 'ERR_KEYSET',
                482 : 'ERR_CHANOPRIVSNEEDED',
                472 : 'ERR_UNKNOWNMODE',
                368 : 'RPL_ENDOFBANLIST',
                349 : 'RPL_ENDOFEXCEPTLIST',
                347 : 'RPL_ENDOFINVITELIST'
                }
        if modes == '':
                self.rsend ( 'MODE ' + channel )
                return self.recv().split() [4]
        else:   self.rsend ( 'MODE ' + channel + ' ' + modes )

        
def banlist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +b' )
        bans = []
 
def exceptlist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +e' )
        excepts = []
 
def invitelist ( self, channel ):
        self.rsend ( 'MODE ' + channel + ' +i' )
        invites = []

def topic ( self, channel, rtopic = None ):
        '''
        topic(), accepts 2 arguments, channel is required, and rtopic can optionally be specified, if you want to change the topic of the given channel;
        returns the topic
        '''
        replies = {
                461 : 'ERR_NEEDMOREPARAMS',
                331 : 'RPL_NOTOPIC',
                482 : 'ERR_CHANOPRIVSNEEDED',
                442 : 'ERR_NOTONCHANNEL',
                332 : 'RPL_TOPIC',
                477 : 'ERR_NOCHANMODES'
                }
        if rtopic != None:
            self.rsend ( 'TOPIC ' + channel + ' :' + rtopic )
        else:
            self.rsend ( 'TOPIC ' + channel )
        topic = ''

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
