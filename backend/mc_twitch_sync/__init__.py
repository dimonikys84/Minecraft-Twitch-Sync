# coding=utf-8
import connexion

from raven.contrib.flask import Sentry
from .models import db, migrate
from . import settings
from .clients.oauth import init_oauth


def create_app(_config=settings):
    """
    Создание экземпляра Flask приложения

    :return: объект Flask
    """
    _app = connexion.FlaskApp(__name__, specification_dir='.')

    if _config.RAVEN_DSN:
        Sentry(_app.app, dsn=_config.RAVEN_DSN)

    _app.app.config.from_object(_config)
    _app.add_api('swagger.yml')

    db.init_app(_app.app)
    migrate.init_app(_app.app, db)
    _app.app.db = db
    init_oauth(_app.app)

    return _app
