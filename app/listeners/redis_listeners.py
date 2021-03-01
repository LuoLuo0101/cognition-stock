import aioredis
from sanic import Sanic
from uvloop.loop import Loop


async def setup_redis(app: Sanic, loop: Loop) -> None:
    app.redis = await aioredis.create_redis_pool(
        app.config.REDIS_DSN, encoding="utf8", minsize=5, maxsize=10
    )
    app.redis_bytes = await aioredis.create_redis_pool(
        app.config.REDIS_DSN, minsize=5, maxsize=10
    )


async def close_redis(app: Sanic, loop: Loop) -> None:
    app.redis.close()
    await app.redis.wait_closed()
    app.redis_bytes.close()
    await app.redis_bytes.wait_closed()


def configure_redis_listeners(app: Sanic) -> None:
    app.register_listener(setup_redis, "before_server_start")
    app.register_listener(close_redis, "after_server_stop")
