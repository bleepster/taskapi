import os

from flask import Flask

from . import run
from . import config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app_config = config.BaseConfig
    if os.environ.get("FLASK_ENV") == "development":
        app_config = config.DevelopmentConfig
    app.config.from_object(app_config)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(run.bp)

    return app
