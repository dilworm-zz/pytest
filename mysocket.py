# -*- coding=utf8 -*-
# 暂时不支持发送中文
import string
import socket
import struct

HEAD_SIZE = 5 # 前五个字节指名后面的数据包大小 
HEAD_PAD = '&'# 用于填充前5个字节中的“字位置”
MAX_SEND_SIZE = 4096 - HEAD_SIZE

class MySocket:
  def __init__(self, sock = None):
    if sock is None:
      self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    else:
      self.sock = sock
  
  def getsocket(self):
    return self.sock

  def setnoblock(self):
    self.sock.setblocking(False)

  def fileno(self):
    return self.sock.fileno()

  def getpeername(self):
    return self.sock.getpeername()

  def connect(self, host, port):
    self.sock.connect((host,port))
    self.peer_host = host
    self.peer_port = port

  def getpeername(self):
    return self.peer_host, self.peer_port

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
      try:
        chunk = self.sock.recv(HEAD_SIZE - totalrecv)
      except socket.error, msg:
        print msg
        return 0
      if chunk == '':
        print u'连接断开 ', self.sock.getpeername()
        return 0

      chunks = chunks + chunk
      totalrecv = totalrecv + len(chunk)
    
    chunks = chunks[:chunks.find(HEAD_PAD)]
    return int(chunks)

  def recv(self):
    dataSize = self._recv_head_size()
    if not dataSize:
      return ''
    remain = dataSize
    chunks = ''
    while remain > 0:
      chunk = self.sock.recv(remain)
      if chunk == '':
        print u'连接断开 ', self.sock.getpeername()
        return ''
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
