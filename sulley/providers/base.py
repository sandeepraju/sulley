from sulley.exceptions import InvalidConfig

class BaseProvider(object):
    def __init__(self, key, secret, phone):
        self.key = key
        self.secret = secret

        if not phone.startswith('+'):
            raise InvalidConfig('Invalid phone number. '
                                'Phone numbers should be in E.164 format.')
        self.phone = phone

    def send(recipient, message):
        raise NotImplementedError

