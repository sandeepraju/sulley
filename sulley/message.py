class Message(object):
    def __init__(self, from_number, text, provider=None, *args, **kwargs):
        self.from_number = from_number
        self.text = text
        self._provider = provider

    def reply(self, text):
        self._provider.send(self.from_number, text)

    def __repr__(self):
        return '[{} - {}]'.format(self.from_number, self.text)
