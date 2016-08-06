from flask import Flask, Response, request
from functools import wraps
from werkzeug.exceptions import BadRequest, MethodNotAllowed

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
                # call the function that is being wrapped
                handler(*args)

            # register the pattern and the callback
            self._matcher.register(regex, wrapper_func)

            # return the wrapper when the function gets decorated
            return wrapper_func

        # return the wrapper generator
        return handler_wrapper

    def _sms_handler(self):
        from_number, text = self._get_request_arguments(request)

        func = self._matcher.match(text) or self._default_handler
        func(Message(from_number, text, provider=self._provider))

        # TODO: handle providers
        xml = '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'
        return Response(xml, mimetype='text/xml')

    def _get_request_arguments(self, request):
        provider_name = self._config.provider['name']
        if provider_name == 'twilio':
            return self._get_twilio_arguments(request)
        elif provider_name == 'plivo':
            return self._get_plivo_arguments(request)

    def _get_twilio_arguments(self, request):
        if request.method == 'GET':
            from_number = request.args.get('From')
            text = request.args.get('Body')
            if from_number is None or text is None:
                raise BadRequest('Both `From` and `Body` parameters are mandatory.')

            return from_number, text

        elif request.method == 'POST':
            from_number = request.form.get('From', None)
            text = request.form.get('Body', None)
            if from_number is None or text is None:
                raise BadRequest('Both `From` and `Body` parameters are mandatory.')

            return from_number, text

        else:
            raise MethodNotAllowed('Only GET and POST methods are allowed.')

    def _get_plivo_arguments(self, request):
        if request.method == 'GET':
            from_number = request.args.get('From')
            text = request.args.get('Text')
            if from_number is None or text is None:
                raise BadRequest('Both `From` and `Text` parameters are mandatory.')

            return from_number, text

        elif request.method == 'POST':
            from_number = request.form.get('From', None)
            text = request.form.get('Text', None)
            if from_number is None or text is None:
                raise BadRequest('Both `From` and `Text` parameters are mandatory.')

            return from_number, text

        else:
            raise MethodNotAllowed('Only GET and POST methods are allowed.')

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
