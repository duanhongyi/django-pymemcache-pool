try:
    import cPickle as pickle
except ImportError:
    import pickle

from pymemcache import PooledClient
from django.core.cache.backends.memcached import BaseMemcachedCache


def serialize_pickle(key, value):
    if isinstance(value, str):
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
            options = {
                'serializer': serialize_pickle,
                'deserializer': deserialize_pickle,
            }
            if self._options:
                options.update(**self._options)
            clients = []
            for server in self._servers:
                host, port = server
                clients.append(PooledClient((host, int(port)), **options))
            self._client = self._lib.Client(clients, **options)
        return self._client
