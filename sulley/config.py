import json
import os
from .exceptions import InvalidConfig


class Config(object):
    def __init__(self, *args, **kwargs):
        self.config_file = kwargs.get("config_file", None) or self._get_config_file()
        self.config = self._load_config()
        # Set dynamic attributes for backward compatibility
        self.__dict__.update(self.config)

    def _get_config_file(self):
        return os.environ.get("SULLEY_CONFIG", "config.json")

    def _load_config(self):
        try:
            with open(self.config_file, "r") as f:
                return json.load(f)
        except IOError:
            raise InvalidConfig("Config file not found.")
        except ValueError:
            raise InvalidConfig("Invalid JSON in config file.")

    @property
    def host(self):
        return self.config.get("host", "127.0.0.1")

    @property
    def port(self):
        return self.config.get("port", 5000)

    @property
    def provider(self):
        return self.config.get("provider", {})

    def reload(self):
        """Reload configuration from file"""
        self.config = self._load_config()
        self.__dict__.update(self.config)
