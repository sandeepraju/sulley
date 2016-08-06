class Message(object):
    def __init__(self, from_number, text, *args, **kwargs):
        self.from_number = from_number
        self.text = text

    def __repr__(self):
        return '[{} - {}]'.format(self.from_number, self.text)
