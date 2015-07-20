from threading import local
from collections import namedtuple
from django.core.cache import CacheHandler

_getitem = CacheHandler.__getitem__
def patch_cache_handler():
    _caches_cls = namedtuple("_caches", ["caches"])
    def __getitem__(self, alias):
        if isinstance(self._caches, local):
            self._caches = _caches_cls(getattr(self._caches, "caches", {}))
        return _getitem(self, alias)
    CacheHandler.__getitem__ = __getitem__

patch_cache_handler()


try:
    import cPickle as pickle
except ImportError:
    import pickle
import six
from collections import namedtuple
from . import client
from django.core.cache.backends.memcached import BaseMemcachedCache

unserialize_types = []
unserialize_types += six.integer_types
unserialize_types.append(six.binary_type)

def serialize_pickle(key, value):
    if isinstance(value, tuple(unserialize_types)):
        return value, 1
    return pickle.dumps(value), 2


def deserialize_pickle(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return pickle.loads(value)
    raise Exception('Unknown flags for value: {1}'.format(flags))


class PyMemcacheCache(BaseMemcachedCache):

    """An implementation of a cache binding using pymemcache."""

    def __init__(self, server, params):
        super(PyMemcacheCache, self).__init__(
            server, params,
            library=client,
            value_not_found_exception=ValueError
        )
        self._client = None

    @property
    def _cache(self):
        if not self._client:
            kwargs = {
                'serializer': serialize_pickle,
                'deserializer': deserialize_pickle,
            }
            if self._options:
                for key, value in self._options.items():
                    kwargs[key.lower()] = value
            self._client = self._lib.Client(self._servers, **kwargs)
        return self._client