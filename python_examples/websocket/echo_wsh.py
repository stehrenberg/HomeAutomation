from threading import Thread
from time import sleep

_GOODBYE_MESSAGE = u'Goodbye'
_HEARTBEAT = u'HEARTBEAT'
_STARTTHREAD = u'StartThread'

class ServerThread(Thread):
    """for demonstration of asynchronous messages initiated by the server"""
    def __init__(self, p_request):
        Thread.__init__(self)
        self.request = p_request
        self.shutdownflag = False
        self.started = False
    
    def run(self):
        while not self.shutdownflag:
            sleep(10)
            self.request.ws_stream.send_message("hi there!", binary=False)
            
    
def web_socket_do_extra_handshake(request):
    # This example handler accepts any request. See origin_check_wsh.py for how
    # to reject access from untrusted scripts based on origin value.

    pass  # Always accept.


def web_socket_transfer_data(request):
    server_thread = ServerThread(request)
    while True:
        line = request.ws_stream.receive_message() # this function call will return only when a message was received from the client -> blocking socket
        if line is None: # error
            server_thread.shutdownflag = True
            return
        if isinstance(line, unicode):
            if line == _GOODBYE_MESSAGE: # server side disconnect: just return from function web_socket_transfer_data()
                server_thread.shutdownflag = True
                return
            elif line == _HEARTBEAT:
                request.ws_stream.send_message('.', binary=False)
            elif line == _STARTTHREAD:
                if not server_thread.started:
                    server_thread.start()  
                    server_thread.started = True 
                    request.ws_stream.send_message('server thread started', binary=False)   
                else:
                    request.ws_stream.send_message('server thread already running', binary=False)
            else:
                request.ws_stream.send_message(line, binary=False) # echo the received text

        else:
            request.ws_stream.send_message(line, binary=True) # echo the received data


