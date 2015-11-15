# -*- coding=utf8 -*-
from mysocket import MySocket

clients = []
s = MySocket()

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
		self.mysocket.bind(self.host, self.port)
		self.mysocket.listen(1)
		print u'listening on ',  self.port
		while True:
			sock, addr = self.mysocket.accept()
			if sock is not None:
				print 'connected by ', addr
			cli = MySocket(sock)
			requestHandler = RequestHandle(cli)
			requestHandler.Run()


svr = BlockServer('', 8888)
svr.run_forever()

			
