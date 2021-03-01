from sanic import Sanic

from app.middlewares import format_req_rsp_middleware, db_session_middleware


def configure_middlewares(app: Sanic) -> None:
    db_session_middleware.install(app)
    format_req_rsp_middleware.install(app)
