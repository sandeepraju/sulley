class Message(object):
    # TODO: add uuid
    def __init__(self, from_number, message, provider, *args, **kwargs):
        self._from = from_number
        self._message = message
        self._provider = provider

    def reply(self, message):
        print 'sending message [{}] to {}'.format(message, self._from)
        self._provider.send(self._from, message)
