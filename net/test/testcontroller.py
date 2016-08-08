#-*-coding=utf-8-*-
import sys
sys.path.append("..")
from controller import *
from cmddispatch import *

c = Controller("127.0.0.1", 9999, BaseCommandDispatcher)
c.start()



