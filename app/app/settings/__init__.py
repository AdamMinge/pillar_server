from os import environ
from split_settings.tools import optional, include

base_settings = [
    'environments/{}.py'.format(environ.get("DJANGO_ENV", "development")),
    optional('environments/local.py'),

    'components/common.py',
    'components/storage.py',
    'components/database.py',
    'components/documentation.py',
    'components/email.py',
    'components/cache.py',
    'components/channel.py',
]

include(*base_settings)
