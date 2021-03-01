from traceback import format_exc
from typing import Dict

from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.handlers import ErrorHandler
from sanic.log import logger
from sanic.request import Request
from sanic.response import HTTPResponse, json
from app import exceptions
from jwt import PyJWTError


class CustomHandler(ErrorHandler):
    def response(self, request, exception):
        self.log(format_exc())
        return super().response(request, exception)

    def log(self, message, level="error"):
        getattr(logger, level)(message)

    def default(self, request: Request, exception: Exception) -> HTTPResponse:
        if issubclass(type(exception), SanicException):
            status: int = getattr(exception, "status_code")
            body: Dict = {"code": status, "message": "Error: {}".format(exception)}
            return json(body, status=status)
        return json({"code": 500, "message": "内部服务器错误"}, status=500)


def handle_jwt_error(request, exception) -> HTTPResponse:
    return json({"code": 401, "message": "用户鉴权失败，请重新登陆"}, status=401)


def configure_exception_handlers(app: Sanic) -> None:
    sub_class = exceptions.BException
    for exception in dir(exceptions):
        cls = getattr(exceptions, exception)
        try:
            if issubclass(cls, sub_class) and cls != sub_class:
                app.error_handler.add(cls, cls.handle)
        except Exception as e:
            pass

    # JWT 异常
    app.error_handler.add(PyJWTError, handle_jwt_error)
