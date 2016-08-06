#-*-coding=utf-8-*-
import logger
import asyncore
from TcpServer import TcpServer
from logger import initlogger

initlogger("server")
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind(("127.0.0.1", 9999))
#s.listen(4)
#
#while True:
#    sock, addr = s.accept()
#    if sock is not None:
#        r = sock.recv(1024)
#        if r is None:
#            print "closing"
#        print(r)
#        r.close()


svr = TcpServer(('127.0.0.1', 9999))
asyncore.loop(0.1)
