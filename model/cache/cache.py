import pickle
import os
try:
    import server.settings
except:
    print('import server.settings error')
    import easydict
    server = easydict.EasyDict()
    server.settings = object()

class MapCache(object):

    map_cache = {}

    def __init__(self, ori_key, load_map_cache=1, rewrite_map_cache=1):
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.load_map_cache = load_map_cache
        self.rewrite_map_cache = rewrite_map_cache
        self.ori_key = ori_key
    
    def run_cache(self, args, kwargs, func):
        if hasattr(server.settings, 'config'):
            cache_type = server.settings.config.PUB_CONF.cache.type
            self.load_map_cache = self.load_map_cache & server.settings.config.PUB_CONF.cache.load
            if cache_type == 'FILE':
                cache_source = cacheFileSource(args, kwargs, func). \
                    set_load_map_cache(self.load_map_cache). \
                    set_rewrite_map_cache(self.rewrite_map_cache)
            elif cache_type == 'REDIS':
                cache_source = cacheRedisSource(args, kwargs, func). \
                    set_load_map_cache(self.load_map_cache). \
                    set_rewrite_map_cache(self.rewrite_map_cache)
            else:
                return func(*args, **kwargs)
        else:
            cache_source = cacheFileSource(args, kwargs, func). \
                set_load_map_cache(self.load_map_cache). \
                set_rewrite_map_cache(self.rewrite_map_cache)
        return cache_source.load_cache(self.obj_key)
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.obj_key = self.ori_key
            return self.run_cache(args, kwargs, func)
        return wrapper

class SimWordMapCache(MapCache):

    def __init__(self, ori_key, load_map_cache=1, rewrite_map_cache=1):
        super().__init__(ori_key, load_map_cache, rewrite_map_cache)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            para_key = str(args[0].a) + '_' + str(args[0].max_dis) + '_' + str(args[0].max_word_count)
            self.obj_key = self.ori_key + '_' + para_key
            return self.run_cache(args, kwargs, func)
        return wrapper

class cacheSource:

    def __init__(self, args, kwargs, func):
        self.args = args
        self.kwargs = kwargs
        self.func = func
        self.rewrite_map_cache = 1
        self.load_map_cache = 1

    def set_rewrite_map_cache(self, rewrite_map_cache):
        self.rewrite_map_cache = rewrite_map_cache
        return self

    def set_load_map_cache(self, load_map_cache):
        self.load_map_cache = load_map_cache
        return self

class cacheFileSource(cacheSource):

    def __init__(self, args, kwargs, func):
        super().__init__(args, kwargs, func)
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        self.dir = os.path.join(self.root_path, '../data/cache')
        self.path = os.path.join(self.dir, args[0].duc_year + '.mat')

    def update_cache(self, obj_key):
        res = self.func(*self.args, **self.kwargs)
        MapCache.map_cache[obj_key] = res
        if self.rewrite_map_cache == 1:
            if not os.path.exists(self.dir):
                os.makedirs(self.dir, exist_ok=True)
            with open(self.path, 'wb') as f:
                pickle.dump(MapCache.map_cache, f)
        return res

    def load_cache(self, obj_key):
        if self.load_map_cache == 1 and os.path.isfile(self.path):
            try:
                with open(self.path, 'rb') as f:
                    MapCache.map_cache = pickle.load(f)
                    res = MapCache.map_cache[obj_key]
            except:
                res = self.update_cache(obj_key)
        else:
            res = self.update_cache(obj_key)

        return res

class cacheRedisSource(cacheSource):

    def __init__(self, args, kwargs, func):
        super().__init__(args, kwargs, func)
        self.re = server.settings.redis
        self.duc_year = args[0].duc_year

    def update_cache(self, obj_key):
        res = self.func(*self.args, **self.kwargs)
        MapCache.map_cache[obj_key] = res
        if self.rewrite_map_cache == 1:
            self.re.set(self.duc_year + '_' + obj_key, pickle.dumps(res));
        return res

    def load_cache(self, obj_key):
        if self.load_map_cache == 1:
            try:
                res = pickle.loads(self.re.get(self.duc_year + '_' + obj_key))
            except:
                res = self.update_cache(obj_key)
        else:
            res = self.update_cache(obj_key)
        return res
