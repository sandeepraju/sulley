from twilio.rest import Client
from twilio.base.exceptions import TwilioException

from .base import BaseProvider
from .. import exceptions


class Twilio(BaseProvider):
    def __init__(self, *args, **kwargs):
        super(Twilio, self).__init__(*args, **kwargs)

        self.client = Client(self.key, self.secret)

    def send(self, recipient, message):
        try:
            message = self.client.messages.create(
                body=message, to=recipient, from_=self.phone
            )
        except TwilioException as e:
            # TODO: this currently hides twilio's exception.
            #       find a way to pass it on.
            raise exceptions.ProviderError(str(e))
