#-*-coding=utf-8-*-
import threading
import asyncore
import logging
from logger import initlogger
from TcpClient import TcpClient
from cmddispatch import *
import packetparser as pp
import ConfigParser as cp


def network_thread_handler(tcpClient): 
    tcpClient.start()

def logic_thread_handler(dispatcher):
    dispatcher.run()

class Agent:
    def __init__(self, CmdHandlerClass):
        self.dispatcher = BaseCommandDispatcher(CmdHandlerClass)
        self.dispatcher.SetConnectCallback(self.OnConnect)

    # 连接服务器成功发登陆命令
    def OnConnect(self, conn):
        req = pp.request("login", {"type":"agent", "name":self.name})
        conn.send(req)

    # 加载配置
    def loadconfig(self):
        config = cp.ConfigParser()
        config.read("./config/agent.config")
        sectionName = "NormalConfig"

        self.name = config.get(sectionName, "name")
        self.host = config.get(sectionName, "host")
        self.port = int(config.get(sectionName, "port"))

    def start(self):
        self.loadconfig()

        self.tcpClient = TcpClient((self.host, self.port), self.dispatcher)

        cmdDispatchThread = threading.Thread(target=logic_thread_handler, 
                name="logic", args=[self.dispatcher])
        tcpclientThread = threading.Thread(target=network_thread_handler, 
                name="Network", args=[self.tcpClient])

        tcpclientThread.start()
        cmdDispatchThread.start()
        tcpclientThread.join()
        cmdDispatchThread.join()


# TODO: Run agent as a deamon service.
