import pymysql

class DBManager:
    def __init__(self, host, user, password, db, charset='utf8', kind='mysql',
                 port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset
        self.kind = kind
        self.port = port

        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
                                    charset=self.charset, port=self.port)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

    def __del__(self):
        try:
            self.cur.close()
            self.conn.commit()
            self.conn.close()
        except Exception as e:
            print(e)

    def reconnect(self):
        self.cur.close()
        self.conn.close()
        self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db,
                                    charset=self.charset, port=self.port)
        self.cur = self.conn.cursor(pymysql.cursors.DictCursor)

    def execute(self, sql, args={}):
        self.cur.execute(sql, args)

    def execute_one(self, sql, args={}):
        self.cur.execute(sql, args)
        row = self.cur.fetchone()
        return row

    def execute_all(self, sql, args={}):
        self.cur.execute(sql, args)
        row = self.cur.fetchall()
        return row

    def commit(self):
        self.conn.commit()

    def close_db(self):
        self.cur.close()
        self.conn.close()