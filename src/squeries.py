def get_motd ( self, server = None ):
    if server == None:
        self.rsend ( 'MOTD' )
    else:
        self.rsend ( 'MOTD ' + server )
        
    self.motd = []
    while self.readable():
        data = self.recv()
        ncode = data.split() [1]
        if ncode == '375':
            pass
        elif ncode == '372':
            self.motd.append ( data.split ( None, 3 ) [3] [1:] )
        elif ncode == '376':
            break
        elif ncode == '422':
            break
    self.motd = tuple ( self.motd )
    return self.motd
def get_lusers ( self, mask = None, target = None ):
    if mask == None:
        self.rsend ( 'LUSERS' )
    elif target == None and mask != None:
        self.rsend ( 'LUSERS ' + mask )
    else:
        self.rsend ( 'LUSERS ' + mask + ' ' + target )
    while self.readable():
        data = self.recv()
        segments = data.split()
        if segments [1] == '251':
            self.lusers [ 'USERS' ] = segments [5]
            self.lusers [ 'INVISIBLE' ] = segments [8]
            self.lusers [ 'SERVERS' ] = segments [11]
        
        elif segments [1] == '252':
            self.lusers [ 'OPERATORS' ] = segments [3]
        
        elif segments [1] == '254':
            self.lusers [ 'CHANNELS' ] = segments [3]
        
        elif segments [1] == '255':
            self.lusers [ 'CLIENTS' ] = segments [5]
            self.lusers [ 'LSERVERS' ] = segments [8]
        
        elif segments [1] == '265':
            self.lusers [ 'LOCALUSERS' ] = segments [6]
            self.lusers [ 'LOCALMAX' ] = segments [8]
        
        elif segments [1] == '266':
            self.lusers [ 'GLOBALUSERS' ] = segments [6]
            self.lusers [ 'GLOBALMAX' ] = segments [8]
            break
    return self.lusers

def version ( self, target = None ):
    if target == None:
        self.rsend ( 'VERSION' )
    else:
        self.rsend ( 'VERSION ' + target )

    while self.readable():
        data = self.recv()
        data = data.replace ( ' :are supported by this server', '' )
        segments = data.split()
        if segments [1] == '351':
            self.info [ 'VERSION' ] = ' '.join ( segments [3:] ) [1:]
        elif segments == '005':
            segments = segments [3:]
            for x in segments:
                    try:
                        x = x.split ( '=' )
                        name = x [0]
                        value = x [1]
                        self.info [ name ] = value
                
                        if name == 'CHARSET': self.encoding = value
                    except IndexError: 
                        self.info [ x [0] ] = True

    return self.info
def stats ( self, query = None, target = None ):
    if query == None:
        self.rsend ( 'STATS' )
    elif target == None and query != None:
        self.rsend ( 'STATS ' + query )
    else:
        self.rsend ( 'STATS ' + query + ' ' + target )

def links ( self, r_server = None, smask = None ):

    if r_server == None:
        self.rsend ( 'LINKS' )
    elif smask == None and r_server != None:
        self.rsend ( 'LINKS ' + r_server )
    else:
        self.rsend ( 'LINKS ' + r_server + ' ' + smask )   
    
def s_time ( self, target = None ):
    if target != None:
        self.rsend ( 'TIME ' + target )
    else:
        self.rsend ( 'TIME' )
    
    data = self.recv().split()
    time = ' '.join ( data [4:] ) [1:]
    return time

def s_connect ( self, tserver, tport, r_server = None ):
    if r_server == None:
        self.rsend ( 'CONNECT ' + tserver + ' ' + tport )
    else:
        self.rsend ( 'CONNECT ' + tserver + ' ' + tport + r_server )

def trace ( self, target ):
    self.rsend ( 'TRACE ' + target )

def admin ( self, target = None ):
    if target == None:
        self.rsend ( 'ADMIN' )
    else:
        self.rsend ( 'ADMIN ' + target )

def info ( self, target = None ):
    if target == None:
        self.rsend ( 'INFO' )
    else:
        self.rsend ( 'INFO ' + target )

def servlist ( self, mask = None, typa = None ):
    if mask == None:
        self.rsend ( 'SERVLIST' )
    elif typa == None and mask != None:
        self.rsend ( 'SERVLIST ' + mask )
    else:
        self.rsend ( 'SERVLIST ' + mask + ' ' + typa )

def squery ( self, sname, msg ):
    self.rsend ( 'SQUERY ' + sname + ' :' + msg )

def kill ( self, nick, msg ):
    self.rsend ( 'KILL ' + nick + ' :' + msg )
