import logging
from raven.handlers.logging import SentryHandler

from .settings import RAVEN_DSN, LOG_LEVEL


def get_logger(name=__name__, file=None, log_level=LOG_LEVEL):
    """
    Create logger instance
    :param name: Logger name
    :param file: filepath to handle logs
    :param log_level: log level
    :return:
    """
    logger = logging.getLogger(name)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    # create file handler which logs even debug messages
    if RAVEN_DSN:
        handler = SentryHandler(RAVEN_DSN)
        handler.setLevel(logging.ERROR)
        logger.addHandler(handler)
    if file:
        fh = logging.FileHandler(file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    logger.setLevel(log_level)
    return logger


logger = get_logger()
