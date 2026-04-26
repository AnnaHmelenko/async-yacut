from random import choices
from string import ascii_letters, digits

from yacut.models import URLMap


SHORT_ID_LENGTH = 6
MAX_CUSTOM_ID_LENGTH = 16
SYMBOLS = ascii_letters + digits


def get_unique_short_id():
    while True:
        short_id = ''.join(choices(SYMBOLS, k=SHORT_ID_LENGTH))

        if URLMap.query.filter_by(short=short_id).first() is None:
            return short_id


def is_valid_short_id(short_id):
    return (
        len(short_id) <= MAX_CUSTOM_ID_LENGTH
        and all(symbol in SYMBOLS for symbol in short_id)
    )
