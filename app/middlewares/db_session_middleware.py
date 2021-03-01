# -*- coding: utf-8 -*-

from sanic import Sanic
from sanic.request import Request

from app.database import Session
from app.utils import regex_match


def denied_middleware_append(request: Request):
    return bool(regex_match(request.path, request.app.config.get("MIDDLEWARE_REGEX_WHITE_LIST", [])))


async def create_db_session_middleware(request: Request) -> None:
    if denied_middleware_append(request=request):
        return
    Session()


async def remove_db_session_middleware(request: Request, response) -> None:
    if denied_middleware_append(request=request):
        return
    Session.remove()


def install(app: Sanic) -> None:
    app.request_middleware.append(create_db_session_middleware)
    app.response_middleware.append(remove_db_session_middleware)
