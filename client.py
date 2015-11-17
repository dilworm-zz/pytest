# -*- coding=utf8 -*-
import select
import thread
import Queue
import configparser as cf
from mysocket import MySocket


def networkHandler(svrSockets):
  rl, wl, xl = svrSockList, [], []
  for k,v in svrSockets:
    v.setnoblock()
    rl.append(k)

  while True:
    rl, wl, xl = select.select(rl, wl, xl, 3000)
    if (rl or wl or xl):
      continue

    for s in rl:
      pass


def main():
  serverList = cf.GetServerList('./serverlist.txt')
  print u'找到',len(serverList), u'个服务器地址:'
  for addr in serverList:
    print addr

  print ''
  svrSockets = {}
  for addr in serverList:
    try:
      s = MySocket()
      s.connect(addr[0], addr[1])
      svrSockets[s.getsocket()] = s
    except:
      print u'Error: 连接', addr, u'出错'
   
  network_thread = thread.Thread(target = networkHandler, args = svrSockets)
  network_thread.start()

  while True:
    pass


if __name__ == '__main__':
  main()
