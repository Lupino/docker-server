from www import app, config, request
from docker import user as _user, container
from docker import models
import json

@app.route('/api/user/me')
def user_me(user):
    return user

@app.post('/api/user/login')
def user_login():
    username = request.forms.username
    passwd = request.forms.passwd
    ret = _user.login(username, passwd)
    if ret.get('user_id'):
        app.login(ret)
    return ret

@app.route('/api/user/containers')
def user_containers(user):
    containers = [_container.copy() for _container in _user.get_containers(user['user_id']) if _container]
    return json.dumps(containers)

@app.post('/api/user/create/container')
def user_create_container(user):
    image = request.forms.image
    container_id = _user.create_cantainer(user['user_id'], image)
    if not container_id:
        return {'err': 'container create fail'}
    _container = models.Container.find_by_id(container_id)
    _container = _container.copy()
    _container.update({'user_id': user['user_id']})
    return json.dumps(_container)

@app.delete('/api/user/remove/container/:container_id')
def user_remove_container(container_id, user):
    models.Container.del_by_id(container_id)
    models.UserContainer.del_by_id(user['user_id'], container_id)
    container.stop(container_id)
    container.rm(container_id)
    return {}

@app.post('/api/user/register')
def user_register():
    username = request.forms.username
    passwd = request.forms.passwd
    repasswd = request.forms.repasswd
    email = request.forms.email
    return _user.register(username, passwd, repasswd, email)

@app.post('/api/user/passwd')
def user_passwd(user):
    oldpasswd = request.forms.oldpasswd
    newpasswd = request.forms.newpasswd
    renewpasswd = request.forms.renewpasswd
    user_id = user['user_id']
    return _user.change_passwd(user_id, oldpasswd, newpasswd, renewpasswd)

@app.post('/api/container/start/:container_id')
def start_container(container_id, user):
    has = models.UserContainer.find_by_id(user['user_id'], container_id)
    if has:
        container.start(container_id)

    return {}

@app.post('/api/container/restart/:container_id')
def restart_container(container_id, user):
    has = models.UserContainer.find_by_id(user['user_id'], container_id)
    if has:
        container.restart(container_id)

    return {}

@app.post('/api/container/stop/:container_id')
def stop_container(container_id, user):
    has = models.UserContainer.find_by_id(user['user_id'], container_id)
    if has:
        container.stop(container_id)

    return ''

@app.get('/api/container/:container_id/passwd')
def container_passwd(container_id, user):
    has = models.UserContainer.find_by_id(user['user_id'], container_id)
    if has:
        return container.get_container_passwd(container_id)
    return ''

@app.get('/api/images')
def images():
    return json.dumps(config.images)
