#-*-coding=utf-8-*-
import sys
sys.path.append("..")

from agent import *
from cmddispatch import *
from logger import initlogger
from AgentCmdHandler import AgentCmdHandler 

initlogger("./log/testagent")
a = Agent(AgentCmdHandler)
a.start()


