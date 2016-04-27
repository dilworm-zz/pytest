#-*-coding=utf8-*-
import asyncore, socket, time

class RedisInfoClient(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.host = host
        self.port = port
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cmd ="*1\r\n$4\r\nping\r\n"
        self.buf =self.cmd

    def connect(self):
        asyncore.dispatcher.connect(self, (self.host, self.port))

    def handle_connect(self):
        print u"connected to " + self.host + u":" + str(self.port)

    def handle_read(self):
        print self.recv(8192)

    def handle_write(self):
        #self.send()
        #asyncore.dispatcher.connect(self, (self.host, self.port))
        sent = self.send(self.buf)
        time.sleep(2)
       # if sent == len(self.buf):
       #     self.buf=self.cmd
       # else:
       #     self.buf=self.buf[sent:]

client = RedisInfoClient('127.0.0.1', 52021)
client.connect()

asyncore.loop()
print "end"
