from flask import Flask

from bankaccount.adapters import bankaccount_api
from bankaccount.settings import DevConfig


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(bankaccount_api.blueprint)
    return app