#-*-coding=utf-8-*-
import asyncore
import socket
import time
import threading
import Queue
import logging
import traceback
import packetparser as pp


logger = logging.getLogger("cf")

CONNECT_INTERVAL = 5 # seconds

def timer_check_connection(conn):
    if not (conn.is_connected() or conn.is_connecting()):
        conn.connect()

def make_nonblocking_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    return s

class TcpClient(asyncore.dispatcher):
    def __init__(self, (host, port)):
        asyncore.dispatcher.__init__(self) 
        self.host = host
        self.port = port
        
        self.outbufferqueue = Queue.Queue()
        self.inbufferqueue = Queue.Queue()
        self.outbuffer = "" # data that need to be send at the moment.

        self._readable = False
        self._writeable = False
        self.connecting = False
        self.connected = False

        self.stopping = False

    def start(self):
        self.connect()
        asyncore.loop(1)


    def add2Queue(self, data):
        try:
            self.outbufferqueue.put((data, time.time()))
            self.set_writeable(True)
            return True
        except Queue.Full:
            logger.error("add2Qeueu Failed!")
            return False

    def try_connect(self):
        print "try_connect connecting = ", self.connecting, "connected = ", self.connected
        if (not self.connecting and 
            not self.connected and 
            (time.time() - self.lastconntime > CONNECT_INTERVAL)):
            self.connect()
            
    def connect(self):
        assert(not self.connecting)
        assert(not self.connected)
        assert(self.host and self.port)
        logger.debug(u"正在连接 {}:{}".format(self.host, self.port))
        
        if self.socket is not None:
            #print "call dispatcher.close"
            self.close()
            #asyncore.dispatcher.close(self)

        asyncore.dispatcher.create_socket(self, socket.AF_INET, socket.SOCK_STREAM)
        #print "fileno = ", self.socket.fileno()
        asyncore.dispatcher.connect(self, (self.host, self.port))
        #print "connect map len", len(self._map)
        self.set_readable(False)
        self.set_writeable(True)
        self.lastconntime = time.time()

    def set_readable(self, r):
        self._readable = r

    def set_writeable(self, w):
        self._writeable = w

    def readable(self):
        self.try_connect()
        return self._readable

    def writable(self):
        # FIXME: Generally, should check outbuffer and outbufferqueue to decide 
        # a writeable state, because set_writeable is not thread safety.
        return self._writeable

    def handle_connect(self):
        traceback.print_stack()
        logger.debug(u"{0}:{1} 连接成功.".format(self.host, self.port))
        self.set_readable(True)
        self.add2Queue("hello")

    def handle_write(self):
        if len(self.outbuffer) > 0:
            s = self.send(self.outbuffer)
            if s > 0:
                self.outbuffer = self.outbuffer[s:]
        elif not self.outbufferqueue.empty():
            try:
                item = self.outbufferqueue.get(True, 0.01)
                self.outbuffer = item[0]
                s = self.send(self.outbuffer)
                if s > 0:
                    self.outbuffer = self.outbuffer[s:]
            except Queue.Empty:
                pass
        else:
            # no more data to sent
            self.set_writeable(False)


    def handle_read(self):
        print(self.recv(1024))

   # def handle_error(self):
   #     self.set_readable(false)
   #     self.set_writeable(false)
   #     if (self.connecting):
   #         logger.warn(u"连接{}:{}失败!".format(self.host, self.port))
   #         asyncore.dispatcher.close(self)
   #         sock = make_nonblocking_socket()
   #         self.set_socket(sock)
   #         print "h e map len", len(self._map)
   #         self.connecting = False
   #     elif self.connected:
   #         logger.warn(u"{}:{} 异常断开".format(self.host, self.port))
   #         self.connected = False
   #     
        #traceback.print_stack()

    def handle_close(self):
        if self.connecting:
            logger.warn(u"连接{}:{} 失败!".format(self.host, self.port))
            self.connecting = False
        elif self.connected:
            logger.info(u"{} 连接断开".format(self.host))
            self.connected = False
        self.set_readable(False)
        self.set_writeable(False)
        #print "handle close self.socket ", self.socket

        # insert new socket into map, make sure the loop won't break out 
        # when map is empty.
        #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.setblocking(0)
        #self.set_socket(sock)
        
        traceback.print_stack()


if __name__ == "__main__":
    from logger import initlogger 
    initlogger("client")
    client = TcpClient(("127.0.0.1", 9999))
    client.start()
    print "end"

