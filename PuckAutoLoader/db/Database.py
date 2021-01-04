from PuckAutoLoader.utils.DBManager import DBManager
from PuckAutoLoader.utils.config_parser import ConfigParser

config = ConfigParser('utils/config.ini').get_config()

DATABASES = {
    'default': {
        'host': config['DATABASE']['Host'],
        'user': config['DATABASE']['User'],
        'password': config['DATABASE']['Password'],
        'db': config['DATABASE']['Db'],
        'charset': config['DATABASE']['Charset'],
        'kind': config['DATABASE']['Kind'],
        'port': int(config['DATABASE']['Port'])
    }
}

class Database:
    def __init__(self):
        self.db = DBManager(host=DATABASES['default']['host'], user=DATABASES['default']['user'],
                            password=DATABASES['default']['password'], db=DATABASES['default']['db'],
                            kind=DATABASES['default']['kind'], port=DATABASES['default']['port'],
                            charset=DATABASES['default']['charset'])

        print("access database")

    def reconnect(self):
        self.db.reconnect()
