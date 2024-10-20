import os
from flask import Flask
from flask_cors import CORS
from api.routes.endpoints import routes_blueprint
from db import db, init_app

def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        config = os.getenv("FLASK_ENV")

    if config == "development":
        app.config.from_object("config.DevelopmentConfig")
    elif config == "testing":
        app.config.from_object("config.TestingConfig")
    else:
        app.config.from_object("config.ProductionConfig")

    CORS(app, resources={r'/*': {'origins': '*'}})

    db.init_app(app)

    app.register_blueprint(routes_blueprint)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
