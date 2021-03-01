import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__name__))
sys.path.append(os.path.join(BASE_DIR, "app", "apps"))
sys.path.append(os.path.join(BASE_DIR, "app", "libs"))

# 不需要经过中间件的请求
MIDDLEWARE_REGEX_WHITE_LIST = [
    r"^/swagger"    # swagger 的请求
]
WHITE_LIST = ["swagger"] # 不需要JWT登录认证的路径
SIGNATURE_WHITE_LIST = []   # 不需要签名的白名单路径

# CREATE DATABASE stock DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
DB_SETTINGS = {
    "dsn": os.environ.get("MYSQL_DSN", "mysql+pymysql://root:TingMin1008!@127.0.0.1:3306/stock?charset=utf8mb4"),
    "pool_size": 100,
    "pool_recycle": 1200,
    "max_overflow": 10,
}

# redis
REDIS_DSN = os.environ.get("REDIS_DSN", "redis://127.0.0.1:6379/8")

# http request timeout
HTTP_TIMEOUT = 5

# jwt token
JWT_SECRET_KEY = "opserver_secret"     # 加密Key
JWT_TTL = 60 * 60 * 24 * 7          # JWT 7天有效

# swagger
# API_HOST = "api.wangge0101.com"  # API的HOST，如果在本地调试，不用加上这个，要不然不会访问 127.0.0.1
# API_BASEPATH  = "/api"  # API上的BaseURL
API_SCHEMES = ["http", "https"]  # API schemes
API_VERSION = "1.0.0"   # API版本
API_TITLE = "wangge0101 API" # 显示标题
API_DESCRIPTION = "API描述"  # 显示描述
API_TERMS_OF_SERVICE = "我是API服务团队"  # api 服务团队
API_CONTACT_EMAIL = "我是API联系邮箱"  # 联系邮箱
API_LICENSE_NAME = "我是许可证名称"   # 许可证名称
API_LICENSE_URL = "我是许可证链接URL"  # 许可证 URL
API_URI_FILTER = "slash"    # URL是否匹配 "/"
# SWAGGER_UI_CONFIGURATION = {  # 样式展开
#     'validatorUrl': None, # Disable Swagger validator
#     'displayRequestDuration': False,
#     'docExpansion': 'full'
# }

# swagger auth
API_SECURITY = [
    # {"BasicAuth": []},
    # {"ApiKeyAuth": []},
    {"TokenAuth": []},
]
API_SECURITY_DEFINITIONS = {
    # "BasicAuth": {"type": "basic"},
    # "ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "X-API-KEY"},
    "TokenAuth": {"type": "apiKey", "in": "header", "name": "Authorization"},
}

log_config = {
    'version':1,
    'disable_existing_loggers': False,
    'loggers':{
        '': {
            'level': 'INFO',
            'handlers': ['console']
        },
        'sanic.root': {
            'level': 'DEBUG',# 打日志的等级可以换的，下面的同理
            'handlers': ['error_file'], # 对应下面的键
            'propagate': 1,
            'qualname': 'sanic.root'
        },
        'sanic.access': {
            'level': 'DEBUG',
            'handlers': ['access_file'],
            'propagate': 0,
            'qualname': 'sanic.access'
        }
    },
    'handlers':{
        'access_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 20,  # 打日志的大小，我这种写法是20M
            'backupCount': 1,  # 备份多少份，经过测试，最少也要写1，不然控制不住大小
            'formatter': 'generic',  # 对应下面的键
            'filename': 'sanic.access.log'  # 打日志的路径
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 20,   # 打日志的大小，我这种写法是20M
            'backupCount': 1,   # 备份多少份，经过测试，最少也要写1，不然控制不住大小
            'formatter': 'generic',     # 对应下面的键
            'filename': 'sanic.error.log'# 打日志的路径
        },
        'root_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 20,
            'backupCount': 1,
            'formatter': 'generic',
            'filename': 'sanic.root.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'generic',
        },
    },
    'formatters':{
        'generic': {
            'format': '%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: %(request)s %(message)s %(status)d %(byte)d', # 打日志的格式
            'datefmt': '[%Y-%m-%d %H:%M:%S %z]',    # 时间显示方法
            'class': 'logging.Formatter'
        },
        'access': {
            'format': '%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: %(request)s %(message)s %(status)d %(byte)d',
            'class': 'logging.Formatter'
        }
    }
}
