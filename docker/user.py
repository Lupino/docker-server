from . import models
from .utils import md5sum
from . import container
from . import conf

def login(username, passwd):
    user = models.User.find_by_username(username)
    if not user:
        return {'err': '用户 {} 不存在'.format(username)}
    if user['passwd'] == md5sum(passwd):
        user.pop('passwd')
        return user
    return {'err': '用户名密码错误'}


def register(username, passwd, repasswd, email):
    retval = {}
    if not username or not email or not passwd:
        if not username:
            retval['type'] = 'username'
        elif not email:
            retval['type'] = 'email'
        else:
            retval['type'] = 'passwd'
        retval['err'] = '用户名、Email或密码不为空'
    elif len(username) > 50:
        retval['type'] = 'username'
        retval['err'] = '用户名:{} 过长，应该小于50个字符'.format(username)
    elif models.User.find_by_username(username):
        retval['type'] = 'username'
        retval['err'] = '用户名: {} 已被抢注'.format(username)
    elif models.User.find_by_email(email):
        retval['type'] = 'email'
        retval['err'] = 'Email: {} 已被抢注'.format(email)
    elif passwd != repasswd:
        retval['type'] = 'passwd'
        retval['err'] = '两次输入密码不一样'
    else:
        user_id = models.User({
            'username': username,
            'passwd': md5sum(passwd),
            'email': email
        }).save()
        retval['username'] = username
        retval['user_id'] = user_id
        retval['email'] = email

    return retval

def change_passwd(user_id, oldpasswd, newpasswd, renewpasswd):
    retval = {}
    user = models.User.find_by_id(user_id)
    if user.passwd == md5sum(oldpasswd):
        if newpasswd and newpasswd == renewpasswd:
            models.User({'user_id': user_id, 'passwd': md5sum(newpasswd)}).save()
        else:
            retval['err'] = '前后两次输入不一致'
    else:
        retval['err'] = '密码输入错误'

    return retval

def create_cantainer(user_id, image_id):
    image = list(filter(lambda x: x['image_id'] == image_id, conf.images))
    if image:
        image = image[0]
        container_id = container.create(image)
        if container_id:
            models.UserContainer({'user_id': user_id, 'container_id': container_id}).save()
            return container_id

    return None

def get_containers(user_id):
    containers = models.UserContainer.find_all({'user_id': user_id})
    return list(map(lambda x: models.Container.find_by_id(x['container_id']),
        containers))
