def msg (self, target, message):
    ''' Sends a PRIVMSG '''
    with self.lock:
        self.rsend ('PRIVMSG ' + target + ' :' + message)
        if self.readable():
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                self.exception (ncode)
            elif ncode == '301': return ('AWAY', data.split (None, 3) [3] [1:])
def notice (self, target, message):
    ''' Sends a NOTICE '''
    with self.lock:
        self.rsend ('NOTICE ' + target + ' :' + message)
        if self.readable():
            data = self.recv()
            ncode = data.split() [1]
            if ncode in self.err_replies.keys():
                self.exception (ncode)
            elif ncode == '301': return ('AWAY', data.split (None, 3) [3] [1:])
