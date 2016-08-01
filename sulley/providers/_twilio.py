from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from base import BaseProvider
from sulley import exceptions

class Twilio(BaseProvider):
    # TODO: doc strings
    def __init__(self, *args, **kwargs):
        super(Twilio, self).__init__(*args, **kwargs)

        # TODO: accept the config in base
        # TODO: write more testable code.
        self.conn = TwilioRestClient(self.key, self.secret)

    def send(self, recipient, message):
        try:
            message = client.messages.create(body=message,
                to=recipient, from_=self.phone)
        except TwilioRestException as e:
            # make the exception class consistent for users
            raise exceptions.ProviderError(e.message)
