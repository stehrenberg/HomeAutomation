#!/usr/bin/python
# This script is started as a background process by shell script /etc/init.d/test_daemon.sh
# file should be executable
from __future__ import print_function, division
import sys
import os
import signal
import time

class Something:
    def __init__(self):
        
        # store kill command with PID in a shell script
        tmpfile = "/tmp/test_daemon_stop"
        PID = os.getpid()  
        try:
            fd = os.open(tmpfile,os.O_RDWR|os.O_CREAT, 0755)
        except:
            print("Error in test_daemon::__init__:: could not open file", file=sys.stderr)
            sys.exit(1)        
        os.write(fd,"#! /bin/sh\n")
        os.write(fd,''.join(["kill -s INT ", str(PID), "\n"]))
        os.close(fd)
        
        self.shutdownflag = False
    
    def signal_handler(self, signum, frame):
        print('Signal handler called with signal', signum)
        self.shutdownflag = True
        
    def run(self):
        while not self.shutdownflag:
            # do stuff
            print("test_daemon running")
            time.sleep(2)
                    

S = Something()
signal.signal(signal.SIGINT, S.signal_handler)
S.run()
           
    