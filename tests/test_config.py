import unittest
import json
import os

from sulley.config import Config

class TestConfig(unittest.TestCase):
    def _create_config_file(self, config, file_name='config.json'):
        # write a config object to the the file in cwd
        with open(file_name, 'w') as f:
            f.write(json.dumps(config))

    def setUp(self):
        self.project_root = os.getcwd()
        self.tmp_config_path = os.path.join(
            self.project_root, 'tests', 'config.json')

        # change to tests folder before running the test case
        os.chdir(os.path.join(self.project_root, 'tests'))
        
    def tearDown(self):
        try:
            # remove the config file generated
            os.remove(self.tmp_config_path)
        except OSError:
            # ignore the error
            pass

        try:
            # remove the env config file
            os.remove(os.path.join(self.project_root, 'tests', 'env.json'))
        except OSError:
            # ignore the error
            pass

        # unset the environ variable
        if os.environ.get('SULLEY_CONFIG', None):
            del os.environ['SULLEY_CONFIG']
        
        # reset the current working directory
        os.chdir(self.project_root)
        
    def test_config_property(self):
        self._create_config_file({
            'param_01': True,
            'param_02': False,
            'param_03': {
                'nested_param_01': True
            }
        })

        config = Config()
        
        self.assertTrue(hasattr(config, 'param_01'))
        self.assertTrue(hasattr(config, 'param_02'))

    def test_config_property_value(self):
        self._create_config_file({
            'param_01': True,
            'param_02': False,
            'param_03': {
                'nested_param_01': True
            }
        })

        config = Config()
        
        self.assertTrue(config.param_01)
        self.assertFalse(config.param_02)
        self.assertTrue(isinstance(config.param_03, dict))
        self.assertTrue(config.param_03.has_key('nested_param_01'))
        self.assertTrue(config.param_03['nested_param_01'])

    def test_config_load_from_env(self):
        self._create_config_file({
            'param_0a': True,
            'param_0b': False,
            'param_0c': {
                'nested_param_0a': True
            }
        }, 'env.json')

        # set this config file path via the env variable
        os.environ['SULLEY_CONFIG'] = os.path.join(self.project_root, 'tests', 'env.json')

        config = Config()

        # should load the config from env
        self.assertTrue(hasattr(config, 'param_0a'))
        self.assertTrue(config.param_0a)

    def test_config_load_precendence(self):
        # create two config files.
        # the one set on the env should take preference
        self._create_config_file({
            'param_01': True,
            'param_02': False,
            'param_03': {
                'nested_param_01': True
            }
        })

        config = Config()
        
        self.assertTrue(hasattr(config, 'param_01'))
        self.assertTrue(config.param_01)

        # create another config file
        self._create_config_file({
            'param_0a': True,
            'param_0b': False,
            'param_0c': {
                'nested_param_0a': True
            }
        }, 'env.json')

        # set this config file path via the env variable
        os.environ['SULLEY_CONFIG'] = os.path.join(self.project_root, 'tests', 'env.json')

        config = Config()

        self.assertTrue(hasattr(config, 'param_0a'))
        self.assertTrue(config.param_0a)
        self.assertFalse(hasattr(config, 'param_01'))
        
        
