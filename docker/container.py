import os
from .drivers import store
from time import time

def create(image, server_port, ssh_port):
    cmd = ['docker', 'run', '-d', '-p', '%s:22'%ssh_port, '%s:80'%server_port,
            image]

    p = os.popen(' '.join(cmd))

    container_id = p.read().strip()
    now = int(time())
    container_id = store.container.save({
        'container_id': container_id,
        'ssh_port': ssh_port,
        'server_port': server_port,
        'created_at': now
        'stop_at': now + 60 * 60
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
