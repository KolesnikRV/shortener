from django.conf import settings
import redis


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)


def do():
    redis_instance.set('111', 'hasmter')
