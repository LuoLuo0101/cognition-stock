from sanic.response import json, HTTPResponse


class BException(Exception):
    @staticmethod
    def handle(request, exception):
        raise NotImplementedError


class BadRequest(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 400, "message": "Bad Request"}, status=400)


class SnmpError(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 400, "message": "snmp error"}, status=400)


class DeviceMacAddrInconsistency(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 400, "message": "该IP对应设备与要更新设备Mac地址不一致"}, status=400)


class NoModelError(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 400, "message": "该设备未设置品牌"}, status=400)


class NoScriptError(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 400, "message": "该型号未设置脚本"}, status=400)


class NoOpCodeError(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 400, "message": "该OpCode功能未适配"}, status=400)


class InvalidCode(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 400, "message": "invalid code"}, status=400)


class ParameterIsIncompleted(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 400009, "message": "parameter is incompleted"}, status=400)


class NotMatch(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 48640, "message": "两次输入密码不一致"}, status=400)


class UserExist(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 48641, "message": "用户已存在"}, status=400)


class ObjNotFound(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 46100, "message": "该对象不存在"}, status=400)


class AuthenticationFailed(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 401, "message": "认证失败，账号密码错误"}, status=401)


class InvalidSignature(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 401, "message": "无效的签名"}, status=401)


class NoToken(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 401, "message": "用户鉴权失败，请重新登陆"}, status=401)


class InvalidToken(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 401, "message": "用户鉴权无效"}, status=401)


class PermissionDenied(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 403, "message": "访问权限拒绝"}, status=403)


class WechatPaymentFailed(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 500, "message": "微信支付失败"}, status=500)


class SendMessageFailed(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 500, "message": "发送消息失败"}, status=500)


class UploadFileFailed(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 500, "message": "上传文件失败"}, status=500)


class SendSMSFailed(BException):
    @staticmethod
    def handle(request, exception) -> HTTPResponse:
        return json({"code": 500, "message": "发送短信失败"}, status=500)
