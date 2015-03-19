from __future__ import print_function, division
import asyncore
import socket

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192) # test with 8 bytes!
        if data:
            print("received", data)
            self.send(data)

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        print('EchoServer: listening ...')        
        self.listen(5)
        print('EchoServer: init done')

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print('Incoming connection from {0} , socket {1}'.format(repr(addr),repr(sock)))
            handler = EchoHandler(sock) # for every incoming connection there is a new instance of class EchoHandler

server = EchoServer('localhost', 8080)
asyncore.loop()

