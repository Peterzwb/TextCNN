# -*- coding:utf-8 -*-
'''
Sqlalchemy数据库访问工具
Created on 2018年7月17日
@author: lianch@ffcs.cn
'''
import traceback

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from Log.logger import run_log as log
from Config.Config import Config

class SqlalchemyUtil(object):
    _db_inst = None
    _db_inst_type = None
    _db_inst_use_pool = False
    conf = Config()
    _db_driver_cfg = {"url": "%s+%s://%s:%s@%s:%s/%s?charset=utf8"
                             % (conf.db_type, conf.db_driver, conf.db_user, conf.db_passwd, conf.db_host, conf.db_port,
                                conf.db_name)}


    @classmethod
    def get_db_inst(cls, useType='cfgurl', dbtype='mysql', user='root', password='root', host='127.0.0.1', port=3306, dbname='ah_q_text_classify', encoding='utf-8'):
        if cls._db_inst is None:
            usePool=cls._db_inst_use_pool
            cls._db_inst_type = useType
            if useType=='cfgurl':
                if usePool:
                    cls._db_inst = create_engine(cls._db_driver_cfg['url'], encoding=encoding)
                else:
                    cls._db_inst = create_engine(cls._db_driver_cfg['url'], encoding=encoding, poolclass=NullPool)
            else:
                cls._db_inst_type = 'default'
                stmt = '%s://%s:%s@%s:%s/%s' % (dbtype, user, password, host, port, dbname)
                if usePool:
                    cls._db_inst = create_engine(stmt, encoding=encoding)
                else:
                    cls._db_inst = create_engine(stmt, encoding=encoding, poolclass=NullPool)
        return cls._db_inst

    @classmethod
    def pandas_read_sql(cls, sql):
        usePool=cls._db_inst_use_pool
        log.info("sql=" + sql)
        if usePool:
            return pd.read_sql(sql, con=cls.get_db_inst())
        else:
            conn = cls.get_db_inst()
            con = conn.connect()
            try:
                with con:
                    return pd.read_sql(sql, con=con)
            except Exception as e:
                log.error("Read from Database fialed: %s"%e)
                traceback.print_exc()
            finally:
                conn.dispose()

    @classmethod
    def pandas_to_sql(cls, pandas_inst, table_name, if_exists='append', index=False, index_label=None, chunksize=1000):
        usePool=cls._db_inst_use_pool
        if usePool:
            pandas_inst.to_sql(table_name,con=cls.get_db_inst(),if_exists=if_exists,index=index,index_label=index_label,chunksize=chunksize)
        else:
            conn = cls.get_db_inst()
            con = conn.connect()
            try:
                with con:
                    pandas_inst.to_sql(table_name,con=con,if_exists=if_exists,index=index,index_label=index_label,chunksize=chunksize)
            except Exception as e:
                log.error("Save to Database fialed: %s"%e)
                traceback.print_exc()
            finally:
                conn.dispose()



if __name__ == '__main__':
    print(SqlalchemyUtil.get_db_inst())