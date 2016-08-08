#-*-coding=utf-8-*-
import sys
sys.path.append("..")

if __name__ == "__main__":
    import logger
    import asyncore
    from TcpServer import TcpServer
    from logger import initlogger

    initlogger("./log/server")

    svr = TcpServer(('127.0.0.1', 9999))
    asyncore.loop(0.1)
