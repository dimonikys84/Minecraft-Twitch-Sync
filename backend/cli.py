# coding=utf-8
import fire
import flask_migrate
from mc_twitch_sync import settings, create_app
from mc_twitch_sync.workers.twitch_pub_sub import main as twitch_pub_sub


def run_server():
    """ Запустить dev server """
    app = create_app()
    return app.run(port=settings.PORT, debug=settings.DEBUG)


def migrate_init():
    """ Инициализировать настройку миграций """
    app = create_app()
    with app.app.app_context():
        return flask_migrate.init(settings.MIGRATIONS_DIR)


def migrate(message):
    """ Создать миграцию """
    app = create_app()
    with app.app.app_context():
        return flask_migrate.migrate(settings.MIGRATIONS_DIR, message=message)


def revision(message):
    """ Создать пустую миграцию """
    app = create_app()
    with app.app.app_context():
        return flask_migrate.revision(settings.MIGRATIONS_DIR, message=message)


def upgrade(revision='head'):
    """ Применить миграцию """
    app = create_app()
    with app.app.app_context():
        return flask_migrate.upgrade(settings.MIGRATIONS_DIR, revision)


def downgrade(revision='-1'):
    """ Отменить миграцию """
    app = create_app()
    with app.app.app_context():
        return flask_migrate.downgrade(settings.MIGRATIONS_DIR, revision)


def run_twitch_pub_sub():
    app = create_app()
    with app.app.app_context():
        twitch_pub_sub()


if __name__ == '__main__':
    fire.Fire({
        'run_server': run_server,
        'migrate_init': migrate_init,
        'migrate': migrate,
        'revision': revision,
        'upgrade': upgrade,
        'downgrade': downgrade,
        'twitch_pub_sub': run_twitch_pub_sub
    })
