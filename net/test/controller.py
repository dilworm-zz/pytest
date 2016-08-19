#-*-coding=utf-8-*-
import time
import threading
import Queue
import logging
from cmd import Cmd
import sys
from TcpClient import TcpClient
from cmddispatch import *
import ConfigParser as cp


logger = logging.getLogger("cf")

def network_thread_handler(tcpClient):
    tcpClient.start()

def logic_thread_handler(dispatcher):
    dispatcher.run()

def cmdloop_thread_hendler(controller):
    controller.cmdloop()

class Controller(Cmd):
    def __init__(self, host, port, CmdHandlerClass):
        Cmd.__init__(self)
        self.use_rawinput = False
        self.dispatcher = BaseCommandDispatcher(CmdHandlerClass)
        self.dispatcher.SetConnectCallback(self.OnConnect)
    
    # 连接服务器成功后，发登陆命令
    def OnConnect(self, conn):
        req = pp.request("login", {"type":"controller", "name":self.name})
        conn.send(req)

    # 加载配置
    def loadconfig(self):
        config = cp.ConfigParser() 
        config.read("./config/controller.config")
        sectionName = "NormalConfig"

        self.name = config.get(sectionName, "name")
        self.host = config.get(sectionName, "host")
        self.port = int(config.get(sectionName, "port"))
        
    def start(self):
        self.loadconfig()

        self.tcpClient = TcpClient((self.host, self.port), self.dispatcher)

        logicThread = threading.Thread(target=logic_thread_handler,
                name="logic", args=[self.dispatcher])
        cmdloopThread = threading.Thread(target=cmdloop_thread_hendler,
                name="cmdloop", args=[self])
        networkThread = threading.Thread(target=network_thread_handler, 
                name="network", args=[self.tcpClient])

        logicThread.start()
        networkThread.start()
        cmdloopThread.start()

        networkThread.join()
        logicThread.join()
        cmdloopThread.join()

    def preloop(self):
        logger.info(u"*"*80)
        logger.info(u"\n")
        logger.info(u"Welcome to use EasyDeploy controller!")
        logger.info(u"\n")
        logger.info(u"*"*80)

        self.printhelp()
    
    def printhelp(self):
        # 打印命令规则
        print u"Usage:\n"
        h = u"\t 1. ed {cmd} [arg1 [arg2]..]\
              \n\t 2. Print 'exit' to exit"
        print h

    def postloop(self):
        print(u"Bye!")

    ############################################################
    # 具体命令行输入处理 do_xxx
    ############################################################
    def do_ed(self, line):
        if line is None:
            return 

        inputs = line.split()
        cnt = len(inputs)
        if cnt < 1:
            print u"命令无效: \"", line , u"\""
            return 

        # 分割出命令和参数 
        cmd = inputs[0]
        param = {}

        if cnt > 1:
            for i in range(1, cnt):
                param[str(i)] = inputs[i]

        req = pp.request("agent_cmd", {"cmd":cmd, "param":param})
        #print req
        self.tcpClient.send(req)

    def do_ping(self, line):
        print "do_ping"
        req = pp.request("ping", {})
        if req is not None:
            self.tcpClient.send(req)

    def do_exit(self, line):
        import os
        os._exit(0)


if __name__ == "__main__":
    import sys
    sys.path.append("..")
    c = Controller("127.0.0.1", 9999, BaseCommandDispatcher, )
    c.start()

