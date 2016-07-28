#-*-coding=utf-8-*-
import asyncore
import socket
import time
import threading
import Queue
import logging

logger = logging.getLogger("cf")

CONN_TIMEOUT = 15

def timer_check_connection(conn):
    if not (conn.is_connected() or conn.is_connecting()):
        conn.connect()

class TcpClient(asyncore.dispatcher):
    def __init__(self, (host, port)):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port
        self.outBufferQueue = Queue.Queue()
        self.inBufferQueue = Queue.Queue()
        self.outbuffer = ""
        self._readable = False
        self._writeable = False

    def connect(self):
        assert(self.host and self.port)
        if (self.socket is None):
           asyncore.dispatcher.create_socket(self, socket.AF_INET, socket.SOCK_STREAM)
        self.set_readable(False)
        self.set_writeable(False)
        asyncore.dispatcher.connect(self, (self.host, self.port))

    def set_readable(self, r):
        self._readable = r

    def set_writeable(self, w):
        self._writeable = w

    def readable(self):
        return self._readable

    def writeable(self):
        return self._writeable

    def handle_connect(self):
        logger.debug(u"{0}: connected to {1}:{2}".format(time.time(), self.host, self.port))

    def handle_write(self):
        self.send("hello")
        #self.set_readable(False)
        self.set_writeable(False)

    def handle_read(self):
        print(self.recv(1024))


if __name__ == "__main__":
    client = TcpClient(("127.0.0.1", 9999))
    client.connect()
    asyncore.loop(0.1)
    print "end"

