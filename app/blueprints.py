from sanic import Sanic
from sanic_openapi import swagger_blueprint

from users.views import user_blueprint


def configure_blueprints(app: Sanic):
    app.blueprint(swagger_blueprint)
    app.blueprint(user_blueprint)
