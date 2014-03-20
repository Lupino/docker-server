import os
from . import models
from time import time

def create(image):
    cmd = ['docker', 'run', '-d']

    port = models.seq.next('container_export_port')
    if port < 49153:
        port = 49152 + port
        models.seq.save('container_export_port', port)

    info = {}
    if image.get('ssh_port'):
        info['ssh_port'] = port
        cmd.extend(['-p', '{}:{}'.format(port, image['ssh_port'])])
        port = 0

    if image.get('server_port'):
        if not port:
            port = models.seq.next('container_export_port')
        info['server_port'] = port
        cmd.extend(['-p', '{}:{}'.format(port, image['server_port'])])

    cmd.append(image['image_id'])

    cmd.extend(image.get('cmd', []))

    p = os.popen(' '.join(cmd))

    now = int(time())

    info['container_id'] = container_id = p.read().strip()
    info['created_at'] = now
    info['stop_at'] = now + 3600
    info['last_startup'] = now
    info['image_id'] = image['image_id']
    if container_id:
        now = int(time())
        models.Container(info).save()

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

def rm(container_id):
    cmd = ['docker', 'rm', container_id]
    p = os.popen(' '.join(cmd))

    return p.read()

def get_container_passwd(container_id):
    cmd = ['docker', 'logs', container_id, "| grep Password | awk '{print $4}'"]
    p = os.popen(' '.join(cmd))
    passwd = p.read().strip()
    if passwd:
        models.Container({
            'container_id': container_id,
            'passwd': passwd,
        }).save()
    return passwd
