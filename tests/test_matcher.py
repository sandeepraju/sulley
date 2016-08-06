import unittest

from sulley.matcher import Matcher

class TestMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = Matcher()

    def test_matcher_register_new_pattern(self):
        # matches the pattern that exists
        self.matcher.register('^abc', lambda x: x)
        self.assertEqual(self.matcher.match('abc')(100), 100)

    def test_matcher_register_when_pattern_already_exists(self):
        self.matcher.register('^abc', lambda x: x)
        self.assertEqual(self.matcher.match('abc')(100), 100)

        # register duplicate (don't throw error)
        self.matcher.register('^abc', lambda x: x**2)

    def test_matcher_match_when_pattern_doesnt_exist(self):
        # doesn't match anything if a pattern doesn't exist
        self.assertEqual(self.matcher.match('abc'), None)

    def test_matcher_match_when_pattern_already_exist(self):
        self.matcher.register('^abc', lambda x: x)
        self.assertEqual(self.matcher.match('abc')(100), 100)

        # register the duplicate pattern
        self.matcher.register('^abc', lambda x: x**2)

        # should call the first matching function
        self.assertEqual(self.matcher.match('abc')(100), 100)
    
    def test_matcher_deregister_when_no_such_pattern_exist(self):
        # should fail silently
        self.matcher.deregister('^abc')

    def test_matcher_deregister_when_pattern_exists(self):
        self.matcher.register('^abc', lambda x: x)

        # should match successfully
        self.assertEqual(self.matcher.match('abc')(100), 100)

        # deregister the pattern
        self.matcher.deregister('^abc')

        # shouldn't match anything
        self.assertEqual(self.matcher.match('abc'), None)


    def test_matcher_deregister_when_duplicate_pattern_exists(self):
        self.matcher.register('^abc', lambda x: x)
        self.matcher.register('^abc', lambda x: x**2)  # add a duplicate pattern

        self.assertEqual(self.matcher.match('abc')(100), 100)

        # remove the route
        self.matcher.deregister('^abc')

        # should match the second pattern
        self.assertEqual(self.matcher.match('abc')(10), 100)
