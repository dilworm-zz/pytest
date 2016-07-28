#-*-coding=utf-8-*-
import SocketServer

class MyTcpHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print "*"*20
        print self.data
        self.request.send("world")


HOST, PORT = "localhost", 9999
server = SocketServer.TCPServer((HOST,PORT), MyTcpHandler)
server.serve_forever()
