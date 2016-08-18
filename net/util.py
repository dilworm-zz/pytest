#-*-coding=utf-8-*-
import socket

def getLocalIp():
    name = socket.getfqdn(socket.gethostname())
    addr = socket.gethostbyname(name)
    print name

    print socket.gethostbyname(socket.gethostname())
    print socket.gethostbyname_ex(socket.gethostname())

    return addr

if __name__ == "__main__":
    getLocalIp()
