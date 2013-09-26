from crawl.conf import prefix
from crawl.drivers.model import Model

class Container(Model):
    table_name = '{}container'.format(prefix)

    create_table_oursql_sql = '''
        CREATE TABLE IF NOT EXISTS `{}container` (
          `container_id` varchar(32) NOT NULL,
          `image_id` varchar(32),
          `passwd` varchar(32),
          `ssh_port` int(5) unsigned NOT NULL DEFAULT '0',
          `server_port` int(5) unsigned NOT NULL DEFAULT '0',
          `created_at` int(10) unsigned NOT NULL DEFAULT '0',
          `stop_at` int(10) unsigned NOT NULL DEFAULT '0',
          `last_startup` int(10) unsigned NOT NULL DEFAULT '0',
          PRIMARY KEY (`container_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''.format(prefix)

    columns = [
        {'name': 'container_id', 'type': 'str', 'primary': True},
        {'name': 'image_id',     'type': 'str'},
        {'name': 'passwd',       'type': 'str'},
        {'name': 'ssh_port',     'type': 'int'},
        {'name': 'server_port',  'type': 'int'},
        {'name': 'created_at',   'type': 'int'},
        {'name': 'stop_at',      'type': 'int'},
        {'name': 'last_startup', 'type': 'int'}
    ]

container = Container()

class UserContainer(Model):
    table_name = '{}user_container'.format(prefix)

    create_table_oursql_sql = '''
        CREATE TABLE IF NOT EXISTS `{}user_container` (
          `user_id` int(10) unsigned NOT NULL,
          `container_id` varchar(32) NOT NULL,
          PRIMARY KEY (`user_id`,`container_id`),
          KEY `container_id` (`container_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''.format(prefix)

    columns = [
        {'name': 'user_id',      'type': 'int', 'primary': True},
        {'name': 'container_id', 'type': 'str', 'primary': True}
    ]

user_container = UserContainer()

class User(Model):
    table_name = '{}user'.format(prefix)

    create_table_oursql_sql = '''
        CREATE TABLE IF NOT EXISTS `{}user` (
          `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
          `username` varchar(50) NOT NULL,
          `passwd` varchar(32) NOT NULL,
          `email` varchar(100) NOT NULL,
          PRIMARY KEY (`user_id`),
          UNIQUE KEY `username` (`username`,`email`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''.format(prefix)

    columns = [
        {'name': 'user_id',  'type': 'int', 'primary': True},
        {'name': 'username', 'type': 'str', 'unique': True},
        {'name': 'passwd',   'type': 'str'},
        {'name': 'email',    'type': 'str', 'unique': True}
    ]

user = User()
