from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from base import BaseProvider
from sulley import exceptions


class Twilio(BaseProvider):
    def __init__(self, *args, **kwargs):
        super(Twilio, self).__init__(*args, **kwargs)

        self.client = TwilioRestClient(self.key, self.secret)

    def send(self, recipient, message):
        try:
            message = self.client.messages.create(
                body=message, to=recipient, from_=self.phone)
        except TwilioRestException as e:
            # TODO: this currently hides twilio's exception.
            #       find a way to pass it on.
            raise exceptions.ProviderError(e.message)
