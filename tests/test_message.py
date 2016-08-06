import unittest
from mock import MagicMock

from sulley.message import Message
from sulley.providers.base import BaseProvider


class TestMessage(unittest.TestCase):
    def test_message(self):
        message = Message('+1234567890', 'hello, world!')
        self.assertEqual(str(message), '[+1234567890 - hello, world!]')

    def test_message_reply(self):
        mocked_provider = BaseProvider(
            'test-key', 'test-secret', '+10000000000')
        mocked_provider.send = MagicMock(return_value=None)
        message = Message('+1234567890', 'hello, world!', mocked_provider)
        message.reply('hello, earth!')

        # check if provider's send function was called.
        mocked_provider.send.assert_called_once_with(
            '+1234567890', 'hello, earth!')
