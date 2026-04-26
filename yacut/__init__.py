from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from yacut import api_views, views
    from yacut.error_handlers import register_error_handlers

    app.register_blueprint(views.bp)
    app.register_blueprint(api_views.bp)

    register_error_handlers(app)

    return app


app = create_app()
