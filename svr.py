# -*- coding=utf8 -*-
import sys
from mysocket import MySocket

# 默认侦听的IP和端口
HOST = ''
PORT = 8888

clients = []

class RequestHandle():
	def __init__(self, mysocket):
		self.mysocket = mysocket
	
	def Run(self):
		try:
			while True:
				data = self.mysocket.recv()
				print 'Run..'
				print data 
				self.mysocket.send('i got you')
				self.mysocket.send(data)
				break
		except RuntimeError, msg:
			print u'异常，断开连接'
			print u'', msg
		finally:
			self.mysocket.close()

	def OnReady(msg):pass
	def OnUpdate(msg):pass

	
class BlockServer():
	def __init__(self, mysocket = None):
		if mysocket is None:
			self.mysocket = MySocket()
		else:
			self.mysocket = mysocket
	
	def __init__(self, host, port):
		self.mysocket = MySocket()
		self.host = host
		self.port = port
	
	def run_forever(self):
		print u'listening on ', self.host,':', self.port
		self.mysocket.bind(self.host, self.port)
		self.mysocket.listen(1)
		while True:
			sock, addr = self.mysocket.accept()
			if sock is not None:
				print 'connected by ', addr
			cli = MySocket(sock)
			requestHandler = RequestHandle(cli)
			requestHandler.Run()



def main(argv):
	if len(argv) > 3:
		print u'Error: 参数过多'
		return
	
	host = HOST
	port = PORT

	if len(argv) == 2:
		port = int(argv[1])
		print 'p ', port
	if len(argv) == 3:
		host = argv[1]
		port = int(argv[2])
	
	svr = BlockServer(host, port)
	svr.run_forever()

if __name__ == '__main__':
	main(sys.argv)

