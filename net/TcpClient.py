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

CONNECT_INTERVAL = 5 # reconnect timeout. seconds

def timer_check_connection(conn):
    if not (conn.is_connected() or conn.is_connecting()):
        conn.connect()

def make_nonblocking_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.setblocking(0) 
    return s 

class TcpClient(asyncore.dispatcher):
    def __init__(self, (host, port), commanddispatcher):
        asyncore.dispatcher.__init__(self) 
        self.host = host
        self.port = port
        self.cmddispatcher = commanddispatcher
        
        self.outbufferqueue = Queue.Queue()
        self.outbuffer = "" # data that need to be send at the moment.
        self.inbuffer = "" 

        self._readable = False
        self._writeable = False
        self.connecting = False
        self.connected = False

        self.started = False

    def _clear(self):
        self.outbufferqueue = Queue.Queue()
        self.inbufferQueue = Queue.Queue()
        self.outbuffer = ""
        self.inbuffer = ""

    def start(self):
        self.started = True
        self.connect()
        asyncore.loop(1)

    def send(self, data):
        assert(self.started)
        try:
            #print "-"*200
            #traceback.print_stack()
            packed = pp.pack(data)
            self.outbufferqueue.put((packed, time.time()))
            self.set_writeable(True)
            return True
        except Queue.Full:
            logger.error("add data to qeueu FAILED!")
            return False

    def try_connect(self):
        #print "try_connect connecting = ", self.connecting, "connected = ", self.connected
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
        # FIXME: Generally, checking outbuffer and outbufferqueue to determine
        # a writeable state, because set_writeable is not thread safety.
        return self._writeable

    def handle_connect(self):
        #traceback.print_stack()
        logger.debug(u"{0}:{1} 连接成功.".format(self.host, self.port))
        self.set_readable(True)
        if hasattr(self.cmddispatcher, "handle_connect"):
            cmddispatcher.handle_connect()

    def handle_write(self):
        if len(self.outbuffer) > 0:
            s = self.send(self.outbuffer)
            if s > 0:
                self.outbuffer = self.outbuffer[s:]
                #print 1
        elif not self.outbufferqueue.empty():
            try:
                #print 2
                item = self.outbufferqueue.get(True, 0.01)
                self.outbuffer = item[0]
                s = asyncore.dispatcher.send(self, self.outbuffer)
                if s > 0:
                    self.outbuffer = self.outbuffer[s:]
            except Queue.Empty:
                pass
        else:
            # no more data to sent
            #print 3
            self.set_writeable(False)


    def handle_read(self):
        try:
            s = self.recv(4096)
            if len(s) > 0:
                print s
                self.inbuffer = self.inbuffer + s
                data = pp.unpack(self.inbuffer)
                if data is not None:
                    self.cmddispatcher.onReceiveData(data)
        except Exception as e:
            print e
            logger.error(u"接收数据出现异常，将主动断开连接 {}:{} ".format(
                self.host, self.port))
            self.peer.close()

        
    def handle_close(self): 
        if self.connecting:
            logger.warn(u"连接{}:{} 失败!".format(self.host, self.port))
            self.connecting = False 
        elif self.connected: 
            logger.info(u"{} 连接断开".format(self.host))
            self.connected = False
        self.set_readable(False)
        self.set_writeable(False)
        self._clear()
        
        #traceback.print_stack()


if __name__ == "__main__":
    from logger import initlogger
    initlogger("./log/tcplclient")
    c = TcpClient(("127.0.0.1", 9999))
    c.start()
