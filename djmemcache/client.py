from pymemcache import sharding_client as _client


class Client(_client.ShardingClient):
    # this just fixes some API holes between python-memcached and pymemcache
    set_multi = _client.ShardingClient.set_many
    get_multi = _client.ShardingClient.get_many
    delete_multi = _client.ShardingClient.delete_many

    def disconnect_all(self, force=False):
        if force == True:
            self.quit()