#-*-coding=utf-8-*-
import asyncore
import socket
import time
import threading
import Queue
import logging
from TcpConnection import TcpConnection

       # except:
       #     logger.error(u"accept 出现未知异常") 

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
        self.clients = []


    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            logger.warn(u"accept 出现异常")
        else: 
            logger.debug(u"{} 请求连接成功".format(pair[1]))
            self.clients[pair[0].fileno()] = TcpConnection(pair[0], self)

    def remove_client(self, fileno):
        self.clients[]



