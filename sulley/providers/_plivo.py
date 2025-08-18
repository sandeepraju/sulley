import plivo

from .base import BaseProvider
from .. import exceptions


class Plivo(BaseProvider):
    def __init__(self, *args, **kwargs):
        super(Plivo, self).__init__(*args, **kwargs)

        self.client = plivo.RestClient(self.key, self.secret)

    def send(self, recipient, message):
        try:
            response = self.client.messages.create(
                src=self.phone, dst=recipient, text=message
            )
        except Exception as e:
            raise exceptions.ProviderError(str(e))
