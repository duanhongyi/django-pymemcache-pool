try:
    import cPickle as pickle
except ImportError:
    import pickle
import six
from collections import namedtuple
from . import client
from pymemcache.client import PooledClient
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

    _client = None

    def __init__(self, server, params):
        super(PyMemcacheCache, self).__init__(
            server, params,
            library=client,
            value_not_found_exception=ValueError
        )

    @property
    def _cache(self):
        if not PyMemcacheCache._client:
            kwargs = {
                'serializer': serialize_pickle,
                'deserializer': deserialize_pickle,
            }
            if self._options:
                for key, value in self._options.items():
                    kwargs[key.lower()] = value
            clients = []
            for server in self._servers:
                host, port = server.split(":")
                clients.append(PooledClient((host, int(port)), **kwargs))
            PyMemcacheCache._client = self._lib.Client(clients)
        return PyMemcacheCache._client