import json
import os


class Config(object):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(self._load())

    def _load(self):
        config_path = self._get_config_path()
        with open(config_path, 'r') as config_file:
            return json.loads(config_file.read())

    def _get_config_path(self):
        return os.environ.get(
            'SULLEY_CONFIG', os.path.join(os.getcwd(), 'config.json'))

    def reload(self):
        self.__dict__.update(self._load())
