import sentry_sdk
from flask import Flask
from config import config
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mongoengine import MongoEngine
from sentry_sdk.integrations.flask import FlaskIntegration

mongo = MongoEngine()
ma = Marshmallow()
jwt = JWTManager()
cors = CORS()


def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mongo.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    sentry_sdk.init(
        dsn=config[config_name].SENTRY_CDN,
        integrations=[FlaskIntegration()]
    )

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    return app
