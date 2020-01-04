from authlib.integrations.flask_client import OAuth
from ..settings import (
    TWITCH_CLIENT_KEY, TWITCH_CLIENT_SECRET
)


def init_oauth(app):
    oauth = OAuth()
    oauth.init_app(app)
    twitch = oauth.register(
        'twitch',
        base_url='https://api.twitch.tv/kraken/',
        request_token_url=None,
        access_token_method='POST',
        access_token_url='https://api.twitch.tv/kraken/oauth2/token',
        authorize_url='https://api.twitch.tv/kraken/oauth2/authorize',
        consumer_key=TWITCH_CLIENT_KEY,
        consumer_secret=TWITCH_CLIENT_SECRET,
        request_token_params={'scope': [
            "user_read", "channel_check_subscription"
        ]}
    )
    app.twitch = twitch
    return app
