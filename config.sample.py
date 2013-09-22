import logging
# import logging.config
FORMAT = '%(asctime)-15s - %(message)s'
crawl_log = logging.getLogger('crawl')
crawl_log.setLevel(logging.DEBUG)
formater = logging.Formatter(FORMAT)
ch = logging.StreamHandler()
ch.setFormatter(formater)
crawl_log.addHandler(ch)

HOME_ROOT = '/'

prefix = 'docker_'

use_mysql = True
use_sequence = True

mysql = {
    'host': '127.0.0.1',
    'user': 'lmj',
    'passwd': 'lmj',
    'db': 'docker',
    'port': 49154
}

images = [
    {
        'image_id': 'lupino/ubuntu',
        'ssh_port': '22',
        'server_port': 80,
        'name': 'Ubuntu 12.04',
        'cmd': ['/bin/bash'],
    }
]
