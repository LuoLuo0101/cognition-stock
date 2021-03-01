from sanic_openapi import doc


class BaseRsp(object):
    code = doc.Integer(description="响应码", choices=[200])
    message = doc.Integer(description="响应描述信息", choices=["请求成功"])
