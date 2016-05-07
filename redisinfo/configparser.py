# -*- coding=utf8 -*-

def GetServerList(filename):
  serverlist = []
  lines = open(filename).read().splitlines()
  for l in lines:
    item = l.split(' ')
    if len(item) != 4:
        raise RuntimeError("Load redis config failed!")
    serverlist.append((item[0], int(item[1]),int(item[2]), item[3]))
    print (item[0], int(item[1]),int(item[2]), item[3]) 
  return serverlist


#Test
#:GetServerList('./serverlist.txt')



