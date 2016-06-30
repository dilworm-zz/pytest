#-*- coding=utf8 -*-
import sys
from TcpServer import * 
import BaseMsgHandler

# 默认侦听的IP和端口
HOST = ''
PORT = 8888

clients = []

def printhelp():
  print u'使用格式 python svr.py [[host] port] \n eg: '
  print u'\t1. "python svr.py"'
  print u'\t2. "python svr.py 8888"'
  print u'\t2. "python svr.py 127.0.0.1 8888"'

def main(argv):
  if len(argv) > 3:
    print u'Error: 参数过多'
    printhelp()
    return
  
  host = HOST
  port = PORT

  if len(argv) == 2:
    port = int(argv[1])
  if len(argv) == 3:
    host = argv[1]
    port = int(argv[2])
  
  svr = BlockServer(host, port)
  svr.run_forever()

if __name__ == '__main__':
  main(sys.argv)

