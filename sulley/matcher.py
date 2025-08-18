import re


class Matcher(object):
    def __init__(self, *args, **kwargs):
        self._pairs = []

    def register(self, pattern, func):
        if pattern.__class__.__name__ == "Pattern":
            # a compiled pattern object is passed directly
            self._pairs.append((pattern, func))
        else:
            # a pattern is passed
            self._pairs.append((re.compile(str(pattern)), func))

    def deregister(self, pattern):
        try:
            # Remove all patterns that match the given pattern string
            # For compiled patterns, compare the pattern string
            # For string patterns, compare directly
            if isinstance(pattern, str):
                self._pairs = [(p, f) for p, f in self._pairs if p.pattern != pattern]
            else:
                # If pattern is a compiled regex, remove exact matches
                self._pairs = [(p, f) for p, f in self._pairs if p != pattern]
        except Exception:
            # pattern not found. fail silently
            pass

    def match(self, pattern):
        for pair in self._pairs:
            if pair[0].match(pattern):
                return pair[1]
        return None
