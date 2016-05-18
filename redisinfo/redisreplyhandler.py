#-*-coding=utf8-*-
import Queue,threading,time, ConfigParser
import pymssql

CONN_TIMEOUT = 10 # timeout reconnect interval, in seconds

class ReplyItem:
    def __init__(self, redisid, redisname, type, data, time):
        self.rid = redisid
        self.rname = redisname
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
    cursor = None
    def __init__(self):
        self.worker = threading.Thread(target = self._run, name = "reply service")

    def _run(self):
        while True:
            try:
                item = self.queue.get(True)
                if item.type == "info":
                    self.handle_info(item.rid,item.rname, item.data)
            except Exception as e:
                print e
                print "Error: unknown exception inside RedisReplyHandler.run"

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
            #print "{0}: add_reply ".format(item.time)
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


    # Extra from redis info and map to database table
    class __redisinfo_record:
        _colnames = ["redis_id", "redisdb_name", "host", "port", "pid",
                     "connected_clients", "keys", "keys_expires", "used_memory_human", "used_memory_peak_human",
                     "mem_fragmentation_ratio", "instantaneous_ops_per_sec", "hit_rate", "used_memory", "used_memory_rss",
                     "used_memory_peak", "used_memory_lua", "expired_keys", "evicted_keys", "keyspace_hist",
                     "keyspace_misses", "total_commands_processed", "pubsub_channels", "pubsub_patterns", "role",
                     "connected_slaves", "rdb_bgsave_in_progress", "rdb_last_save_status", "rdb_last_bgsave_time_sec", "aof_enabled",
                     "confile_file", "version", "uptime_in_seconds",]
        _cols = dict(
                redis_id=1,
                redisdb_name="",
                host="",
                port=0,
                pid=0,

                connected_clients=0,
                keys=0,
                keys_expires=0,
                used_memory_human="",
                used_memory_peak_human=0.0,

                mem_fragmentation_ratio=0.0,
                instantaneous_ops_per_sec=0,
                hit_rate=0.0,
                used_memory=0,
                used_memory_rss=0,

                used_memory_peak=0,
                used_memory_lua=0,
                expired_keys=0,
                evicted_keys=0,
                keyspace_hist=0,

                keyspace_misses=0,
                total_commands_processed=0,
                pubsub_channels=0,
                pubsub_patterns=0,
                role="",

                connected_slaves=0,
                rdb_bgsave_in_progress=0,
                rdb_last_save_status="",
                rdb_last_bgsave_time_sec=0,
                aof_enabled=0,

                #confile_file="",
                version="",
                uptime_in_seconds="",
                )

        def colsnames(self):
            return self._cols.iterkeys()

        def values(self):
            return self._cols.itervalues()

        def len(self):
            return len(self._cols)

        def __init__(self, rid, rname, info):
            lines = info.splitlines()
            self._cols["redis_id"] = rid
            self._cols["redisdb_name"] = rname
            for l in lines:
                kv = l.split(":")
                if len(kv) == 2:
                    if kv[0] in self._cols: # check columns that we interested in
                        self._cols[kv[0]] = kv[1]
                        #print 'good'
                        #print k[0],"=", self._cols[kv[0]]

    def writeinfo2db(self, rid, rname, info):
        record = self.__redisinfo_record(rid, rname, info)
        #print "{0}: writeinfo2db ".format(time.time())

        if self.db is None:
            self.try_connect()
        
        if self.db is not None:
            try:
                #TODO: try using sqlschmay instead of this ugly hardcode
                d = dict(user_id=123,name="123",birthdate="2012-1-1")
                #self.cursor.execute("insert into RedisInfo values(")
                #self.cursor.execute("""insert into test values(id, name)""", d)
                #l = dict()[123,"1234"]
                #self.cursor.callproc("inserttest",d)
                p =[record._cols[x] for x in record._colnames]
                #for n in record._colnames: p.append(record._cols[n])

                print p
                self.cursor.callproc("GSP_InsertRedisInfo", p)
                

                self.db.commit()
            except pymssql.OperationalError as e:
                print e
                if self.db is not None:
                    self.db.close()
                    self.db = None
                if self.cursor is not None:
                    self.cursor = None
            except pymssql.Error as e:
                print e

    def handle_info(self, rid, rname, info):
        try:
            self.writeinfo2db(rid, rname, info)
        except IOError as e:
            print e

