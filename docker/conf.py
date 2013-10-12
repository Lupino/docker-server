# Base settings
prefix = 'docker_'

# database settings
drivers = {
    'path':'sqlite://run/%s/data.db'%prefix,
    # 'path':'mysql://127.0.0.1:3306?db=&user=&passwd=',
    'memcached': [],
    'lru_cache': False,
    'cache_timeout': 0
}

images = []

HOME_ROOT = '/'

try:
    from config import *
except ImportError:
    pass
