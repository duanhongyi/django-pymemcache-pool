django-pymemcache-pool
=====================

An efficient fast Django Memcached backend with a pool of connectors, based on
pymemcache.

See https://github.com/duanhongyi/django-pymemcache-pool

Each connection added in the pool stays connected to Memcache or Membase,
drastically limiting the number of reconnections and open sockets your
application will use on high load.

If you configure more than one Memcache server, each new connection
will randomly pick one.

Everytime a socket timeout occurs on a server, it's blacklisted so
new connections avoid picking it for a while.

To use this backend, make sure the package is installed in your environment
then use `django-pymemcache-pool.cache.UMemcacheCache` as backend in your settings.
