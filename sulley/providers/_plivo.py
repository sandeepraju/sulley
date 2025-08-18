"""
Plivo SMS provider implementation for Sulley.

This module provides the Plivo class that implements SMS sending
using the Plivo API.
"""

import plivo

from .base import BaseProvider
from .. import exceptions


class Plivo(BaseProvider):
    """
    Plivo SMS provider implementation.
    
    This class provides SMS sending functionality using the Plivo API.
    It handles authentication, message creation, and error handling
    specific to Plivo's service.
    
    Attributes:
        client: Plivo REST client instance
    """

    def __init__(self, key, secret, phone):
        """
        Initialize the Plivo provider.
        
        Args:
            key (str): Plivo Auth ID
            secret (str): Plivo Auth Token
            phone (str): Plivo phone number (E.164 format)
        """
        super(Plivo, self).__init__(key, secret, phone)

        # Initialize Plivo REST client
        self.client = plivo.RestClient(self.key, self.secret)

    def send(self, recipient, message):
        """
        Send an SMS message using Plivo.
        
        Args:
            recipient (str): The recipient's phone number (E.164 format)
            message (str): The message content to send
            
        Raises:
            ProviderError: If the SMS fails to send due to Plivo API errors
            
        Example:
            >>> provider = Plivo('auth_id', 'auth_token', '+1234567890')
            >>> provider.send('+0987654321', 'Hello from Sulley!')
        """
        try:
            # Create and send the message via Plivo
            response = self.client.messages.create(
                src=self.phone, dst=recipient, text=message
            )
        except Exception as e:
            # Convert Plivo exceptions to Sulley exceptions
            raise exceptions.ProviderError(str(e))
