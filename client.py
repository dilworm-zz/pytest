# -*- coding=utf8 -*-
import select
import thread
import Queue
import configparser as cf
from mysocket import MySocket


g_messageQueues = {} #每个scoket分配一个队列用于读写
g_messageQueues['main'] = Queue.Queue()

svrSockets = {}

class Item:
  def __int__(self, msgType, socket, data):
    self.msgType = msgType
    self.socket = socket
    self.data = data

def userInputThreadHandler(mainQueue,)

def networkThreadHandler(svrSockets, msgQueues):
  rl, wl, xl = svrSockList, [], []
  for k,v in svrSockets:
    v.setnoblock() # 设置为非阻塞
    rl.append(k)

  while True:
    rl, wl, xl = select.select(rl, wl, xl, 3000)
    if (rl or wl or xl):
      continue

    for s in rl:
      data = svrSockets[s].recv()

      if data == '':
        print u'Error: 连接断开', s.getpeername() 
        rl.remove(s)
        del msgQueues[s]
      else:
        item = Item('read', s, data)
        msgQueues['main'].put(item) # 投递到主队列进行处理
        wl.append(s) # 等下一次用户命令

    for s in wl:
      item = msgQueues[s].get_nowait()
      if item and item.socket:
        svrSockets[s].send(item.data)
        rl.append(s) # 准备接收服务器返回的消息
       else:
         wl.append(s)

      
def OnQueueMsg(msg):
  pass

def main():
  serverList = cf.GetServerList('./serverlist.txt')
  print u'找到',len(serverList), u'个服务器地址:'
  for addr in serverList:
    print addr

  print ''
  for addr in serverList:
    try:
      s = MySocket()
      s.connect(addr[0], addr[1])
      svrSockets[s.getsocket()] = s
    except:
      print u'Error: 连接', addr, u'失败'
   
  network_thread = thread.Thread(target = networkThreadHandler, args = g_messageQueues)
  network_thread.start()
  userInput_thread = thread.Thread(target = userInputThreadHandler, args =())
  while True:
    OnQueueMsg(g_messageQueues['main'].get())


if __name__ == '__main__':
  main()
