from flask import Blueprint

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

from . import diagnosis  # noqa: E402, F401
