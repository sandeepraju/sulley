class BaseProvider(object):
    def __init__(self, key, secret, phone):
        self.key = key
        self.secret = secret
        self.phone = phone

    def send(recipient, message):
        raise NotImplementedError

