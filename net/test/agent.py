#-*-coding=utf-8-*-
import threading
import asyncore
import logging
from logger import initlogger
from TcpClient import TcpClient
from cmddispatch import *


def network_thread_handler(tcpClient): 
    tcpClient.start()

def logic_thread_handler(dispatcher):
    dispatcher.run()

class Agent:
    def __init__(self, host, port, CmdHandlerClass):
        self.dispatcher = BaseCommandDispatcher(CmdHandlerClass)
        self.tcpClient = TcpClient((host, port), self.dispatcher)

    def start(self):
        cmdDispatchThread = threading.Thread(target=logic_thread_handler, 
                name="CmdDispatch", args=[self.dispatcher])
        tcpclientThread = threading.Thread(target=network_thread_handler, 
                name="Network", args=[self.tcpClient])

        tcpclientThread.start()
        cmdDispatchThread.start()
        tcpclientThread.join()
        cmdDispatchThread.join()


# TODO: Run agent as a deamon service.
if __name__ == "__main__":
    import sys
    sys.path.append("..")

    from AgentCmdHandler import AgentCmdHandler 
    initlogger("./log/client")
    logger = logging.getLogger("cf")

    agent = Agent("127.0.0.1", 9999, AgentCmdHandler)
    agenk.start()

    logger.info("agent exit.")

