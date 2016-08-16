#-*-coding=utf-8-*-
import sys
sys.path.append("..")
from controller import *
from cmddispatch import *
from logger import initlogger
from ControllerCmdHandler import ControllerCmdHandler 

initlogger("./log/testcontroller")
c = Controller("127.0.0.1", 9999, ControllerCmdHandler)
c.start()



