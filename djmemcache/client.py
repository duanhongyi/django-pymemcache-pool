from pymemcache.client.hash import HashClient


class Client(HashClient):

    def disconnect_all(self):
        if not self.use_pooling:
            self.quit()
