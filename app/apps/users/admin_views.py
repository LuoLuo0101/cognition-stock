from typing import Dict

from sanic import Blueprint
from sanic.request import Request

admin_user_blueprint = Blueprint("user", url_prefix="/user")


# @admin_user_blueprint.post("/register")
# async def register(request: Request) -> Dict:
#     return await services.register(request)
