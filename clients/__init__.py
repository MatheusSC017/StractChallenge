import os
from flask import Flask
from . import routers, api_proxy


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app)
    initialize_routes(app)
    return app


def configure_app(app):
    app.config.from_mapping(
        API_PROXY=api_proxy.SocialMediaProxy('ProcessoSeletivoStract2025')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def initialize_routes(app):
    app.register_blueprint(routers.clients)
