from crawl.conf import prefix
from crawl.drivers.model import Model

class Container(Model):
    table_name = '{}container'.format(prefix)

    columns = [
        {'name': 'container_id', 'type': 'str', 'primary': True, 'length': 32},
        {'name': 'image_id',     'type': 'str', 'length': 32},
        {'name': 'passwd',       'type': 'str', 'length': 32},
        {'name': 'ssh_port',     'type': 'int', 'unsigned': True, 'length': 5, 'default': 0},
        {'name': 'server_port',  'type': 'int', 'unsigned': True, 'length': 5, 'default': 0},
        {'name': 'created_at',   'type': 'int', 'unsigned': True, 'length': 10, 'default': 0},
        {'name': 'stop_at',      'type': 'int', 'unsigned': True, 'length': 10, 'default': 0},
    ]

container = Container()

class UserContainer(Model):
    table_name = '{}user_container'.format(prefix)

    columns = [
        {'name': 'user_id',      'type': 'int', 'length': 10, 'unsigned': True, 'primary': True},
        {'name': 'container_id', 'type': 'str', 'length': 32, 'primary': True, 'unique': True}
    ]

user_container = UserContainer()

class User(Model):
    table_name = '{}user'.format(prefix)

    columns = [
        {'name': 'user_id',  'type': 'int', 'length': 10, 'unsigned': True, 'primary': True, 'auto_increment': True},
        {'name': 'username', 'type': 'str', 'length': 50, 'unique': True},
        {'name': 'passwd',   'type': 'str', 'length': 32},
        {'name': 'email',    'type': 'str', 'length': 100, 'unique': True}
    ]

user = User()
