from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse, text, json

from app import create_app
from app.utils import get_client_ip

app: Sanic = create_app()


@app.route("/ping", methods=["GET"])
async def ping(request: Request) -> HTTPResponse:
    return text("pong")


@app.route("/ip", methods=["GET"])
async def get_my_ip(request: Request) -> HTTPResponse:
    return json({"ip": get_client_ip(request)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
