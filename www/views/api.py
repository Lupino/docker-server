from www import app, config, request
from docker import user as _user
from docker.drivers import store

@app.route('/api/user/me')
def user_me(user):
    return user

@app.route('/api/user/containers')
def user_containers(user):
    return _user.get_containers(user['user_id'])

@app.post('/api/user/create/cantainer')
def user_create_container(user):
    image = request.forms.image
    container_id = _user.create_cantainer(user['user_id'], image)
    container = store.container.find_by_id(container_id)
    container.update({'user_id': user_id})
    return container

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
    has = store.user_container.find_by_id(user['user_id'], container_id)
    if has:
        container.start(container_id)

@app.post('/api/container/restart/:container_id')
def restart_container(container_id, user):
    has = store.user_container.find_by_id(user['user_id'], container_id)
    if has:
        container.restart(container_id)

@app.post('/api/container/stop/:container_id')
def stop_container(container_id, user):
    has = store.user_container.find_by_id(user['user_id'], container_id)
    if has:
        container.stop(container_id)

@app.get('/api/images')
def images():
    return config.images
