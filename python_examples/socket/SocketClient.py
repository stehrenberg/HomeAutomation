from __future__ import print_function, division
import asyncore, socket, time

class DataController():
    def __init__(self):
        self.template = 'testdata_{0}'
        self.loopcount = 0
        
    def GetData(self):
        if self.loopcount < 5:
            self.loopcount += 1
            return self.template.format(self.loopcount)
        else:
            return ''
        
        
class SocketClient(asyncore.dispatcher):
    """This client is able to send and receive data from the SocketServer"""
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        # connect to server
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect( (host, port) )
        # data handling stuff
        self.buffer = '' # data to be sent
        self.sent = 0
        self.DC = DataController()
        print('SocketClient: init done')

    def handle_connect(self):
        pass
    
    def handle_close(self):
        self.close()

    def handle_read(self):
        rec_data = self.recv(8192) # test with 8 bytes!
        print("received", rec_data)

    def writable(self): # as long as this function return True, data will be sent
        self.buffer += self.DC.GetData()
        return len(self.buffer)

    def handle_write(self):
            print("sending", self.buffer)
            self.sent = self.send(self.buffer) # returns the number of bytes sent
            self.buffer = self.buffer[self.sent:] # rest of buffer remains in buffer
            time.sleep(1) # slow down the client process ...


client = SocketClient('localhost', 8080)
asyncore.loop()


