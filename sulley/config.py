"""
Configuration management for Sulley SMS bot.

This module provides the Config class that handles loading and managing
configuration settings from JSON files and environment variables.
"""

import json
import os
from .exceptions import InvalidConfig


class Config(object):
    """
    Configuration manager for Sulley SMS bot.
    
    This class handles loading configuration from JSON files and provides
    access to configuration settings. It supports loading from a default
    config.json file or from a file specified by the SULLEY_CONFIG
    environment variable.
    
    Attributes:
        config_file (str): Path to the configuration file
        config (dict): Loaded configuration data
    """

    def __init__(self, config_file=None):
        """
        Initialize the configuration manager.
        
        Args:
            config_file (str, optional): Path to configuration file.
                                        If not provided, uses SULLEY_CONFIG
                                        environment variable or defaults to 'config.json'
        """
        self.config_file = config_file or self._get_config_file()
        self.config = self._load_config()
        # Set dynamic attributes for backward compatibility
        self.__dict__.update(self.config)

    def _get_config_file(self):
        """
        Get the configuration file path.
        
        Returns:
            str: Path to the configuration file
            
        Note:
            Checks the SULLEY_CONFIG environment variable first,
            then defaults to 'config.json' in the current directory.
        """
        return os.environ.get("SULLEY_CONFIG", "config.json")

    def _load_config(self):
        """
        Load configuration from the JSON file.
        
        Returns:
            dict: Configuration data loaded from the file
            
        Raises:
            InvalidConfig: If the config file is not found or contains invalid JSON
        """
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except IOError:
            raise InvalidConfig("Config file not found.")
        except ValueError:
            raise InvalidConfig("Invalid JSON in config file.")

    @property
    def host(self):
        """
        Get the host address for the web server.
        
        Returns:
            str: Host address (defaults to '127.0.0.1')
        """
        return self.config.get("host", "127.0.0.1")

    @property
    def port(self):
        """
        Get the port number for the web server.
        
        Returns:
            int: Port number (defaults to 5000)
        """
        return self.config.get("port", 5000)

    @property
    def provider(self):
        """
        Get the SMS provider configuration.
        
        Returns:
            dict: Provider configuration including name, key, secret, phone, etc.
        """
        return self.config.get("provider", {})

    def reload(self):
        """
        Reload configuration from the file.
        
        This method re-reads the configuration file and updates
        the internal configuration data and dynamic attributes.
        
        Raises:
            InvalidConfig: If the config file is not found or contains invalid JSON
        """
        """Reload configuration from file"""
        self.config = self._load_config()
        self.__dict__.update(self.config)
