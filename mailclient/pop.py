# -*- coding:utf8 -*-

import sys
import poplib

class MailBox:
    connected = False
    def __init__(self, host, port = 110):
        self.o = poplib.POP3(host, port)

    def login(self, user, pwd):
        try:
            self.o.apop(user, pwd)
        except poplib.error_proto as e:
            print(e)
            print("use plain text instead")
            self.o.user(user)
            self.o.pass_(pwd)

    def stat(self):
        ret = self.o.stat()
        print("total %d, size = %s"%(ret[0], ret[1]/1024.0/1024))
        listret = self.o.list()
        response = listret[0]
        octlist = listret[1]
        print(self.o.list(octlist[0]))
        #print (octlist[1], type(octlist[1]))

def main(argv):
    try:
        host, port = "pop3.lkgame.com", 110
        user = "yanggaodi@lkgame.com"
        pwd = "gaodi583"

        lk = MailBox(host, port)
        lk.login(user, pwd)
        lk.stat()

        #
        #print(len(o.list()[1]))
    except poplib.error_proto as e:
        print (dir(e), e)


if __name__ == "__main__":
    main(sys.argv)
