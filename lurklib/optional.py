def s_away ( self, msg ):
    self.rsend ( 'AWAY :%s' % msg )
    if self.readable():
        ncode = self.recv().split() [1]
        if ncode == '306': self.away = True
        elif ncode == '305': self.away = False

def rehash ( self ):
    self.rsend ( 'REHASH' )
    if self.readable():
        segments = self.recv().split()
        if segments [1] == '382': pass
        elif segments [1] in self.err_replies: self.exception ( segments [1] )
        else: self.index -= 1

def die ( self, password = '' ):
    self.rsend ( 'DIE :%s' % password )
    if self.readable():
        segments = self.recv().split()
        if segments [1] == self.err_replies: self.exception ( segments [1] )
        else: self.index -= 1

def restart ( self, password = '' ):
    self.rsend ( 'RESTART :%s' % password )
    if self.readable():
        segments = self.recv().split()
        if segments [1] in self.err_replies: self.exception ( segments [1] )
        else: self.index -= 1
        
def summon ( self ): pass

def users ( self ): pass

def operwall ( self, msg ): self.rsend ( 'WALLOPS :%s' % msg )

def userhost ( self, nick ):
    self.rsend ( 'USERHOST :%s' % nick )
    rvalue = ''
    if self.readable():
        segments = self.recv().split()
        if segments [1] == '302': rvalue = ' '.join ( segments [3:] ) [1:]
        elif segments [1] in self.err_replies: self.exception ( segments [1] )
        else: self.index -= 1
    return rvalue

def ison ( self, nick ):
    self.rsend ( 'ISON :%s' % nick )
    rvalue = ''
    if self.readable():
        segments = self.recv().split()
        if segments [1] == '303': rvalue = ' '.join ( segments [3:] ) [1:]
        elif segments [1] in self.err_replies: self.exception ( segments [1] )
        else: self.index -= 1
    return rvalue