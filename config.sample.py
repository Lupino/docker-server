import logging
FORMAT = '%(asctime)-15s - %(message)s'
docker_log = logging.getLogger('docker')
docker_log.setLevel(logging.DEBUG)
formater = logging.Formatter(FORMAT)
ch = logging.StreamHandler()
ch.setFormatter(formater)
docker_log.addHandler(ch)

FORMAT = '%(asctime)-15s - %(message)s'
lee_log = logging.getLogger('lee')
lee_log.setLevel(logging.DEBUG)
formater = logging.Formatter(FORMAT)
ch = logging.StreamHandler()
ch.setFormatter(formater)
lee_log.addHandler(ch)

HOME_ROOT = '/'

prefix = 'docker_'

# database settings
drivers = {
    'path':'sqlite://run/%s/data.db'%prefix,
    # 'path':'mysql://127.0.0.1:3306?db=&user=&passwd=',
    'memcached': [],
    'lru_cache': False,
    'cache_timeout': 0
}

images = [
    {
        'image_id': 'lupino/ubuntu',
        'ssh_port': '22',
        'server_port': 80,
        'name': 'Ubuntu 12.04',
        'cmd': ['/bin/bash', '/src/startup.sh'],
    },
    {
        'image_id': 'lupino/lnmp',
        'ssh_port': '22',
        'server_port': 80,
        'name': 'Ubuntu 12.04 lnmp',
        'cmd': ['/usr/local/bin/run'],
    }
]
