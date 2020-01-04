from datetime import datetime
from flask import (
    session, redirect,
    url_for,
)
from .settings import (
    TWITCH_CLIENT_KEY, STATE_SECRET
)
from .clients.twitch import (
    exchange_code_to_token, get_user,
    is_user_subscribed
)
from .clients.minecraft import search_minecraft_profile
from .methods.user import (
    get_user_by_ids, create_user,
    update_user
)
from .decorators import requires_auth
from urllib.parse import urlencode
import jwt


def healthcheck():
    return 'OK'


def callback(code):
    token = exchange_code_to_token(code)
    twitch_user = get_user(token.get('access_token'))
    session['user'] = twitch_user
    user = get_user_by_ids(twitch_id=twitch_user.get('_id'))
    if not user:
        create_user(
            twitch_id=twitch_user.get('_id'),
            twitch_nickname=twitch_user.get('name'),
        )

    return redirect('/')


def login():
    params = {
        'client_id': TWITCH_CLIENT_KEY,
        'redirect_uri': url_for(
            '/api/v1.mc_twitch_sync_views_callback',
            _external=True
        ),
        'response_type': 'code',
        'scope': 'user_read'
    }
    url = 'https://id.twitch.tv/oauth2/authorize?' + urlencode(params)
    return redirect(url)


@requires_auth
def logout():
    session.clear()
    return redirect('/login')


@requires_auth
def session_info():
    twitch_user = session.get('user')
    user = get_user_by_ids(twitch_id=twitch_user.get('_id'))
    if user:
        return {
            'twitch_nickname': user.twitch_nickname,
            'twitch_id': user.twitch_id,
            'minecraft_nickname': user.minecraft_nickname,
            'minecraft_uuid': user.minecraft_uuid,
            'expire_date': user.expire_date,
            'is_member': user.is_member,
            'is_banned': user.is_banned
        }
    return session.get('user')


def is_allowed(username, uuid):
    # print('Uuid: ', uuid)
    now = datetime.now().date()
    user = get_user_by_ids(minecraft_uuid=uuid.replace('-', ''))
    # print('User: ', user.minecraft_uuid)
    if not user:
        link = url_for(
            '/api/v1.mc_twitch_sync_views_login',
            _external=True
        )
        return {
            'is_allowed': False,
            'message': f'Необходимо зарегестрироваться: \n {link}',
        }

    if is_user_subscribed(twitch_id=user.twitch_id):
        return {
            'is_allowed': True,
            'message': 'Привет, дружище!'
        }

    if user.is_member and user.expire_date < now:
        return {
            'is_allowed': False,
            'message': 'Необходимо продлить посещение, используя channel '
                       'points'
        }

    if user.is_member and user.expire_date > now:
        return {
            'is_allowed': True,
            'message': 'Проходи, дружище!'
        }

    return {
        'is_allowed': False,
        'message': 'Тебе необходимо приобрести членство FymsaTown, '
                   'чтобы попасть на сервер.',
    }


@requires_auth
def link(body):
    twitch_user = session.get('user')
    user = get_user_by_ids(twitch_id=twitch_user.get('_id'))

    if not user:
        create_user(
            twitch_id=twitch_user.get('_id'),
            twitch_nickname=twitch_user.get('name'),
            minecraft_nickname=body.get('nickname'),
            minecraft_uuid=body.get('uuid')
        )
        return {"status": "ok"}

    update_user(
        id=user.id,
        minecraft_nickname=body.get('nickname'),
        minecraft_uuid=body.get('uuid')
    )
    return {"status": "ok"}


@requires_auth
def search(nickname):
    return search_minecraft_profile(nickname)


def mc_add(token, username):
    pass


def mc_extend(token, username):
    pass


def mc_ban(token, username):
    pass


def mc_unban(token, username):
    pass
