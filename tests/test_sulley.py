import unittest
from mock import Mock, MagicMock

from flask import Flask

from sulley.matcher import Matcher
from sulley.providers.base import BaseProvider
from sulley import Sulley

class TestSulley(unittest.TestCase):
    def setUp(self):
        self.mockedConfig = self._generateMockedConfig({
            "host": "127.0.0.1",
            "port": "5000",
            "provider": {
                "name": "twilio",
                "key": "twilio-account-sid",
                "secret": "twilio-auth-token",
                "phone": "+12345678901",
                "url": "/sulley/",
                "methods": ["GET"]
            },
            "users": [
                {
                    "name": "John Doe",
                    "phone": "+10000000000",
                    "role": "admin"
                }
            ]
        })
        self.mockedApp = self._generateMockedApp(self.__class__.__name__)
        self.mockedMatcher = self._generateMockedMatcher()
        self.mockedProvider = self._generateMockedProvider()

    def _generateMockedConfig(self, config):
        return Mock(**config)

    def _generateMockedApp(self, name='sulley_test'):
        app = Flask(name)
        app.add_url_rule = MagicMock(return_value=None)
        app.run = MagicMock(return_value=None)
        return app

    def _generateMockedMatcher(self):
        matcher = Matcher()
        matcher.register = MagicMock(return_value=None)
        matcher.deregister = MagicMock(return_value=None)
        # mock the match as required in each test case

        return matcher

    def _generateMockedProvider(self):
        provider = BaseProvider('test-key', 'test-secret', '+10000000000')
        provider.send = MagicMock(return_value=None)
        return provider

    def tearDown(self):
        pass

    def test_sulley_run_without_params(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=self.mockedApp,
            matcher=self.mockedMatcher,
            provider=self.mockedProvider)

        # with no arguments
        sulley.run()
        self.mockedApp.run.assert_called_once_with()

    def test_sulley_run_with_params(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=self.mockedApp,
            matcher=self.mockedMatcher,
            provider=self.mockedProvider)

        # with few flask params
        sulley.run(debug=True)
        self.mockedApp.run.assert_called_once_with(debug=True)
