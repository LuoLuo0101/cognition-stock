import functools

from sanic.request import Request

from app.exceptions import InvalidSignature
from app.utils import md5


def generate_signature(content):
    """
    制作签名
    """
    return md5(content=content)


def signature():
    """
    验证签名，可以多加一步相当于保险，也可以当做第二种验证登录的方式
    """

    def outer(func):
        @functools.wraps(func)
        async def inner(request: Request, *args, **kwargs):
            # 有可能需要再加一个参数APIKey，signature = md5(APIKey + Secret + Timestamp)
            timestamp: str = request.headers.get("Timestamp")
            signature: str = request.headers.get("Signature")
            if timestamp is None or signature is None:
                raise InvalidSignature()

            expect_signature: str = generate_signature(timestamp)
            if signature != expect_signature:
                raise InvalidSignature()
            return await func(request, *args, **kwargs)

        return inner

    return outer
