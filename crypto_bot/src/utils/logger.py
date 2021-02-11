import logging

import src.settings as settings


def init_logger():
    logging.basicConfig(
        filename=settings.Paths.LOGGER,
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
    )


def get_logger():
    return logging.getLogger('crypto_bot')
