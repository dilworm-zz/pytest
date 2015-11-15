# -*- coding=utf8 -*-

def GetServerList(filename):
	serverlist = []
	lines = open(filename).read().splitlines()
	for l in lines:
		addr = l.split(' ')
		if len(addr) == 2:
			serverlist.append((addr[0], addr[1]))
			#print (addr[0], addr[1])
	return serverlist


#Test
#:GetServerList('./serverlist.txt')



