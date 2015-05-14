from pymemcache import sharding_client as client


class Client(client.ShardingClient):
    # this just fixes some API holes between python-memcached and pymemcache
    set_multi = client.ShardingClient.set_many
    get_multi = client.ShardingClient.get_many
    delete_multi = client.ShardingClient.delete_many
    disconnect_all = client.ShardingClient.quit
