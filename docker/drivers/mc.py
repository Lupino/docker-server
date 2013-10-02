from docker import conf
memcached = getattr(conf, 'memcached', False)
lru_cache = getattr(conf, 'lru_cache', False)
if memcached:
    import memcache
    mc = memcache.Client(memcached)
    get = mc.get
    set = mc.set
    delete = mc.delete
    incr = mc.incr
    decr = mc.decr
elif lru_cache:
    from _thread import RLock
    _cache = {}
    _cache_max = 128
    full = False
    key_list = []

    lock = RLock()
    def get(key, *args, **kwargs):
        global _cache, full, key_list, lock
        with lock:
            if key in key_list:
                key_list.remove(key)
                key_list.insert(0, key)
            return _cache.get(key)

    def set(key, val, *args, **kwargs):
        global _cache, full, key_list, lock
        with lock:
            if key in key_list:
                _cache[key] = val
                key_list.remove(key)
                key_list.insert(0, key)
            elif full:
                old_key = key_list.pop()
                key_list.insert(0, key)
                _cache.pop(old_key)
                _cache[key] = val
            else:
                key_list.insert(0, key)
                _cache[key] = val
                full = (len(_cache) >= _cache_max)

    def delete(key, *args, **kwargs):
        global _cache, full, key_list, lock
        with lock:
            if key in key_list:
                key_list.remove(key)
                _cache.pop(key)
                full = (len(_cache) >= _cache_max)

    def incr(key, *args, **kwargs):
        global _cache, full, key_list, lock
        with lock:
            val = _cache.get(key, 0)
            val += 1
            if key in key_list:
                _cache[key] = val
                key_list.remove(key)
                key_list.insert(0, key)
            elif full:
                old_key = key_list.pop()
                key_list.insert(0, key)
                _cache.pop(old_key)
                _cache[key] = val
            else:
                key_list.insert(0, key)
                _cache[key] = val
                full = (len(_cache) >= _cache_max)

            return _cache.get(key)

    def decr(key, *args, **kwargs):
        global _cache, full, key_list, lock
        with lock:
            val = _cache.get(key, 0)
            val -= 1
            if key in key_list:
                _cache[key] = val
                key_list.remove(key)
                key_list.insert(0, key)
            elif full:
                old_key = key_list.pop()
                key_list.insert(0, key)
                _cache.pop(old_key)
                _cache[key] = val
            else:
                key_list.insert(0, key)
                _cache[key] = val
                full = (len(_cache) >= _cache_max)

            return _cache.get(key)
else:
    def get(key, *args, **kwargs):
            return None

    def set(key, val, *args, **kwargs):
        pass

    def delete(key, *args, **kwargs):
        pass

    def incr(key, *args, **kwargs):
        return 0

    def decr(key, *args, **kwargs):
        return 0

def gen_key(*args):
    args = map(str, args)
    return ':'.join(args)