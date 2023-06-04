import os

from datetime import timedelta

ACCESS_TOKEN_LIFETIME = timedelta(
    seconds=int(os.getenv('ACCESS_TOKEN_LIFETIME')))
REFRESH_TOKEN_LIFETIME = timedelta(
    seconds=int(os.getenv('REFRESH_TOKEN_LIFETIME')))

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': ACCESS_TOKEN_LIFETIME,
    'REFRESH_TOKEN_LIFETIME': REFRESH_TOKEN_LIFETIME,
}
