# -*- coding:utf-8 -*-
'''
日志工具，基于logbook
Created on 2018年7月18日
@author: lianch@ffcs.cn
'''
import os
import logbook
from logbook import Logger, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler

def log_type(record, handler):
    log = "[{date}] [{level}] [{filename}:{lineno}] [{func_name}] {msg}".format(
        date = record.time,                              # 日志时间
        level = record.level_name,                       # 日志等级
        filename = os.path.split(record.filename)[-1],   # 文件名
        func_name = record.func_name,                    # 函数名
        lineno = record.lineno,                          # 行号
        msg = record.message                             # 日志内容
    )
    return log

# 日志名称
LOG_NAME = 'ai_csr'
# 日志等级
LOG_LEVEL = logbook.base.INFO
# 日志存放路径
# LOG_DIR = os.path.join(os.path.dirname(__file__), '/logs')
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath( __file__ )),r'logs')
#print("LOG_DIR="+LOG_DIR)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
# 日志打印到控制台
log_std = ColorizedStderrHandler(bubble=True, level=LOG_LEVEL)
log_std.formatter = log_type
# 日志打印到文件
log_file = TimedRotatingFileHandler(
    os.path.join(LOG_DIR, '%s.log' % LOG_NAME),date_format='%Y-%m-%d', bubble=True, level=LOG_LEVEL, encoding='utf-8')
log_file.formatter = log_type

# 脚本日志
run_log = Logger(LOG_NAME)
def init_logger():
    logbook.set_datetime_format("local")
    run_log.handlers = []
    run_log.handlers.append(log_file)
    run_log.handlers.append(log_std)

# 实例化，默认调用
logger = init_logger()