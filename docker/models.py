from docker.conf import prefix
from lee import Model, query, Table, conf as lee_conf
from docker.logging import logger

class _Container(Model):
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

Container = Table(_Container)

class _UserContainer(Model):
    table_name = '{}user_container'.format(prefix)

    columns = [
        {'name': 'user_id',      'type': 'int', 'length': 10, 'unsigned': True, 'primary': True},
        {'name': 'container_id', 'type': 'str', 'length': 32, 'primary': True, 'unique': True}
    ]

UserContainer = Table(_UserContainer)

class _User(Model):
    table_name = '{}user'.format(prefix)

    columns = [
        {'name': 'user_id',  'type': 'int', 'length': 10, 'unsigned': True, 'primary': True, 'auto_increment': True},
        {'name': 'username', 'type': 'str', 'length': 50, 'unique': True},
        {'name': 'passwd',   'type': 'str', 'length': 32},
        {'name': 'email',    'type': 'str', 'length': 100, 'unique': True}
    ]

User = Table(_User)

class Sequence(Model):
    table_name = 'sequence'

    columns = [
        {'name': 'name', 'type': 'str', 'primary': True, 'length': 20},
        {'name': 'id',   'type': 'int', 'default': 0}
    ]

    @query(autocommit=True)
    def next(self, name, cur):
        name = '{}:{}'.format(prefix, name)
        last_id = 0
        if lee_conf.use_mysql:
            sql = 'INSERT INTO `sequence` (`name`) VALUES (?) ON DUPLICATE KEY UPDATE `id` = LAST_INSERT_ID(`id` + 1)'
            args = (name, )
            logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))
            cur.execute(sql, args)
            last_id = cur.lastrowid
        else:
            seq = self._table.find_by_id(name)
            if seq:
                sql = 'UPDATE `sequence` SET `id` = `id` + 1 WHERE `name` = ?'
                args = (name, )
                logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))
                cur.execute(sql, args)
            else:
                self._table.save({'name': name})

            seq = self._table.find_by_id(name)
            last_id = seq['id']
        return last_id

    def save(self, name, id):
        name = '{}:{}'.format(prefix, name)
        return self._table.save({'name': name, 'id': id})

seq = Table(Sequence)()
