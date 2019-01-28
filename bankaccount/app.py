from flask import Flask

from bankaccount.rest import bankaccount
from bankaccount.settings import DevConfig


def create_app(config_object=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    app.register_blueprint(bankaccount.blueprint)
    return app