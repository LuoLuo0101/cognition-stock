from sanic import Sanic

from app.listeners.redis_listeners import configure_redis_listeners


def configure_listeners(app: Sanic):
    configure_redis_listeners(app)
