import re


class Matcher(object):
    def __init__(self, *args, **kwargs):
        self._pairs = []

    def register(self, pattern, func):
        self._pairs.append((re.compile(pattern), func))

    def deregister(self, pattern):
        try:
            pair = filter(lambda x: x[0].pattern == pattern, self._pairs)[0]
            self._pairs.remove(pair)
        except Exception:
            # pattern not found. fail silently
            pass

    def match(self, pattern):
        for pair in self._pairs:
            if pair[0].match(pattern):
                return pair[1]
