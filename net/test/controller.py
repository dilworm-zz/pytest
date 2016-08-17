#-*-coding=utf-8-*-
import time
import threading
import Queue
import logging
from cmd import Cmd
import sys
from TcpClient import TcpClient
from cmddispatch import *



logger = logging.getLogger("cf")

def network_thread_handler(controller):
    controller.peer.start()

def logic_thread_handler(controller):
    controller.dispatcher.run()

def cmdloop_thread_hendler(controller):
    controller.cmdloop()

class Controller(Cmd):
    def __init__(self, host, port, CmdHandlerClass):
        Cmd.__init__(self)
        self.use_rawinput = False
        self.dispatcher = BaseCommandDispatcher(CmdHandlerClass)
        self.peer = TcpClient((host,port), self.dispatcher)

    def preloop(self):
        logger.info(u"*"*80)
        logger.info(u"\n")
        logger.info(u"Welcome to use EasyDeploy!")
        logger.info(u"\n")
        logger.info(u"*"*80)
    
    def postloop(self):
        print(u"Bye!")

    def do_ed(self, line):
        print "ed"
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
        print req
        self.peer.send(req)

    def do_ping(self, line):
        print "do_ping"
        req = pp.request("ping", {})
        if req is not None:
            self.peer.send(req)

    def do_exit(self, line):
        import os
        os._exit(0)

    def start(self):
        networkThread = threading.Thread(target=network_thread_handler, 
                name="network", args=[self])
        logicThread = threading.Thread(target=logic_thread_handler,
                name="logic", args=[self])
        cmdloopThread = threading.Thread(target=cmdloop_thread_hendler,
                name="cmdloop", args=[self])

        logicThread.start()
        networkThread.start()
        cmdloopThread.start()

        networkThread.join()
        logicThread.join()
        cmdloopThread.join()

if __name__ == "__main__":
    import sys
    sys.path.append("..")
    c = Controller("127.0.0.1", 9999, BaseCommandDispatcher, )
    c.start()

