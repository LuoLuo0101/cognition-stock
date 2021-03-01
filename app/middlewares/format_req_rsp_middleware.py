import time

from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse

from app.utils import regex_match
from app.utils.json_utils import to_json


async def stats_middleware_start_timer(request: Request) -> None:
    if regex_match(request.path, request.app.config.get("MIDDLEWARE_REGEX_WHITE_LIST", [])):
        return
    if request.method == "OPTIONS":
        return
    request.ctx.start_time = time.time()


def process_response(response) -> HTTPResponse:
    if not isinstance(response, HTTPResponse):
        json_response: str = to_json({"code": 200, "message": "请求成功", "data": response})
        response = HTTPResponse(json_response, content_type="application/json")
    return response


async def response_body_middleware(request: Request, response: HTTPResponse):
    if regex_match(request.path, request.app.config.get("MIDDLEWARE_REGEX_WHITE_LIST", [])):
        return
    if request.method == "OPTIONS":
        return
    # 这里需要对某些API做限定，有可能这里有文件请求，不能返回json
    response = process_response(response)
    return response


def install(app: Sanic):
    app.request_middleware.append(stats_middleware_start_timer)
    app.response_middleware.append(response_body_middleware)
