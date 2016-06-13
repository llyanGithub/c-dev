#! /usr/bin/python
#--coding=utf-8--

import socket
import threading
import time
import signal
import sys

host = '127.0.0.1'
port = 50008
is_exit = False

class thread_client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.s.connect((host, port))
        i = 0
        while i != 5:
            if is_exit:
                return
            i = i + 1
            try:
                self.s.sendall('hello server %s', i)
                print 'client send ', i
            except:
                print 'client send message error'
                return
            time.sleep(1)

        try:
            self.s.sendall('q')
        except:
            print 'client send message error'
            return
        self.s.close()

class thread_child(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn

    def run(self):
        while not is_exit:
            data = self.conn.recv(1024)
            print 'receive data from client', data
            if data == 'q':
                self.conn.close()
                break;

class thread_server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((host, port))

    def run(self):
        while not is_exit:
            self.s.listen(1)

            conn, addr = self.s.accept()
            print 'Conneted by ', addr

            thread =  thread_child(conn)
            thread.start()

def handler(signum, frame):
    global is_exit
    is_exit = True
    print "receive a signal %d, is_exit = %d" % (signum, is_exit)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)
    while not is_exit:
       time.sleep(1) 

    #if sys.argv[1] == 's':
        #thread = thread_server()
        #thread.start()
        #thread.join()
        #print 'main thread quit'
    #elif sys.argv[1] == 'c':
        #thread = thread_client()
        #thread.start()
        #thread.join()
        #print 'main thread quit'

