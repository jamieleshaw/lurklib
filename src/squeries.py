# This module is not done yet.
def motd ( self, server = None ):
    if server == None:
        self.rsend ( 'MOTD' )
    else:
        self.rsend ( 'MOTD ' + server )

def lusers ( self, mask = None, target = None ):
    if mask == None:
        self.rsend ( 'LUSERS' )
    elif target == None and mask != None:
        self.rsend ( 'LUSERS ' + mask )
    else:
        self.rsend ( 'LUSERS ' + mask + ' ' + target )


def version ( self, target = None ):
    if target == None:
        self.rsend ( 'VERSION' )
    else:
        self.rsend ( 'VERSION ' + target )


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

def time ( self, target = None ):
    if target == None:
        self.rsend ( 'TIME ' + target )
    else:
        self.rsend ( 'TIME' )

def connect_s ( self, tserver, tport, r_server = None ):
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
