#-*-coding=utf-8-*-
import asyncore
import socket
import time
import threading
import Queue
import logging
from TcpConnection import TcpConnection 

logger = logging.getLogger("cf")

class TcpServer(asyncore.dispatcher):

    def __init__(self, (host, port)):
        logger.debug("TcpServer.__init__")
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(10)
        self.clients = {}


    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            logger.warn(u"accept 出现异常")
        else: 
            sock, addr = pair
            logger.debug(u"{} 请求连接成功".format(addr))
            self.new_connection(sock, addr)


    def new_connection(self, sock, addr):
        conn = TcpConnection(sock, self)
        self.clients[sock] = conn
        conn.handle_connect()

    def remove_connection(self, sock):
        del self.clients[sock]



