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
    print u'使用：'
    print u'\t1. "python svr.py"'
    print u'\t2. "python svr.py 8888"'
    print u'\t2. "python svr.py 127.0.0.1 8888"'
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

