#-*-coding=utf-8-*-

import asyncore
import socket
import time
import threading
import Queue
import logging

logger = logging.getLogger("cf")

class TcpConnection(asyncore.dispatcher):

    def __init__(self, sock):
        asyncore.dispatcher.__init__(self, sock)

        self.outbufferqueue = Queue.Queue()
        self.inbufferqueue = Queue.Queue()
        self.outbuffer = ""
        self._readable = True
        self._writeable = True

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
            data = self.recv(1024)
            print(data)
            self.send(data.upper())
        except:
            logger.error(u"接收数据发生异常,将主动断开{}连接".format(self.addr))
            self.close()
    
    def handle_write(self):
        pass

    def handle_close(self):
        logger.info(u"{}:{} 断开连接".format(self.addr[0], self.addr[1]))
        self.close()
   
