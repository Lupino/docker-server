import os
from .drivers import store
from time import time
import config

def create(image_id, server_port, ssh_port):
    image = list(filter(lambda x: x['image_id'] == image_id, config.images))
    if not image:
        return None
    image = image[0]
    cmd = ['docker', 'run', '-d', '-p', '{}:{}'.format(ssh_port, image['ssh_port']),
            '-p', '{}:{}'.format(server_port, image['server_port']),
            image_id]

    for c in image['cmd']:
        cmd.append(c)

    p = os.popen(' '.join(cmd))
    container_id = p.read().strip()
    if container_id:
        now = int(time())
        container_id = store.container.save({
            'container_id': container_id,
            'ssh_port': ssh_port,
            'server_port': server_port,
            'created_at': now,
            'stop_at': now + 60 * 60,
            'image_id': image_id,
            'last_startup': now
        })

    return container_id

def start(container_id):
    cmd = ['docker', 'start', container_id]
    p = os.popen(' '.join(cmd))

    return p.read()

def stop(container_id):
    cmd = ['docker', 'stop', container_id]
    p = os.popen(' '.join(cmd))

    return p.read()

def restart(container_id):
    cmd = ['docker', 'restart', container_id]
    p = os.popen(' '.join(cmd))

    return p.read()
