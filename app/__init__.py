from sanic import Sanic
from sanic_cors import CORS

import settings
from app.blueprints import configure_blueprints
from app.exception_handlers import CustomHandler, configure_exception_handlers
from app.listeners import configure_listeners
from app.middlewares import configure_middlewares


def create_app() -> Sanic:
    error_handler = CustomHandler()
    app: Sanic = Sanic(name="stock", error_handler=error_handler)
    app.config.from_object(settings)  # 导入 Sanic 配置
    configure_blueprints(app)  # 配置蓝图
    configure_listeners(app)  # 配置监听：redis
    configure_middlewares(app)  # 配置中间件
    configure_exception_handlers(app)  # 配置异常处理Handler
    CORS(app, automatic_options=True)
    return app
