from __future__ import print_function, division
import socket, time

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

class SocketClient():
    """ this client sends data as long as DataController returns non-empty strings"""
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.buffer = ''
        self.sent = 0
        self.DC = DataController()
        print("init done")
        
    def __del__(self):
        self.socket.close()
        
    def run(self):
        self.buffer += self.DC.GetData()
        while len(self.buffer) > 0:
            print("sending", self.buffer)
            self.sent = self.socket.send(self.buffer)
            self.buffer = self.buffer[self.sent:] # rest of buffer remains in buffer
            self.buffer += self.DC.GetData()
            time.sleep(1)
        print("done")
            
SC = SocketClient('localhost', 8080)
SC.run()