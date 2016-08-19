#-*-coding=utf-8-*-
import cmddispatch
import logging
import packetparser as pp
import time
logger = logging.getLogger("cf")


# 管理客户端连接
class ClientManager:
    def __init__(self):
        self.agents = {}
        self.controllers = {}
        pass

    def AddClient(self, type, name, conn): 
        if type == "agent":
            assert(conn not in self.agents)
            self.agents[conn] = (name, type, time.time())
        elif type == "controller":
            assert(conn not in self.controllers)
            self.controllers[conn] = (name, type, time.time())

    def RemoveClient(self, conn):
        name, type, remainCnt = None, None, None
        if conn in self.agents:
            name = self.agents[conn][0]
            type = self.agents[conn][1]
            remainCnt = len(self.agents) - 1
            del self.agents[conn]
        elif conn in self.controllers:
            name = self.controllers[conn][0] 
            type = self.controllers[conn][1]
            remainCnt = len(self.controllers) - 1
            del self.controllers[conn] 
        return name, type, remainCnt

    def GetAgents(self):
        return self.agents

    def GetControlers(self):
        return self.controllers

# 业务处理类
class DeployServerCmdHandler(cmddispatch.BaseCommandHandler):
    def __init__(self, owner):
        cmddispatch.BaseCommandHandler.__init__(self, owner)
        self.clientManager = ClientManager()
        self.clients = {}

    def _do_pong(self, conn, data):
        logger.debug("recv pong")

    def _do_login(self, conn, data):
        type, name = data["type"], data["name"]
        self.clientManager.AddClient(type, name, conn)

        logger.info(u"收到 {0} 注册: {1}".format(type, name))

        if type == "agent":
            logger.info(u"当前总 {0} 数为{1}".format(type, len(self.clientManager.GetAgents())))
        elif type == "controller":
            logger.info(u"当前总 {0} 数为{1}".format(type, len(self.clientManager.GetControlers())))


    ########################################################
    #
    # 转发controler的命令给所有agent
    def _do_agent_cmd(self, peer, data):
        cmd, param = data["cmd"], data["param"]
        logger.debug(u"_do_agent_cmd :'{}' ".format(cmd))
        #print cmd, param
        a = self.clientManager.GetAgents()
        for conn, _ in a.items():
            req = pp.request(cmd, param)
            #print req
            conn.send(req)
            

    # agent 执行命令后的返回
    def _do_agent_response(self, peer, data):
        logger.debug(u"_do_agent_response")
        for n, p in self.clientManager.controllers():
            p.send(data)
    
    def OnConnectClose(self, conn):
        logger.debug("DeployServerCmdHandler OnConnectClose")
        ret = self.clientManager.RemoveClient(conn)
        if ret is not None:
            logger.info(u"'{}'断开连接".format(ret[0]))
            logger.info(u"当前总 {0} 数为{1}".format(ret[1], ret[2]))

