from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
from flask_mail import Mail


mail = Mail()
db = SQLAlchemy(session_options={"autoflush": False})
ma = Marshmallow()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()


def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    sentry_sdk.init(
        dsn=config[config_name].SENTRY_CDN,
        integrations=[FlaskIntegration()]
    )

    from .tools.custom_url_path_params import SignedIntConverter
    app.url_map.converters['signed_int'] = SignedIntConverter

    from .modules import api_blueprints
    for api_blueprint in api_blueprints:
        app.register_blueprint(api_blueprint, url_prefix="/api")
    return app
