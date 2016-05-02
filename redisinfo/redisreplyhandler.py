#-*-coding=utf8-*-
import Queue,threading,time, ConfigParser
import pymssql

CONN_TIMEOUT = 10 # timeout reconnect interval in seconds

class ReplyItem:
    def __init__(self, type, data, time):
        self.type = type
        self.data = data
        self.time = time

class DBConfig:
    pass
class RedisReplyService:
    queue = Queue.Queue()
    is_start = False
    dbconf = DBConfig()
    last_conn_time = 0
    db = None
    
    def __init__(self):
        self.worker = threading.Thread(target = self._run, name = "reply service")

    def _run(self):
        while True:
            try:
                item = self.queue.get(True)
                if item.type == "info":
                    self.handle_info(item.data)
            except Exception as e:
                print e
                print "unknown exception inside RedisReplyHandler.run"

    def load_dbconfig(self, conf_file):
        cfp = ConfigParser.ConfigParser()
        cfp.readfp(open(conf_file))

        self.dbconf.server = cfp.get("db", "server")
        self.dbconf.user = cfp.get("db", "user")
        self.dbconf.pwd = cfp.get("db", "pwd")
        self.dbconf.database = cfp.get("db", "database")
        
        conf = self.dbconf
        print "db config loaded :"
        print "server: ", conf.server
        print "user: ", conf.user
        print "pwd: ", conf.pwd
        print "db: ", conf.database

        return conf

    def add_reply(self, item):
        try:
            print "{0}: add_reply ".format(item.time)
            self.queue.put_nowait(item)
        except Queue.Full:
            print "AddRely failed, queue full."

    def try_connect(self):
        if ((self.db is None) and 
            (time.time() - self.last_conn_time > CONN_TIMEOUT)):
            try:
                print "{0}: connecting database {1}".format(time.time(), self.dbconf.server)
                self.last_conn_time = time.time()
                self.db = pymssql.connect(self.dbconf.server, self.dbconf.user, self.dbconf.pwd, self.dbconf.database, 5,5)
                self.cursor = self.db.cursor()
            except pymssql.OperationalError as e:
                if self.db is not None:
                    self.db.close()
                    self.db = None
                if self.cursor is not None:
                    self.cursor = None
                print e

    def start(self):
        if self.is_start:
            return True

        self.load_dbconfig("./config/dbconfig.ini")

        #self.db = pymssql.connect(cf.server, cf.user, cf.pwd, cf.database)
        self.try_connect()

        self.is_start = True
        self.worker.start()

        return True


    def writeinfo2db(self, info):
        print "writeinfo2db"

        if self.db is None:
            self.try_connect()

        if self.db is not None:
            try:
                #TODO: try using sqlschmay instead of ugly hardcode
                self.cursor.execute("insert into UserProfile1 values(%d, %s, %s)", (123,"hh", "2014-2-2"))
                self.db.commit()
            except pymssql.OperationalError as e:
                print e
                if self.db is not None:
                    self.db.close()
                    self.db = None
                if self.cursor is not None:
                    self.cursor = None

    def handle_info(self, info):
        try:
            self.writeinfo2db(info)
        except IOError as e:
            print e

