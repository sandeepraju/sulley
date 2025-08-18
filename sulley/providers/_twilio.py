"""
Twilio SMS provider implementation for Sulley.

This module provides the Twilio class that implements SMS sending
using the Twilio API.
"""

from twilio.rest import Client
from twilio.base.exceptions import TwilioException

from .base import BaseProvider
from .. import exceptions


class Twilio(BaseProvider):
    """
    Twilio SMS provider implementation.
    
    This class provides SMS sending functionality using the Twilio API.
    It handles authentication, message creation, and error handling
    specific to Twilio's service.
    
    Attributes:
        client: Twilio REST client instance
    """

    def __init__(self, key, secret, phone):
        """
        Initialize the Twilio provider.
        
        Args:
            key (str): Twilio Account SID
            secret (str): Twilio Auth Token
            phone (str): Twilio phone number (E.164 format)
        """
        super(Twilio, self).__init__(key, secret, phone)

        # Initialize Twilio REST client
        self.client = Client(self.key, self.secret)

    def send(self, recipient, message):
        """
        Send an SMS message using Twilio.
        
        Args:
            recipient (str): The recipient's phone number (E.164 format)
            message (str): The message content to send
            
        Raises:
            ProviderError: If the SMS fails to send due to Twilio API errors
            
        Example:
            >>> provider = Twilio('account_sid', 'auth_token', '+1234567890')
            >>> provider.send('+0987654321', 'Hello from Sulley!')
        """
        try:
            # Create and send the message via Twilio
            message = self.client.messages.create(
                body=message, to=recipient, from_=self.phone
            )
        except TwilioException as e:
            # Convert Twilio exceptions to Sulley exceptions
            # TODO: Consider preserving more error details from Twilio
            raise exceptions.ProviderError(str(e))
