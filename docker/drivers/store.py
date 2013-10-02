from docker.conf import prefix
from .model import Model, use_mysql, query
from docker.logging import logger

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

class Sequence(Model):
    table_name = 'sequence'

    columns = [
        {'name': 'name', 'type': 'str', 'primary': True, 'length': 20},
        {'name': 'id',   'type': 'int', 'default': 0}
    ]

    @query(autocommit=True)
    def next(self, name, cur):
        name = '%s:%s'%(prefix, name)
        last_id = 0
        if use_mysql:
            sql = 'INSERT INTO `sequence` (`name`) VALUES (?) ON DUPLICATE KEY UPDATE `id` = LAST_INSERT_ID(`id` + 1)'
            args = (name, )
            logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))
            cur.execute(sql, args)
            last_id = cur.lastrowid
        else:
            seq = self.find_by_id(name)
            if seq and seq['id']:
                sql = 'UPDATE `sequence` SET `id` = `id` + 1 WHERE `name` = ?'
                args = (name, )
                logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))
                cur.execute(sql, args)
            else:
                self.save({'name': name})

            seq = self.find_by_id(name)
            last_id = seq['id']
        return last_id

    def update(self, name, id):
        name = '{}:{}'.format(prefix, name)
        return self.save({'name': name, 'id': id})

seq = Sequence()
