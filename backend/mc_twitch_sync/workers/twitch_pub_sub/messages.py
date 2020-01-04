import enum
import json
from datetime import datetime, timedelta
from mc_twitch_sync.logger import logger
from mc_twitch_sync.methods.user import (
    get_user_by_ids, create_user,
    update_user, add_expire_days
)
from mc_twitch_sync.settings import (
    ADD_TO_SERVER_REWARD_ID, EXTEND_EXPIRATION_REWARD_ID,
    REWARD_ADD_DAYS_QUANTITY, REWARD_EXTEND_DAYS_QUANTITY
)


class RewardAction(enum.Enum):
    ADD = 'ADD'
    EXTEND = 'EXTEND'


REWARD_ID_TO_ACTION = {
    ADD_TO_SERVER_REWARD_ID: RewardAction.ADD,
    EXTEND_EXPIRATION_REWARD_ID: RewardAction.EXTEND
}


def reward_add(twitch_user):
    user = get_user_by_ids(twitch_id=twitch_user.get('id'))

    if not user:
        now = datetime.now().date()
        logger.info('Adding user')
        create_user(
            twitch_id=twitch_user.get('id'),
            twitch_nickname=twitch_user.get('login'),
            is_member=True,
            expire_date=now + timedelta(days=REWARD_ADD_DAYS_QUANTITY)
        )
        return
    elif not user.is_member:
        logger.info('User is already added but not in membership')
        logger.info('Adding membership to user')
        update_user(
            id=user.id,
            is_member=True
        )
    logger.info('Updating expire days for user')
    logger.info(f'Adding {REWARD_ADD_DAYS_QUANTITY} days')
    add_expire_days(
        id=user.id,
        days=REWARD_ADD_DAYS_QUANTITY
    )


def reward_extend(twitch_user):
    user = get_user_by_ids(twitch_id=twitch_user.get('id'))

    if not user:
        logger.info('Cannot extend reward for non existing user')
        return
    if not user.is_member:
        logger.info('Cannot extend reward without membership')
        return

    logger.info('Updating expire days for user')
    logger.info(f'Adding {REWARD_ADD_DAYS_QUANTITY} days')
    add_expire_days(
        id=user.id,
        days=REWARD_EXTEND_DAYS_QUANTITY
    )


ACTION_TO_FUNCTION = {
    RewardAction.ADD: reward_add,
    RewardAction.EXTEND: reward_extend
}


def on_reward_redeem(ws, data):
    logger.info(f'Got reward redeemed message: {data}')
    redemption = data.get('redemption', '{}')
    twitch_user = redemption.get('user')
    reward = redemption.get('reward')
    logger.info(f'User: {twitch_user}')
    logger.info(f'Reward: {reward}')

    if not twitch_user or not reward:
        logger.info('Failed to process reward message. No user, or reward')
        return

    action = REWARD_ID_TO_ACTION.get(reward.get('id'))

    if not action:
        logger.info('Action for this reward is not found. Skip')
        return

    function = ACTION_TO_FUNCTION.get(action)

    if not function:
        logger.info('Cannot find function for this action, skipping')
        return

    function(twitch_user)
