# Base settings
prefix = 'docker_'
# database settings
use_mysql = False

# if you use sqlite3 set the store_path
store_path = 'run/%s/cache.db'%prefix

# if you use mysql set mysql
# mysql = {
#     'host': '127.0.0.1',
#     'user': 'lmj',
#     'passwd': 'lmj',
#     'db': 'docker',
#     'port': 3306
# }

# memcached
# memcached = ['127.0.0.1:11211']
# cache_timeout = 500
# lru_cache = False

images = [
    {
        'image_id': 'lupino/ubuntu',
        'ssh_port': '22',
        'server_port': 80,
        'name': 'Ubuntu 12.04',
        'cmd': ['/bin/bash'],
    }
]

HOME_ROOT = '/'

try:
    from config import *
except ImportError:
    try:
        from settings import *
    except ImportError:
        pass
