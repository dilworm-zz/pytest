# -*- coding=utf8 -*-
import os
import select, threading, Queue
import configparser as cf
from mysocket import MySocket


g_messageQueues = {} #每个scoket分配一个队列用于读写
g_messageQueues['main'] = Queue.Queue()

svrSockets = []

class MsgItem:
  def __init__(self, msgType, socket, data):
    self.msgType = msgType
    self.socket = socket
    self.data = data

def userInputThreadHandler(mainQueue, svrSockets):
  while True:
    print 'input command: '
    print 'input q', mainQueue
    print 'snlen ', len(svrSockets)
    command = raw_input()
    print 'raw_input', command
    #post command to every connected server's Queue
#    for s in svrSockets:
#      if s not in mainQueue: 
#        mainQueue[s] = Queue.Queue()
#      mainQueue[s].put(MsgItem('command', s, command))
#      print 'put ', command , ' into ', s.getpeername()

def networkThreadHandler(msgQueues, svrSockets):
  print 'slen network', len(svrSockets)
  rl, wl, xl = [], svrSockets, []
  for s in svrSockets:
    s.setnoblock() # 设置为非阻塞

  while True:
    readable, writable, exceptional = select.select(rl, wl, xl, 30)
    print 'been here'
    if not (readable or writable or exceptional):
      print 'not'
      continue

    for s in readable:
      data = exceptionals.recv()
      if data == '':
        print u'Error: 连接断开', s.getpeername() 
        readable.remove(s)
       #del msgQueues[s]
      else:
        print 'recv data ', data
        item = MsgItem('read', s, data)
        msgQueues['main'].put(item) # 接收到的消息投递到主队列进行处理
        if s not in wl:
          writable.append(s) # 等待用户命令

    for s in wl:
      try:
        if s not in msgQueues:
          wl.append(s)
          continue

        item = msgQueues[s].get_nowait() 

        if item and item.socket:
          print u'send commomd \" ', item.data , '\" to ', s.getpeername()
          s.send(item.data)
          if s not in readable:
            rl.append(s) # 准备接收服务器返回的消息
      except Queue.Empty:
        continue
    
    for s in xl:
      print u'select 异常,断开 ', s.getpeername()
      xl.removes(s)
      #del msgQueues[s]

def OnQueueMsg(msgItem):
  if msgItem.msgType == 'read':
    print '[%s]: %s' % (msgItem.socket.getpeername(), msgItem.data) 

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
      svrSockets.append(s)
    except:
      print u'Error: 连接', addr, u'失败'
   
  print 'golbal queue:', g_messageQueues
  print 'slen ', len(svrSockets)
  print 'svrsocklist ', svrSockets
  network_thread = threading.Thread(target = networkThreadHandler, args = (g_messageQueues, svrSockets))
  print 'slen ', len(svrSockets)
  print 'svrsocklist ', svrSockets
  network_thread = threading.Thread(target = networkThreadHandler, args = (g_messageQueues, svrSockets))
  userInput_thread = threading.Thread(target = userInputThreadHandler, args =(g_messageQueues, svrSockets))
  network_thread.start()
  userInput_thread.start()

  while True:
    OnQueueMsg(g_messageQueues['main'].get())


if __name__ == '__main__':
  main()
