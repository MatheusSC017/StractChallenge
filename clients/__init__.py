import os
from dotenv import load_dotenv
from flask import Flask
from . import routers

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app)
    initialize_routes(app)
    return app


def configure_app(app):
    authorization_token = os.getenv('AUTHORIZATION_TOKEN')

    if not authorization_token:
        raise ValueError("Missing required configuration values")

    app.config.from_mapping(
        AUTHORIZATION_TOKEN=authorization_token
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def initialize_routes(app):
    app.register_blueprint(routers.clients)
