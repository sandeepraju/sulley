class MessageManager(object):
    def __init__(self, provider, *args, **kwargs):
        self._provider = provider

    def reply(self, message, text):
        self._provider.send(message.from_number, text)
