from flask import Flask, Response, request

from config import Config
from message import Message
from matcher import Matcher
from providers import plivo

class Sulley(object):
    def __init__(self, *args, **kwargs):
        self._config = Config()
        self._app = Flask(self.__class__.__name__)
        self._matcher = Matcher()
        self._default_handler = lambda x: x
        self._provider = plivo.Plivo(
            key=self._config.provider['key'],
            secret=self._config.provider['secret'],
            phone=self._config.provider['phone'][1:])  # NOTE: ignore +1 for plivo

        # TODO: register global flask handler
        self._app.add_url_rule(
            self._config.provider['url'],
            view_func=self._sms_handler,
            methods=self._config.provider['methods'])

    def default(self, func):
        self.default
        def wrapper_func(*args):
            func(*args)

        wrapper_func.__name__ == func.__name__

        self._default_handler = wrapper_func
        
        return wrapper_func
        
    def reply_to(self, regex, *args, **kwargs):
        # TODO: add option to turn case senstivity on and off
        # pass pattern object directly
        # create a wrapper generator
        def handler_wrapper(handler):
            # create a wrapper
            def wrapper_func(*args):
                print '----- begin -----'
                # call the function that is being wrapped
                handler(*args)
                print '-----  end  -----'

            # fake the name of the wrapper function
            wrapper_func.__name__ = handler.__name__

            # register the pattern and the callback
            self._matcher.register(regex, wrapper_func)

            # return the wrapper when the function gets decorated
            return wrapper_func
        
        # return the wrapper generator
        return handler_wrapper

    def _sms_handler(self):
        # TODO multiple methods
        from_number = request.args.get('From')
        message = request.args.get('Text')
        func = self._matcher.match(message) or self._default_handler

        # TODO: wish this was async
        func(Message(from_number, message, self._provider))
        
        # TODO: handle providers
        xml = '<Response></Response>'
        return Response(xml, mimetype='text/xml')

    def run(self, *args, **kwargs):
        self._app.run(*args, **kwargs)
