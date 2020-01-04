import websocket
import json
import random
import atexit
import ssl
from mc_twitch_sync.logger import logger
from mc_twitch_sync.settings import TWITCH_WS_HOST, CHANNEL_ID, CHANNEL_TOKEN
from .messages import on_reward_redeem

try:
    import thread
except ImportError:
    import _thread as thread


def on_reconnect(ws, message):
    logger.info('Got reconnect message, exiting...')
    exit()


TYPE_TO_ACTION = {
    'RECONNECT': on_reconnect,
    'reward-redeemed': on_reward_redeem
}


def on_message(ws, message):
    logger.info(f'Got pub sub message: {message}')
    if not isinstance(message, str):
        return
    message = json.loads(message)
    if not message:
        return
    message = message.get('data', {}).get('message', {})
    message = json.loads(message)
    logger.info(f'Parsed message is: {message}')
    message_type = message.get('type')
    logger.info(f'Message type is: {message_type}')
    action = TYPE_TO_ACTION.get(message_type)
    logger.info(f'ACTION IS: {action}')
    if action:
        data = message.get('data', {})
        action(ws, data)


def on_error(ws, error):
    logger.error(f'Got error in pub sub: {error}')
    ws.close()
    exit()


def on_close(ws):
    logger.error('Pub sub connection closed')
    ws.close()
    exit()


def close_before_exit(ws):
    logger.info('Got exit message. Closing ws connection')
    ws.close()
    exit()


def register_to_threads(ws):
    payload = {
        'type': 'LISTEN',
        'nonce': str(random.randint(9999, 99999)),
        'data': {
            'topics': [f'channel-points-channel-v1.{CHANNEL_ID}'],
            'auth_token': CHANNEL_TOKEN,
        }
    }
    logger.info(f'Sending message: {json.dumps(payload)}')
    ws.send(json.dumps(payload))


def main():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(TWITCH_WS_HOST,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = register_to_threads
    atexit.register(close_before_exit, ws=ws)
    ws.run_forever(
        sslopt={"cert_reqs": ssl.CERT_NONE},
        ping_interval=70,
        ping_timeout=10,
    )
