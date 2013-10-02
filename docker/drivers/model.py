from docker import conf
use_mysql = getattr(conf, 'use_mysql', False)
cache_timeout = getattr(conf, 'cache_timeout', 0)

if use_mysql:
    from .query_oursql import query, create_table, show_tables, diff_table
else:
    from .query_sqlite import query, create_table, show_tables, diff_table

from . import mc

import json
import pickle
import re

from docker.logging import logger

_query = query

tables = show_tables()

class Model(object):

    table_name = 'default'
    columns = []
    auto_cache = True
    cache_timeout = cache_timeout
    auto_create_table = True

    def __init__(self):

        if self.auto_create_table and self.table_name not in tables:
            tables.append(self.table_name)
            create_table(self.table_name, self.columns)

        primarys = []
        self.defaults = {}
        for column in self.columns:
            if column.get('primary'):
                primarys.append(column)
            elif column.get('unique'):
                self.gen_query(column)
                self.gen_del(column)

            if column.get('default') is not None:
                self.defaults[column['name']] = column['default']

        self.gen_primary_query(primarys)
        self.gen_primary_del(primarys)

    def diff_table(self):
        return diff_table(self.table_name, self.columns)

    def gen_query(self, column):

        @query()
        def _gen_query(uniq_key, cur):
            if self.auto_cache:
                mc_key = mc.gen_key(self.table_name, column['name'], uniq_key)
                ret = mc.get(mc_key)
                if ret:
                    ret = self._unparse(ret)
                    return ret

            sql = 'SELECT * FROM `%s` WHERE `%s` = ?'%(self.table_name, column['name'])
            args = (uniq_key, )
            logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))

            cur.execute(sql, args)

            ret = cur.fetchone()
            if ret:
                ret = self._unparse(ret)
                if self.auto_cache:
                    mc.set(mc_key, ret, self.cache_timeout)
                return ret
            return None

        if column.get('primary'):
            self._find_by_id = _gen_query
        else:
            setattr(self, 'find_by_%s'%column['name'], _gen_query)

    def gen_primary_query(self, primarys):
        pri_len = len(primarys)
        if pri_len == 1:
            return self.gen_query(primarys[0])
        keys = list(map(lambda x: x['name'], primarys))
        def gen(*args):
            if len(args) == pri_len:
                if self.auto_cache:
                    cols = []
                    for row in zip(keys, args):
                        for v in row:
                            cols.append(v)
                    mc_key = mc.gen_key(self.table_name, *cols)
                    obj = mc.get(mc_key)
                    if obj:
                        return obj
                return self.find_one(list(zip(keys, args)))
            return None

        self._find_by_id = gen

    def find_by_id(self, *args):
        return self._find_by_id(*args)

    def gen_del(self, column):

        @query(autocommit=True)
        def _gen_del(uniq_key, cur):
            if self.auto_cache:
                mc_key = mc.gen_key(self.table_name, column['name'], uniq_key)
                obj = mc.get(mc_key)

                if obj:
                    del_keys = []
                    for col in self.columns:
                        if col.get('unique') or col.get('primary'):
                            if obj.get(col['name']):
                                del_keys.append((col['name'], obj.get(col['name'])))

                    for col_name, col_value in del_keys:
                        mc_key = mc.gen_key(self.table_name, col_name, col_value)
                        mc.delete(mc_key)

            sql = 'DELETE FROM `%s` WHERE `%s` = ?'%(self.table_name, column['name'])
            args = (uniq_key, )
            logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))

            cur.execute(sql, args)

        if column.get('primary'):
            self._del_by_id = _gen_del
        else:
            setattr(self, 'del_by_%s'%column['name'], _gen_del)

    def gen_primary_del(self, primarys):
        pri_len = len(primarys)
        if pri_len == 1:
            return self.gen_del(primarys[0])
        keys = list(map(lambda x: x['name'], primarys))
        def gen(*args):
            if len(args) == pri_len:
                if self.auto_cache:
                    cols = []
                    for row in zip(keys, args):
                        for v in row:
                            cols.append(v)
                    mc_key = mc.gen_key(self.table_name, *cols)
                    mc.delete(mc_key)
                return self.del_all(list(zip(keys, args)))
            return None

        self._del_by_id = gen

    def del_by_id(self, *args):
        self._del_by_id(*args)

    def _unparse(self, obj):
        for column in self.columns:
            if obj.get(column['name']) is not None:
                key = column['name']
                value = obj[key]
                tp = column['type']

                if tp == 'json':
                    try:
                        if value and isinstance(value, str):
                            obj[key] = json.loads(value)
                    except Exception as e:
                        logger.exception(e)
                        obj[key] = None

                elif tp == 'pickle':
                    try:
                        if value and isinstance(value, bytes):
                            obj[key] = pickle.loads(value)
                    except Exception as e:
                        logger.exception(e)
                        obj[key] = None

                else:
                    obj[key] = self._filter(tp, value,
                            column.get('encoding', 'UTF-8'))

        return obj

    def _parse(self, obj):
        for column in self.columns:
            if obj.get(column['name']) is not None:
                key = column['name']
                value = obj[key]
                tp = column['type']

                if tp == 'json':
                    try:
                        if value:
                            obj[key] = json.dumps(value)
                    except Exception as e:
                        logger.exception(e)
                        obj[key] = None

                elif tp == 'pickle':
                    try:
                        if value:
                            obj[key] = pickle.dumps(value)
                    except Exception as e:
                        logger.exception(e)
                        obj[key] = None

                else:
                    obj[key] = self._filter(tp, value,
                            column.get('encoding', 'UTF-8'))

        return obj

    def _filter(self, tp, val, encoding = 'UTF-8'):

        if tp == 'int':
            if not isinstance(val, int):
                if re.match('^[0-9-]+$', str(val)):
                    val = int(val)
                else:
                    val = None

        elif tp == 'float':
            if not isinstance(val, float):
                if re.match('^[0-9.-]+$', str(val)):
                    val = float(val)
                else:
                    val = None

        elif tp == 'str':
            if not isinstance(val, str):
                val = str(val, encoding)

        elif tp == 'bytes':
            if not isinstance(val, bytes):
                val = bytes(val, encoding)
        elif tp == 'bool':
            if not use_mysql:
                if isinstance(val, bool):
                    if val:
                        val = 1
                    else:
                        val = 0

        return val

    @query(autocommit=True)
    def save(self, obj, cur):
        obj = self._parse(obj)

        primarys = []

        uniqs = []
        use_keys = []
        use_values = []

        for column in self.columns:
            key = column['name']
            val = obj.get(key)
            if column.get('primary'):
                primarys.append([key, val])
            else:
                if val is not None:
                    if column.get('unique'):
                        uniqs.append([key, val])
                    else:
                        use_keys.append(key)
                        use_values.append(val)

        old_obj = None
        if primarys and list(filter(lambda x: x[1] is not None, primarys)):
            old_obj = self.find_by_id(*list(map(lambda x: x[1], primarys)))
            for column_name, column_value in uniqs:
                use_keys.append(column_name)
                use_values.append(column_value)

        elif len(uniqs) > 0:
            for column_name, column_value in uniqs:
                if not old_obj:
                    find = getattr(self, 'find_by_%s'%column_name)
                    old_obj = find(column_value)
                    if old_obj:
                        primarys = [[column_name, column_value]]
                        continue
                use_keys.append(column_name)
                use_values.append(column_value)

        if old_obj:
            old_obj.update(obj)
            part = ', '.join(['`%s`= ?'%k for k in use_keys])
            where, values = self.parse_query(primarys)
            for val in values:
                use_values.append(val)
            if len(use_values) < 2:
                logger.error('UPDATE %s'%str(obj))
                return primarys[0][1]

            sql = 'UPDATE `%s` SET %s %s'%(self.table_name, part, where)
            args = tuple(use_values)
            logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))

            cur.execute(sql, args)

            if self.auto_cache:
                if len(primarys) == 1:
                    uniqs.extend(primarys)
                else:
                    cols = []
                    for primary in primarys:
                        for v in primary:
                            cols.append(v)
                    mc_key = mc.gen_key(self.table_name, *cols)
                    mc.delete(mc_key)
                    mc.set(mc_key, old_obj, self.cache_timeout)

                for column_name, column_value in uniqs:
                    if column_value:
                        mc_key = mc.gen_key(self.table_name, column_name, column_value)
                        mc.delete(mc_key)
                        mc.set(mc_key, old_obj, self.cache_timeout)
            return primarys[0][1]
        else:
            for primary in primarys:
                if primary[1] is not None:
                    use_keys.append(primary[0])
                    use_values.append(primary[1])

            for key, val in self.defaults.items():
                if key not in use_keys:
                    use_keys.append(key)
                    if callable(val):
                        val = val()
                    use_values.append(val)

            part_k = ', '.join(['`%s`'%k for k in use_keys])
            part_v = ', '.join(['?' for k in use_keys])

            sql = 'INSERT INTO `%s` (%s) VALUES (%s)'%(self.table_name, part_k, part_v)
            args = tuple(use_values)
            logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))

            cur.execute(sql, args)

            if primarys and list(filter(lambda x: x[1] is not None, primarys)):
                return primarys[0][1]
            else:
                return cur.lastrowid

    def find_one(self, query = None, column = '*', order = None, group = None,
            is_or = False):

        where, values = self.parse_query(query, 1, order, group, is_or)

        @_query()
        def _find_one(cur):

            sql = 'SELECT %s FROM `%s` %s'%(column, self.table_name, where)
            args = tuple(values)
            logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))

            cur.execute(sql, args)

            return cur.fetchone()

        ret = _find_one()
        if ret:
            ret = self._unparse(ret)
        return ret

    def find_all(self, query = None, column = '*', limit = '', order = None,
            group = None, is_or = False, page = None):

        if limit and page:
            start = int(limit) * int(page)
            limit = '{}, {}'.format(start, limit)
        where, values = self.parse_query(query, limit, order, group, is_or)

        @_query()
        def _find_all(cur):

            sql = 'SELECT %s FROM `%s` %s'%(column, self.table_name, where)
            args = tuple(values)
            logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))

            cur.execute(sql, args)

            return cur.fetchall()

        return [self._unparse(ret) for ret in _find_all()]

    def parse_query(self, query = None, limit = '', order = None, group= None,
            is_or = False):
        keys = []
        values = []
        where = []

        re_q = re.compile('^(.+?)_\$(.+?)$')
        def parse_item(item):
            if len(item) == 3:
                return item
            else:
                key, val = item
            q = re_q.search(key)
            op = '='
            if q:
                key = q.group(1)
                s_op = q.group(2)
                s_op = s_op.lower()
                if s_op == 'gt':
                    op = '>'
                elif s_op == 'gte':
                    op = '>='
                elif s_op == 'lt':
                    op = '<'
                elif s_op == 'lte':
                    op = '<='
                elif s_op == 'eq':
                    op = '='
                elif s_op == 'like':
                    op = 'like'
                elif s_op == 'in':
                    op = 'in'

            return key, op, val

        columns = list(map(lambda x: x['name'], self.columns))
        def get_order(query):
            key = query[0]
            if key not in columns:
                columns.append(key)
            return columns.index(key)

        if query:
            if isinstance(query, dict):
                query = query.items()

            queries = list(map(parse_item, query))
            queries = sorted(queries, key=get_order)

            for key, op, val in queries:
                if op == 'like':
                    keys.append('`%s` LIKE "%s"'%(key, val))
                elif op == 'in':
                    if len(val) > 0:
                        op = keys.append('`%s` IN (%s)'%(key, ', '.join(['?'] * len(val))))
                        for v in val:
                            values.append(v)
                else:
                    if op == '=':
                        val = self._parse({key: val})[key]
                    keys.append('`%s` %s ?'%(key, op))
                    values.append(val)

            if len(keys) > 0:
                where.append('WHERE')
                if is_or:
                    where.append(' OR '.join(keys))
                else:
                    where.append(' AND '.join(keys))

        if order:
            if type(order) == dict:
                _order = ['ORDER BY `%s` %s'%(key, val) \
                        for key, val in order.items()]
            elif type(order) == list:
                _order = ['ORDER BY `%s`'%key for key in order]
            else:
                _order = ['ORDER BY `%s`'%order]

            where.extend(_order)

        if group:
            _group = ['GROUP BY `%s`'%key for key in group]
            where.extend(_group)

        if limit:
            limit = str(limit)
            if not limit.startswith('limit'):
                limit = 'LIMIT %s'%limit
            where.append(limit)

        return ' '.join(where), values

    def del_all(self, query = None, limit = '', order = None, group = None,
            is_or = False):

        if self.auto_cache:
            uniqs = {}
            for col in self.columns:
                if col.get('unique') or col.get('primary'):
                    uniqs[col['name']] = col.get('default')
            column = ', '.join(map(lambda x: '`%s`'%x, uniqs.keys()))
            old_objs = self.find_all(query, column, limit, order, group, is_or)

            for old_obj in old_objs:
                for k, v in uniqs.items():
                    mc_key = mc.gen_key(self.table_name, k, old_obj.get(k, v))
                    mc.delete(mc_key)

        where, values = self.parse_query(query, limit, order, group, is_or)

        @_query(autocommit=True)
        def _del_all(cur):
            sql = 'DELETE FROM `%s` %s'%(self.table_name, where)
            args = tuple(values)
            logger.debug('Query> SQL: %s | ARGS: %s'%(sql, args))

            cur.execute(sql, args)

        return _del_all()
