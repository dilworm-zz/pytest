#-*-coding=utf-8-*-
import asyncore
import socket
import time
import threading
import Queue
import logging

logger = logging.getLogger("cf")


def timer_check_connection(conn):
    if not (conn.is_connected() or conn.is_connecting()):
        conn.connect()

class TcpClient(asyncore.dispatcher):
    def __init__(self, (host, port)):
        asyncore.dispatcher.__init__(self) 
        self.host = host
        self.port = port
        
        self.outbufferqueue = Queue.Queue()
        self.inbufferqueue = Queue.Queue()
        self.outbuffer = ""

        self._readable = True
        self._writeable = True
        self.connecting = False
        self.connected = False

        self.stopping = False

    def start(self):
        self.connect()
        while (not self.stopping):
            asyncore.loop(0.1)

    def try_connect(self):
        if self.connecting or self.connected:
            return None

    def connect(self):
        assert(not self.connecting)
        assert(not self.connected)
        assert(self.host and self.port)
        if (self.socket is None):
           asyncore.dispatcher.create_socket(self, socket.AF_INET, socket.SOCK_STREAM)
        #self.set_readable(False)
        #self.set_writeable(False)
        asyncore.dispatcher.connect(self, (self.host, self.port))

    def set_readable(self, r):
        self._readable = r

    def set_writeable(self, w):
        self._writeable = w

    def readable(self):
        return self._readable

    def writable(self):
        self.try_connect()
        return self._writeable

    def handle_connect(self):
        logger.debug(u"{0}:{1}: 连接成功.".format(self.host, self.port))

    def handle_write(self):
        self.send("hello")
        self.set_writeable(False)

    def handle_read(self):
        print(self.recv(1024))

    #def handle_error(self):
    #    print "error"

    def handle_close(self):
        logger.info(u"{} 连接断开. {}".format(self.host, self.socket))
        self.close()
        print self.socket
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.setblocking(0)
        self.set_socket(new_sock)
        print "new ",new_sock
        self.set_readable(False)
        self.set_writeable(False)


if __name__ == "__main__":
    from logger import initlogger 
    initlogger()
    client = TcpClient(("127.0.0.1", 9999))
    client.start()
    print "end"

