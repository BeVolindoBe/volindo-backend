from os import environ

import redis


def get_connector():
    return redis.Redis(
        host=environ.get('CACHE_HOST'),
        port=int(environ.get('CACHE_PORT')),
        db=int(environ.get('CACHE_DB'))
)
