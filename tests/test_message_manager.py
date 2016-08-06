import unittest
from mock import MagicMock

from sulley.providers.base import BaseProvider
from sulley.message import Message
from sulley.message_manager import MessageManager

class TestMessageManager(unittest.TestCase):
    def setUp(self):
        self.mockedProvider = BaseProvider(
            'test-key', 'test-secret', '+10000000000')
        self.mockedProvider.send = MagicMock(return_value=None)

        self.message = Message('+1234567890', 'hello, world!')

    def test_message_manager_reply(self):
        message_manager = MessageManager(self.mockedProvider)
        message_manager.reply(self.message, 'hello, earth!')

        # check if provider's send function was called.
        self.mockedProvider.send.assert_called_once_with(
            '+1234567890', 'hello, earth!')
