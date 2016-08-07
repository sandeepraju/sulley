class InvalidConfig(Exception):
    def __init__(self, *args, **kwargs):
        super(InvalidConfig, self).__init__(*args, **kwargs)


class SulleyError(Exception):
    def __init__(self, *args, **kwargs):
        super(SulleyError, self).__init__(*args, **kwargs)


class ProviderError(Exception):
    def __init__(self, *args, **kwargs):
        super(ProviderError, self).__init__(*args, **kwargs)


class BadRequest(Exception):
    def __init__(self, *args, **kwargs):
        super(BadRequest, self).__init__(*args, **kwargs)
