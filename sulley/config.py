import json
import os


class Config(object):
    def __init__(self, *args, **kwargs):
        self._config = self._load()

        super(Config, self).__init__(*args, **kwargs)

    def _load(self):
        config_path = self._get_config_path()
        with open(config_path, 'r') as config_file:
            self._config = json.loads(config_file.read())
            self.__dict__.update(self._config)

    def _get_config_path(self):
        return os.environ.get(
            'SULLEY_CONFIG', os.path.join(os.getcwd(), 'config.json'))

    def reload(self):
        self._config = self._load()
