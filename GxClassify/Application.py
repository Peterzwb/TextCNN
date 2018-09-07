import time
from multiprocessing import Lock
import os
from Log.logger import run_log as log
from Util.sqlUtil.sqlalchemyUtil import SqlalchemyUtil


class Application:

    all_data =None

    init_data = False
    init_model = False
    lastTime = None
    updataTime = 20

    # 工程根目录
    base_dir = os.path.dirname( os.path.abspath( __file__ ) )

    def __init__(self):
        pass

    @classmethod
    def clean(cls):

        cls.all_data = None

        cls.init_data = False
        cls.last_time = None


mutex = Lock()
# do something

def tasker():

    # log.debug('开启互斥锁')

    mutex.acquire()
    try:
        log.info('Application更新时间：%s'%Application.lastTime)
        if Application.lastTime != None:
            if int(time.time()) - int(Application.lastTime) < Application.updataTime:
                log.info('---无需更新数据---')
                return
        initData()
        Application.lastTime = time.time()
        Application.init_data = True
        Application.init_model = True
    finally:
        mutex.release()
        log.debug('释放互斥锁')

def initData():

    que_label =None
    que_nolabel = None



    sql = 'select * from gx_regular_label'
    que_label = SqlalchemyUtil.pandas_read_sql(sql=sql)

    log.info('数据已经更新')


    sql = 'select * from gx_regular_nolabel'
    que_nolabel = SqlalchemyUtil.pandas_read_sql(sql=sql)
    
    


    Application.all_data = {'gx_regular_label':que_label,'gx_regular_nolabel':que_nolabel}


    
if __name__ == '__main__':

    tasker()
    data = Application.all_data['q_original_label']

