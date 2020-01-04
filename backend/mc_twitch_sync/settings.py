from envparse import env
import logging

env.read_envfile()

ENV = env('ENV', 'development')
DEBUG = env('DEBUG', True)
PORT = env('PORT', 80, cast=int)
JSON_AS_ASCII = env('JSON_AS_ASCII', False)
SERVER_NAME = env('SERVER_NAME', 'localhost:8000')
SECRET_KEY = env('SECRET_KEY')

STATE_SECRET = env('STATE_SECRET', '1234')

RAVEN_DSN = env('RAVEN_DSN', None)
LOG_LEVEL = env('LOG_LEVEL', logging.DEBUG)

MIGRATIONS_DIR = env('MIGRATIONS_DIR', 'mc_twitch_sync/migrations')
SQLALCHEMY_DATABASE_URI = env('DB_DSN', 'sqlite://')
SQLALCHEMY_TRACK_MODIFICATIONS = env('DB_TRACK_MODIFCATIONS', False)

TWITCH_CLIENT_KEY = env('TWITCH_CLIENT_KEY')
TWITCH_CLIENT_SECRET = env('TWITCH_CLIENT_SECRET')

TWITCH_WS_HOST = env('TWITCH_WS_HOST')

ADD_TO_SERVER_REWARD_ID = env('ADD_TO_SERVER_REWARD_ID')
EXTEND_EXPIRATION_REWARD_ID = env('EXTEND_EXPIRATION_REWARD_ID')

CHANNEL_ID = env('CHANNEL_ID')
CHANNEL_TOKEN = env('CHANNEL_TOKEN')

REWARD_ADD_DAYS_QUANTITY = env('REWARD_ADD_DAYS_QUANTITY', cast=int,
                               default=14)
REWARD_EXTEND_DAYS_QUANTITY = env('REWARD_EXTEND_DAYS_QUANTITY', cast=int,
                                  default=7)
