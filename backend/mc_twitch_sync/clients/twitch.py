import requests
import backoff
from flask import url_for
from urllib.parse import urlencode
from ..settings import (
    TWITCH_CLIENT_KEY, TWITCH_CLIENT_SECRET,
    CHANNEL_ID, CHANNEL_TOKEN
)


def _build_request_headers(token):
    return {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': TWITCH_CLIENT_KEY,
        'Authorization': f'OAuth {token}'
    }


@backoff.on_exception(backoff.expo, requests.ConnectionError)
def get_client_token():
    params = {
        'client_id': TWITCH_CLIENT_KEY,
        'client_secret': TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'channel_check_subscription channel:read:redemptions'
    }
    url = 'https://id.twitch.tv/oauth2/token?' + urlencode(params)
    response = requests.post(url)
    response.raise_for_status()
    return response.json()


def exchange_code_to_token(code):
    params = {
        'client_id': TWITCH_CLIENT_KEY,
        'client_secret': TWITCH_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'scope': 'user_read',
        'redirect_uri': url_for('/api/v1.mc_twitch_sync_views_callback',
                                _external=True)
    }
    url = 'https://id.twitch.tv/oauth2/token?' + urlencode(params)
    response = requests.post(url)
    response.raise_for_status()
    return response.json()


def refresh_token(refresh_token):
    params = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': TWITCH_CLIENT_KEY,
        'client_secret': TWITCH_CLIENT_SECRET
    }
    url = 'https://id.twitch.tv/oauth2/token?' + urlencode(params)
    response = requests.post(url)
    response.raise_for_status()
    return response.json()


def get_user(token):
    url = 'https://api.twitch.tv/kraken/user'
    response = requests.get(url, headers=_build_request_headers(token))
    print(response.content)
    response.raise_for_status()
    return response.json()


def is_user_subscribed(twitch_id):
    url = f'https://api.twitch.tv/kraken/channels/{CHANNEL_ID}/subscriptions/{twitch_id}'
    response = requests.get(url, headers=_build_request_headers(CHANNEL_TOKEN))
    json = response.json()
    return json.get('user')
