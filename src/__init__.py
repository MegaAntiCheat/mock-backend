from __future__ import annotations

import os

from flask import Flask
from flask_cors import CORS

from src.api import api
from src.config import Config, DevelopmentConfig


def create_app(config: Config | None = None):
    app = Flask(__name__)
    CORS(app)

    stage = os.environ["stage"]

    if config is None:
        config = DevelopmentConfig if stage == "dev" else Config

    app.config.from_object(config)

    app.logger.info(f"{stage=}")

    app.register_blueprint(api)

    def health_view():
        """Health check endpoint."""
        return "OK", 200

    app.add_url_rule("/health", endpoint="health", view_func=health_view)

    return app
