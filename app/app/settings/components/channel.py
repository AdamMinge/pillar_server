from environ import Env

env = Env()
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": env.str('REDIS_HOST'),
        },
    },
}
