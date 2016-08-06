import unittest

from sulley.message import Message

class TestMessage(unittest.TestCase):

    def test_message(self):
        message = Message('+1234567890', 'hello, world!')
        self.assertEqual(str(message), '[+1234567890 - hello, world!]')
