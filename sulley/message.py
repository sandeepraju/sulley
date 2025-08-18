"""
Message class for handling SMS messages in Sulley.

This module provides the Message class that represents an incoming SMS message
and provides methods for replying to the sender.
"""


class Message(object):
    """
    Represents an incoming SMS message with reply functionality.
    
    The Message class encapsulates an incoming SMS message and provides
    a simple interface for sending replies back to the sender.
    
    Attributes:
        from_number (str): The phone number that sent the message (E.164 format)
        text (str): The content of the SMS message
        raw_text (str): The original, unmodified message text
        matched_text (str): The portion of text that matched the regex pattern
        _provider: The SMS provider instance used for sending replies
    """

    def __init__(self, from_number, text, provider=None, matched_text=None):
        """
        Initialize a new Message instance.
        
        Args:
            from_number (str): The phone number that sent the message
            text (str): The content of the SMS message
            provider: The SMS provider instance for sending replies
            matched_text (str, optional): The portion of text that matched the regex pattern
        """
        self.from_number = from_number
        self.text = text
        self.raw_text = text  # Store the original text
        self.matched_text = matched_text or text  # Store the matched portion
        self._provider = provider

    def reply(self, text):
        """
        Send a reply SMS to the sender of this message.
        
        Args:
            text (str): The message content to send as a reply
            
        Example:
            >>> @bot.reply_to(r'hello')
            ... def greet(message):
            ...     message.reply('Hi there! How can I help you?')
        """
        if self._provider:
            self._provider.send(self.from_number, text)

    def get_raw_text(self):
        """
        Get the original, unmodified message text.
        
        Returns:
            str: The original message text as received
            
        Example:
            >>> @bot.reply_to(r'echo (.+)')
            ... def echo(message):
            ...     original = message.get_raw_text()
            ...     message.reply(f'You said: {original}')
        """
        return self.raw_text

    def get_matched_text(self):
        """
        Get the portion of text that matched the regex pattern.
        
        Returns:
            str: The matched portion of the message text
            
        Example:
            >>> @bot.reply_to(r'weather in (.+)')
            ... def weather(message):
            ...     location = message.get_matched_text()
            ...     message.reply(f'Checking weather for {location}...')
        """
        return self.matched_text

    def __repr__(self):
        """
        Return a string representation of the Message.
        
        Returns:
            str: A formatted string showing the sender and message content
        """
        return "[{} - {}]".format(self.from_number, self.text)
