from flask import Flask

from .config import Config
from .db import init_db
from .routes import main_blueprint
from .api import api_blueprint


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)

    return app
