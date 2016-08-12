#-*-coding=utf-8-*-
import sys
sys.path.append("..")

def logic_thread_handler(dispatcher):
    dispatcher.run()

def network_thread_handler(server):
    server.run_forever()

if __name__ == "__main__":
    import logger
    #import asyncore
    from TcpServer import TcpServer
    from logger import initlogger
    from cmddispatch import *
    from DeployServerCmdHandler import DeployServerCmdHandler

    initlogger("./log/server")

    
    dispatcher = BaseCommandDispatcher(DeployServerCmdHandler)
    cmdDispatchThread = threading.Thread(target=logic_thread_handler, 
            name="CmdDispatch", args=[dispatcher])
    dpServer= TcpServer(('127.0.0.1', 9999))
    tcpServerThread = threading.Thread(target=network_thread_handler, 
            name="Network", args=[dpServer])
    
    cmdDispatchThread.start()
    tcpServerThread.start()
    cmdDispatchThread.join()
    tcpServerThread.join()

    
