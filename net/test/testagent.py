#-*-coding=utf-8-*-
import sys
sys.path.append("..")

from agent import *
from cmddispatch import *
from logger import initlogger

initlogger("./log/testagent")
a = Agent("127.0.0.1", 9999, BaseCommandDispatcher)
a.start()


