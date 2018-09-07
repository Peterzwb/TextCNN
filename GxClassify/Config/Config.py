import configparser
import os
from Log.logger import run_log as log

class Config(object):

    cf = configparser.ConfigParser()

    # Config file path
    config_path = os.path.join(os.path.dirname( os.path.abspath( __file__ )),r'compact.conf')


    # DB
    db_type = 'mysql'  # 数据库类型
    db_driver = 'pymsql'
    db_host = '127.0.0.1'
    db_port = '3306'
    db_user = 'root'
    db_passwd = 'root'
    db_name='ah_q_text_classify'

    def __init__(self, config_path=config_path):
        # 初始配置
        self.config_path = config_path
        self.LoadConfig(config_path)

    # 载入配置
    def LoadConfig(self, conf_path):
        log.info('配置文件路径',os.path.abspath(conf_path))
        if self.config_path != conf_path:
            self.config_path = conf_path

        self.cf.read(conf_path)

        # DB
        db_sec = self.cf['db']
        self.db_type = db_sec.get("type", "mysql")
        self.db_driver = db_sec.get("driver","pymysql")
        self.db_host = db_sec.get('host')
        self.db_port = db_sec.get('port', '3306')
        self.db_user = db_sec.get('user')
        self.db_passwd = db_sec.get('passwd')
        self.db_name = db_sec.get('dbname', '')
        self.db_charset = db_sec.get('charset', 'utf8')
        self.db_insertInterval = db_sec.get('insertInterval')
        self.db_verStartTime = db_sec.get('verStartTime')


    # 重载配置文件
    def ReloadConfig(self):
        self.LoadConfig(self.config_path)

    # 输出当前所有配置
    def PrintConfig(self):
        # Config file path
        print('configuration file path : ', self.config_path)
        # Model

        # DB
        print('===DB===')
        print('Database type is [%s]' % self.db_type)
        print('  host = [%s]' % self.db_host)
        print('  port = [%s]' % self.db_port)
        print('  user = [%s]' % self.db_user)
        print('  password = [%s]' % self.db_passwd)
        print('  dbname = [%s]' % self.db_name)
        print('  charset = [%s]' % self.db_charset)

    # 设置指定配置
    def SetSKV(self, secs, opt, kvs):
        if self.cf is not None:
            self.cf.set(secs, opt, kvs)
            self.cf.write(open(self.config_path, 'w'))




if __name__ == '__main__':
    alm_cfg = Config('../config/compact.conf')
    alm_cfg.PrintConfig()
    print(alm_cfg.db_driver)
    print(alm_cfg.config_path)
