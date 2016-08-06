import unittest
from mock import Mock, MagicMock

import urllib
from flask import Flask

from sulley.matcher import Matcher
from sulley.providers.base import BaseProvider
from sulley.exceptions import InvalidConfig
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
                "url": "/sulley-test-url/",
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

    def test_sulley_default_decorator_wrap_side_effects(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=self.mockedApp,
            matcher=self.mockedMatcher,
            provider=self.mockedProvider)

        # define a function to be sent as a handler
        @sulley.default
        def test_handler(message):
            pass

        self.assertEqual(test_handler.__name__, 'test_handler')

    def test_sulley_reply_to_decorator_wrap_side_effects(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=self.mockedApp,
            matcher=self.mockedMatcher,
            provider=self.mockedProvider)

        # define a function to be sent as a handler
        @sulley.reply_to('something')
        def test_handler(message):
            pass

        self.assertEqual(test_handler.__name__, 'test_handler')

    def test_sulley_pick_provider_from_configration(self):
        sulley = Sulley(
            config=self.mockedConfig,  # contains twilio configured
            app=self.mockedApp,
            matcher=self.mockedMatcher)

        # verify if the correct provider was picked
        # TODO: is there any other clean way to check this other than
        # accessing the 'pseudo-private' property
        self.assertEqual(sulley._provider.__class__.__name__, 'Twilio')

    def test_sulley_throw_error_on_invalid_provider(self):
        self.mockedConfig.provider['name'] = 'invalid'

        with self.assertRaisesRegexp(InvalidConfig, 'Invalid provider.'):
            Sulley(config=self.mockedConfig,  # contains an invalid provider
                   app=self.mockedApp,
                   matcher=self.mockedMatcher)

    def test_sulley_throw_error_on_invalid_phone_number(self):
        self.mockedConfig.provider['phone'] = '0202'
        with self.assertRaisesRegexp(
                InvalidConfig,
                'Invalid phone number. Phone numbers should be in E.164 format.'):
            Sulley(config=self.mockedConfig,  # contains an invalid provider
                   app=self.mockedApp,
                   matcher=self.mockedMatcher)

    def test_sulley_inbound_sms_url_and_method_from_config(self):
        # should configure the url & method specified in the config
        # for inbound sms requests from providers
        sulley = Sulley(
            config=self.mockedConfig,
            app=self.mockedApp,
            matcher=self.mockedMatcher,
            provider=self.mockedProvider)

        self.mockedApp.add_url_rule.assert_called_once_with(
            self.mockedConfig.provider['url'],
            view_func=sulley._sms_handler,
            methods=self.mockedConfig.provider['methods']
        )

    def test_sulley_url_not_found(self):
        # should return a 404 when trying to access url that doesn't exist
        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=self.mockedMatcher,
        provider=self.mockedProvider)

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.get('/non-existent/').status_code, 404)

    def test_sulley_url_method_not_allowed(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=self.mockedMatcher,
        provider=self.mockedProvider)

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.post(
            self.mockedConfig.provider['url']).status_code, 405)

    def test_sulley_url_returns_400_when_mandatory_params_missing(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=self.mockedMatcher,
        provider=self.mockedProvider)

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.get(
            self.mockedConfig.provider['url']).status_code, 400)

    def test_sulley_url_returns_200_when_mandatory_params_passed(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=self.mockedMatcher,
        provider=self.mockedProvider)

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.get(
            self.mockedConfig.provider['url'] + '?' + urllib.urlencode({
                'From': '+12345678901', 'Body': 'Hey'})).status_code, 200)

    def test_sulley_xml_for_twilio(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=self.mockedMatcher,
            provider=self.mockedProvider)

        @sulley.default
        def default(message):
            pass

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.get(
            self.mockedConfig.provider['url'] + '?' + urllib.urlencode({
                'From': '+12345678901', 'Body': 'Hey'})).data,
                         '<?xml version="1.0" encoding="UTF-8"?><Response></Response>')

    def test_sulley_xml_for_plivo(self):
        self.mockedConfig.provider['name'] = 'plivo'

        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=self.mockedMatcher,
            provider=self.mockedProvider)

        @sulley.default
        def default(message):
            pass

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.get(
            self.mockedConfig.provider['url'] + '?' + urllib.urlencode({
                'From': '+12345678901', 'Text': 'Hey'})).data,
                         '<?xml version="1.0" encoding="UTF-8"?><Response></Response>')

    def test_sulley_pattern_exact_match(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=Matcher(),
            provider=self.mockedProvider)

        @sulley.reply_to('abc')
        def abc(message):
            message.reply('world')

        @sulley.default
        def default(message):
            message.reply('hello')

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.get(
            self.mockedConfig.provider['url'] + '?' + urllib.urlencode({
                'From': '+12345678901', 'Body': 'abc'})).data,
                         '<?xml version="1.0" encoding="UTF-8"?><Response></Response>')

        self.mockedProvider.send.assert_called_once_with('+12345678901', 'world')

    def test_sulley_pattern_regex_match(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=Matcher(),
            provider=self.mockedProvider)

        @sulley.reply_to('abc')
        def abc(message):
            message.reply('world')

        @sulley.reply_to('[0-9]*')
        def abc(message):
            message.reply('earth')

        @sulley.default
        def default(message):
            message.reply('hello')

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.get(
            self.mockedConfig.provider['url'] + '?' + urllib.urlencode({
                'From': '+12345678901', 'Body': '123'})).data,
                         '<?xml version="1.0" encoding="UTF-8"?><Response></Response>')

        self.mockedProvider.send.assert_called_once_with('+12345678901', 'earth')

    def test_sulley_pattern_doesnt_match(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=Matcher(),
            provider=self.mockedProvider)

        @sulley.reply_to('abc')
        def abc(message):
            message.reply('world')

        @sulley.default
        def default(message):
            message.reply('hello')

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.get(
            self.mockedConfig.provider['url'] + '?' + urllib.urlencode({
                'From': '+12345678901', 'Body': 'Hey'})).data,
                         '<?xml version="1.0" encoding="UTF-8"?><Response></Response>')

        self.mockedProvider.send.assert_called_once_with('+12345678901', 'hello')

    def test_sulley_multi_pattern_registration(self):
        sulley = Sulley(
            config=self.mockedConfig,
            app=Flask(self.__class__.__name__),
            matcher=Matcher(),
            provider=self.mockedProvider)

        @sulley.reply_to('xyz')
        @sulley.reply_to('abc')
        def abc(message):
            message.reply('world')

        @sulley.default
        def default(message):
            message.reply('hello')

        test_app = sulley._app.test_client()
        self.assertEqual(test_app.get(
            self.mockedConfig.provider['url'] + '?' + urllib.urlencode({
                'From': '+12345678901', 'Body': 'xyz'})).data,
                         '<?xml version="1.0" encoding="UTF-8"?><Response></Response>')

        self.mockedProvider.send.assert_called_once_with('+12345678901', 'world')

        self.assertEqual(test_app.get(
            self.mockedConfig.provider['url'] + '?' + urllib.urlencode({
                'From': '+12345678901', 'Body': 'abc'})).data,
                         '<?xml version="1.0" encoding="UTF-8"?><Response></Response>')

        self.mockedProvider.send.assert_called_with('+12345678901', 'world')
