# -*- coding=utf8 -*-
import select
import configparser as cf
from mysocket import MySocket

def main():
  serverList = cf.GetServerList('./serverlist.txt')
  print u'找到',len(serverList), u'个服务器地址:'
  for addr in serverList:
    print addr

  print ''
  sockList = []
  for addr in serverList:
    try:
      s = MySocket()
      s.connect(addr[0], addr[1])
  
    except:
      print u'Error: 连接', addr, u'出错'
      return

if __name__ == '__main__':
  main()
