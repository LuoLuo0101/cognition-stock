# -*- coding: utf-8 -*-

# gunicorn -c gunicorn.conf.py manage:app

bind = '0.0.0.0:8000'
workers = 4
worker_class = 'sanic.worker.GunicornWorker'

logconfig_dict = {
    'version':1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    },
    'loggers':{
        'gunicorn.error': {
            'level': 'DEBUG',# 打日志的等级可以换的，下面的同理
            'handlers': ['error_file'], # 对应下面的键
            'propagate': 1,
            'qualname': 'gunicorn.error'
        },
        'gunicorn.access': {
            'level': 'DEBUG',
            'handlers': ['access_file'],
            'propagate': 0,
            'qualname': 'gunicorn.access'
        }
    },
    'handlers':{
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*20,# 打日志的大小，我这种写法是20M
            'backupCount': 1,   # 备份多少份，经过测试，最少也要写1，不然控制不住大小
            'formatter': 'generic',# 对应下面的键
            # 'mode': 'w+',
            'filename': 'gunicorn.error.log'# 打日志的路径
        },
        'access_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024*1024*1024,
            'backupCount': 1,
            'formatter': 'generic',
            'filename': 'gunicorn.access.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'generic',
        },
    },
    'formatters':{
        'generic': {
            'format': '[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s', # 打日志的格式
            'datefmt': '[%Y-%m-%d %H:%M:%S %z]',    # 时间显示方法
            'class': 'logging.Formatter'
        },
        'access': {
            'format': '[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
            'class': 'logging.Formatter'
        }
    }
}