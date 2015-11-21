# -*- coding=utf8 -*-
import sys
from mysocket import MySocket

class RequestHandle():
  def __init__(self, mysocket):
    self.mysocket = mysocket
  
  def Run(self):
    try:
      while True:
        print 'Run..'
        data = self.mysocket.recv()
        if not data:
          break
        else:
          print 'recv', data

        respone = 'i got you \"' + data + '"'
        self.mysocket.send(respone)
    except RuntimeError, msg:
      print msg
      pass
    finally:
      print 'finally'
      self.mysocket.close()

  def OnReady(*args):
    pass
  def OnUpdate(msg):pass

  
class BlockServer():
  def __init__(self, mysocket = None, MsgHandler = None):
    if mysocket is None:
      self.mysocket = MySocket()
    else:
      self.mysocket = mysocket
    self.msg_handler = MsgHandler
  
  def __init__(self, host, port, MsgHandler = None):
    self.mysocket = MySocket()
    self.host = host
    self.port = port
    self.msg_handler = MsgHandler
  
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

