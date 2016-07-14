class Message(object):
    # TODO: add uuid (use decorator?)
    def __init__(self, from_number, text, provider, *args, **kwargs):
        self.from_number = from_number
        self.text = text
        self._provider = provider

    def reply(self, text):
        print 'sending message [{}] to {}'.format(text, self._from)
        self._provider.send(self._from, text)
