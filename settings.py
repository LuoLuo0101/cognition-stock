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

# CREATE DATABASE cognition DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
DB_SETTINGS = {
    "dsn": "mysql+pymysql://root:TingMin1008!@127.0.0.1:3306/cognition?charset=utf8mb4",
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
