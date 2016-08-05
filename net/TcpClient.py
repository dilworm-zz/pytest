#-*-coding=utf-8-*-
import asyncore
import socket
import time
import threading
import Queue
import logging
import traceback

logger = logging.getLogger("cf")

CONNECT_INTERVAL = 5 # seconds

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
        self._writeable = False
        self.connecting = False
        self.connected = False

        self.stopping = False

    def start(self):
        self.connect()
        while (not self.stopping):
            asyncore.loop(1)

    def try_connect(self):
        print "try_connect"
        if (not self.connecting and 
            not self.connected and 
            (time.time() - self.lastconntime > CONNECT_INTERVAL)):
            self.connect()
            

    def connect(self):
        assert(not self.connecting)
        assert(not self.connected)
        assert(self.host and self.port)
        logger.debug(u"正在连接{}:{}".format(self.host, self.port))
        self.set_readable(True)
        
        asyncore.dispatcher.create_socket(self, socket.AF_INET, socket.SOCK_STREAM)
        print "fileno = ", self.socket.fileno()
        asyncore.dispatcher.connect(self, (self.host, self.port))
        self.lastconntime = time.time()

    def set_readable(self, r):
        self._readable = r

    def set_writeable(self, w):
        self._writeable = w

    def readable(self):
        self.try_connect()
        return self._readable

    def writable(self):
        return self._writeable

    def handle_connect(self):
        logger.debug(u"{0}:{1} 连接成功.".format(self.host, self.port))
        self.set_writeable(True)

    def handle_write(self):
        self.send("hello")
        self.set_writeable(False)

    def handle_read(self):
        print(self.recv(1024))

    def handle_error(self):
        if (self.connecting):
            logger.warn(u"连接{}:{}失败!".format(self.host, self.port))
            self.connecting = False
            self.set_readable(False)
            self.set_writeable(False)

    def handle_close(self):
        assert(self.connecting)
        logger.info(u"{} 连接断开. {}".format(self.host, self.socket))
        self.close()
        self.socket = None
        self.set_writeable(False)

        # insert new socket into map, make sure the loop won't break out 
        # when map is empty.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(0)
        self.set_socket(sock)
        self.set_readable(True)
        
        traceback.print_stack()


if __name__ == "__main__":
    from logger import initlogger 
    initlogger()
    client = TcpClient(("127.0.0.1", 9999))
    client.start()
    print "end"

