# -*- coding=utf8 -*-
import string
import socket
import struct

HEAD_SIZE = 5#
HEAD_PAD = '&'
MAX_SEND_SIZE = 4096 - HEAD_SIZE

class MySocket:
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		else:
			self.sock = sock
	
	def connect(self, host, port):
		self.sock.connect((host,port))

	def send2(self, msg):
		msg = struct.pack('s', msg)
		print len(msg)


	def send(self, msg):
		msglen = len(msg)
		if (msglen> MAX_SEND_SIZE):
			raise RuntimeError(u'发送数据超过最大值')
		
		head = string.ljust(str(msglen), HEAD_SIZE,HEAD_PAD)
		data = head + msg
		totalSize = msglen + HEAD_SIZE
		totalSent = 0
		while totalSent < totalSize:
			sent = self.sock.send(data[totalSent:])
			if sent == 0:
				raise RuntimeError(u"socket 连接断开")
			totalSent = totalSent + sent
			
	def _recv_head_size(self):
		chunks = ''
		totalrecv = 0
		while totalrecv < HEAD_SIZE:
			chunk = self.sock.recv(HEAD_SIZE - totalrecv)
			if chunk == '':
				raise RuntimeError(u"socket 连接断开")
			chunks = chunks + chunk
			totalrecv = totalrecv + len(chunk)
		
		chunks = chunks[:chunks.find(HEAD_PAD)]
		return int(chunks)

	def recv(self):
		dataSize = self._recv_head_size()
		remain = dataSize
		chunks = ''
		while remain > 0:
			chunk = self.sock.recv(remain)
			if chunk == '':
				raise RuntimeError(u'断开连接')
			chunks = chunks + chunk
			remain = remain - len(chunk)
		return chunks

	def bind(self, host, port):
		self.sock.bind((host, port))
	
	def listen(self, n):
		self.sock.listen(n)

	def accept(self):
		return self.sock.accept()

	def close(self):
		self.sock.close()
		
				
