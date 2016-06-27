import re

class Matcher(object):
    def __init__(self, *args, **kwargs):
        self._pairs = []

    def register(self, pattern, func):
        # TODO: check for duplicates?
        self._pairs.append((re.compile(pattern), func))

    def deregister(self, pattern):
        try:
            idx = filter(lambda x: x[0].pattern == pattern, self._pairs)[0]
            self._pairs.pop(idx)
        except Exception as e:
            # pattern not found. Nothing to do.
            pass

    def match(self, pattern):
        for pair in self._pairs:
            if pair[0].match(pattern):
                return pair[1]
