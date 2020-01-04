from datetime import datetime, timedelta
from ..models import User, db_atomic, db


def get_user_by_id(id):
    return User.query.filter(User.id == id).first()


def get_user_by_ids(twitch_id=None, minecraft_uuid=None):
    query = User.query

    if twitch_id:
        query = query.filter(User.twitch_id == twitch_id)

    if minecraft_uuid:
        query = query.filter(User.minecraft_uuid == minecraft_uuid)

    return query.first()


@db_atomic(db.session)
def create_user(twitch_nickname, twitch_id, minecraft_nickname=None,
                minecraft_uuid=None, is_member=False, expire_date=None):
    new_user = User(
        twitch_nickname=twitch_nickname,
        twitch_id=twitch_id,
        minecraft_nickname=minecraft_nickname,
        minecraft_uuid=minecraft_uuid,
        is_member=is_member,
        expire_date=expire_date
    )
    db.session.add(new_user)
    return new_user


@db_atomic(db.session)
def update_user(id, minecraft_nickname=None, minecraft_uuid=None,
                is_banned=None, expire_date=None, is_member=None):
    user = get_user_by_id(id)

    if minecraft_nickname:
        user.minecraft_nickname = minecraft_nickname

    if minecraft_uuid:
        user.minecraft_uuid = minecraft_uuid

    if is_banned:
        user.is_banned = is_banned

    if expire_date:
        user.expire_date = expire_date

    if is_member:
        user.is_member = is_member

    return user


@db_atomic(db.session)
def add_expire_days(days, id=None, user=None):
    now = datetime.now().date()

    if not user:
        user = get_user_by_id(id)

    if not user:
        return False

    if user.expire_date < now:
        user.expire_date = now + timedelta(days=days)
    else:
        user.expire_date = user.expire_date + timedelta(days=days)

    return True
