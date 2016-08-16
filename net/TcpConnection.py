#-*-coding=utf-8-*-

import asyncore
import socket
import time
import threading
import Queue
import logging
import packetparser as pp

logger = logging.getLogger("cf")

class TcpConnection(asyncore.dispatcher):

    def __init__(self, sock, tcpserver):
        asyncore.dispatcher.__init__(self, sock)

        self.outbufferqueue = Queue.Queue()
        self.inbufferqueue = Queue.Queue()
        self.inbuffer = ""
        self.outbuffer = ""
        self._readable = True
        self._writeable = True

        self.tcpserver = tcpserver # point to the server
        self.cmddispatcher = self.tcpserver.dispatcher

    def _clear(self):
        self.outbufferqueue = Queue.Queue()
        self.inbufferqueue = Queue.Queue()
        self.inbuffer = ""
        self.outbuffer = ""

    def set_readable(self, r):
        self._readable = r

    def set_writeable(self, w):
        self._writeable = w

    def readable(self):
        return self._readable

    def writable(self):
        return self._writeable

    def handle_read(self):
        try:
            s = self.recv(4096)
            if len(s) > 0:
                self.inbuffer = self.inbuffer + s
                data = pp.unpack(self.inbuffer)
                if data is not None:
                    self.cmddispatcher.onReceiveData(self, data)
        except Exception as e :
            logger.error(u"接收数据发生异常,将主动断开{}连接".format(self.addr))
            print e
            self.close()
            self._clear()
    
    def handle_write(self):
        pass

    def handle_close(self):
        logger.info(u"{}:{} 断开连接".format(self.addr[0], self.addr[1]))
        #self.close_callback(self.socket)
        self.close()
   
