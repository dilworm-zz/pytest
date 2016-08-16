#-*-coding=utf-8-*-
import sys
sys.path.append("..")

from agent import *
from cmddispatch import *
from logger import initlogger
from AgentCmdHandler import AgentCmdHandler 

initlogger("./log/testagent")
a = Agent("127.0.0.1", 9999, AgentCmdHandler)
a.start()


