# -*- coding=utf8 -*-
import select
import configparser as cf
from mysocket import MySocket

serverList = cf.GetServerList('./serverlist.txt')
print u'找到',len(serverList), u'个服务器地址:'
for addr in serverList:
	print addr

print len(u'菌肥l')
s = MySocket()
s.connect('127.0.0.1', 8888)
#s.send(u'菌肥lo world.. fukkk')
s.send2('o world.. fukkk')
data = s.recv()
print 'recv: ', data
data = s.recv()
print 'recv: ', data
