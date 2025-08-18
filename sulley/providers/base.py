"""
Base provider class for SMS service integrations.

This module provides the BaseProvider class that defines the interface
for SMS service providers like Twilio and Plivo.
"""

from ..exceptions import InvalidConfig


class BaseProvider(object):
    """
    Abstract base class for SMS service providers.
    
    This class defines the interface that all SMS providers must implement.
    It handles common functionality like phone number validation and
    provides a template for provider-specific implementations.
    
    Attributes:
        key (str): API key/account SID for the SMS service
        secret (str): API secret/auth token for the SMS service
        phone (str): The phone number associated with this provider (E.164 format)
    """

    def __init__(self, key, secret, phone):
        """
        Initialize a new provider instance.
        
        Args:
            key (str): API key/account SID for the SMS service
            secret (str): API secret/auth token for the SMS service
            phone (str): The phone number for this provider (must be E.164 format)
            
        Raises:
            InvalidConfig: If the phone number is not in E.164 format
        """
        self.key = key
        self.secret = secret

        # Validate phone number format
        if not phone.startswith("+"):
            raise InvalidConfig(
                "Invalid phone number. " "Phone numbers should be in E.164 format."
            )
        self.phone = phone

    def send(self, recipient, message):
        """
        Send an SMS message to the specified recipient.
        
        This is an abstract method that must be implemented by subclasses.
        
        Args:
            recipient (str): The recipient's phone number (E.164 format)
            message (str): The message content to send
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError
