from flask import Flask, Response, request
from functools import wraps

from config import Config
from message import Message
from matcher import Matcher
from exceptions import InvalidConfig
from providers import twilio, plivo


class Sulley(object):
    def __init__(self, *args, **kwargs):
        self._config = kwargs.get('config', None) or Config()
        self._app = kwargs.get('app', None) or Flask(self.__class__.__name__)
        self._matcher = kwargs.get('matcher', None) or Matcher()

        # do nothing by default
        self._default_handler = lambda x: None

        # TODO: add support for provider
        self._provider = kwargs.get('provider', None) or \
                         self._get_provider_from_config()

        # TODO: register global flask handler and return 404 (and 400 when applicable)
        self._app.add_url_rule(
            self._config.provider['url'],
            view_func=self._sms_handler,
            methods=self._config.provider['methods'])

    def default(self, func):
        # wrap the passed handler
        @wraps(func)
        def wrapper_func(*args):
            func(*args)

        # attach the passed handler as default handler
        self._default_handler = wrapper_func

        return wrapper_func

    def reply_to(self, regex, *args, **kwargs):
        # TODO: add option to pass pattern object directly
        # create a wrapper generator
        def handler_wrapper(handler):
            # create a wrapper
            @wraps(handler)
            def wrapper_func(*args):
                # TODO: remove this
                print '----- begin -----'
                # call the function that is being wrapped
                handler(*args)
                print '-----  end  -----'

            # register the pattern and the callback
            self._matcher.register(regex, wrapper_func)

            # return the wrapper when the function gets decorated
            return wrapper_func

        # return the wrapper generator
        return handler_wrapper

    def _sms_handler(self):
        # TODO handle request params for both GET and POST request
        from_number = request.args.get('From')
        text = request.args.get('Text')

        if from_number is None or text is None:
            # both parameters are mandatory
            return '', 400

        func = self._matcher.match(text) or self._default_handler

        # TODO: wish this was async
        func(Message(from_number, text, self._provider))

        # TODO: handle providers
        xml = '<Response></Response>'
        return Response(xml, mimetype='text/xml')

    def _get_provider_from_config(self):
        provider_name = self._config.provider['name']

        if provider_name == 'twilio':
            return twilio.Twilio(
                self._config.provider['key'],
                self._config.provider['secret'],
                self._config.provider['phone'])
        elif provider_name == 'plivo':
            return plivo.Plivo(
                self._config.provider['key'],
                self._config.provider['secret'],
                self._config.provider['phone'])
        else:
            raise InvalidConfig('Invalid provider.')

    def run(self, *args, **kwargs):
        self._app.run(*args, **kwargs)
