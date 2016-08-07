import plivo

from base import BaseProvider
from sulley import exceptions


class Plivo(BaseProvider):
    def __init__(self, *args, **kwargs):
        super(Plivo, self).__init__(*args, **kwargs)

        self.conn = plivo.RestAPI(self.key, self.secret)

    def send(self, recipient, message):
        response = self.conn.send_message({
            'src': self.phone[1:],  # strip off the start + for plivo
            'dst': recipient,
            'text': message
        })

        # check if SMS was sent successfully.
        if response[0] >= 300 or response[0] < 200:
            # non 2xx response
            raise exceptions.ProviderError(response[1]['error'])
