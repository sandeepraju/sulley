"""
Sulley SMS Bot Framework

A simple, decorator-based framework for building SMS bots with minimal configuration.
Supports Twilio and Plivo providers out of the box.
"""

from flask import Flask, Response, request
from functools import wraps
from werkzeug.exceptions import BadRequest, MethodNotAllowed

from .config import Config
from .message import Message
from .matcher import Matcher
from .exceptions import InvalidConfig
from .providers import twilio, plivo


class Sulley(object):
    """
    Main SMS bot class that handles webhook processing and message routing.
    
    Sulley provides a simple decorator-based API for creating SMS bots. It handles
    webhook processing, message matching, and provider integration automatically.
    
    Example:
        >>> bot = Sulley()
        >>> @bot.reply_to(r'hi')
        ... def say_hello(message):
        ...     message.reply('Hello!')
        >>> bot.run()
    """

    def __init__(self, config=None, app=None, matcher=None, provider=None):
        """
        Initialize the Sulley bot instance.
        
        Args:
            config: Optional Config instance. If not provided, loads from config.json
            app: Optional Flask app instance. If not provided, creates a new one
            matcher: Optional Matcher instance. If not provided, creates a new one
            provider: Optional provider instance. If not provided, loads from config
        """
        self._config = config or Config()
        self._app = app or Flask(self.__class__.__name__)
        self._matcher = matcher or Matcher()

        # Default handler that does nothing when no patterns match
        self._default_handler = lambda x: None

        # Initialize the SMS provider (Twilio or Plivo)
        self._provider = provider or self._get_provider_from_config()

        # Register the webhook endpoint for incoming SMS
        self._app.add_url_rule(
            self._config.provider["url"],
            view_func=self._sms_handler,
            methods=self._config.provider["methods"],
        )

    def default(self, func):
        """
        Decorator to set the default handler for unmatched messages.
        
        This handler is called when no regex patterns match the incoming message.
        
        Args:
            func: The function to call for unmatched messages
            
        Returns:
            The decorated function
            
        Example:
            >>> @bot.default
            ... def handle_unknown(message):
            ...     message.reply("I didn't understand that command.")
        """
        @wraps(func)
        def wrapper_func(*args):
            func(*args)

        # Set the default handler
        self._default_handler = wrapper_func
        return wrapper_func

    def reply_to(self, regex):
        """
        Decorator to register a handler for messages matching a regex pattern.
        
        Args:
            regex: Regex pattern to match against incoming messages.
                  Can be a string or compiled regex object.
            
        Returns:
            Decorator function that registers the handler
            
        Example:
            >>> @bot.reply_to(r'hi|hello')
            ... def greet(message):
            ...     message.reply('Hello there!')
            
            >>> @bot.reply_to(re.compile(r'weather', re.IGNORECASE))
            ... def weather(message):
            ...     message.reply('The weather is sunny!')
        """
        def handler_wrapper(handler):
            @wraps(handler)
            def wrapper_func(*args):
                # Call the decorated function
                handler(*args)

            # Register the pattern and handler with the matcher
            self._matcher.register(regex, wrapper_func)
            return wrapper_func

        return handler_wrapper

    def _sms_handler(self):
        """
        Internal webhook handler for incoming SMS messages.
        
        This method is called by Flask when an SMS webhook is received.
        It extracts the message details, finds the appropriate handler,
        and executes it.
        
        Returns:
            Flask Response object with XML response for the SMS provider
        """
        # Extract phone number and message text from the webhook
        from_number, text = self._get_request_arguments(request)

        # Find matching handler or use default handler
        func = self._matcher.match(text) or self._default_handler
        
        # Get matched text if a pattern matched
        matched_text = None
        if func != self._default_handler:
            matched_text = getattr(self._matcher, '_last_matched_text', None)
        
        # Create message object and call the handler
        func(Message(from_number, text, provider=self._provider, matched_text=matched_text))

        # Return empty TwiML response (required by SMS providers)
        xml = '<?xml version="1.0" encoding="UTF-8"?><Response></Response>'
        return Response(xml, mimetype="text/xml")

    def _get_request_arguments(self, request):
        """
        Extract phone number and message text from the webhook request.
        
        Args:
            request: Flask request object
            
        Returns:
            tuple: (from_number, text) from the SMS
            
        Raises:
            BadRequest: If required parameters are missing
        """
        provider_name = self._config.provider["name"]
        if provider_name == "twilio":
            return self._get_twilio_arguments(request)
        elif provider_name == "plivo":
            return self._get_plivo_arguments(request)

    def _get_twilio_arguments(self, request):
        """
        Extract SMS details from Twilio webhook request.
        
        Twilio sends 'From' (phone number) and 'Body' (message text) parameters.
        
        Args:
            request: Flask request object
            
        Returns:
            tuple: (from_number, text)
            
        Raises:
            BadRequest: If From or Body parameters are missing
            MethodNotAllowed: If HTTP method is not GET or POST
        """
        if request.method == "GET":
            from_number = request.args.get("From")
            text = request.args.get("Body")
            if from_number is None or text is None:
                raise BadRequest("Both `From` and `Body` " "parameters are mandatory.")

            return from_number, text

        elif request.method == "POST":
            from_number = request.form.get("From", None)
            text = request.form.get("Body", None)
            if from_number is None or text is None:
                raise BadRequest("Both `From` and `Body` " "parameters are mandatory.")

            return from_number, text

        else:
            raise MethodNotAllowed("Only `GET` and `POST` methods are allowed.")

    def _get_plivo_arguments(self, request):
        """
        Extract SMS details from Plivo webhook request.
        
        Plivo sends 'From' (phone number) and 'Text' (message text) parameters.
        
        Args:
            request: Flask request object
            
        Returns:
            tuple: (from_number, text)
            
        Raises:
            BadRequest: If From or Text parameters are missing
            MethodNotAllowed: If HTTP method is not GET or POST
        """
        if request.method == "GET":
            from_number = request.args.get("From")
            text = request.args.get("Text")
            if from_number is None or text is None:
                raise BadRequest("Both `From` and `Text` " "parameters are mandatory.")

            return from_number, text

        elif request.method == "POST":
            from_number = request.form.get("From", None)
            text = request.form.get("Text", None)
            if from_number is None or text is None:
                raise BadRequest("Both `From` and `Text` " "parameters are mandatory.")

            return from_number, text

        else:
            raise MethodNotAllowed("Only `GET` and `POST` methods are allowed.")

    def _get_provider_from_config(self):
        """
        Create and return the appropriate SMS provider based on configuration.
        
        Returns:
            Provider instance (Twilio or Plivo)
            
        Raises:
            InvalidConfig: If provider name is not supported
        """
        provider_name = self._config.provider["name"]

        if provider_name == "twilio":
            return twilio.Twilio(
                self._config.provider["key"],
                self._config.provider["secret"],
                self._config.provider["phone"],
            )
        elif provider_name == "plivo":
            return plivo.Plivo(
                self._config.provider["key"],
                self._config.provider["secret"],
                self._config.provider["phone"],
            )
        else:
            raise InvalidConfig("Invalid provider.")

    def run(self, host=None, port=None, debug=None, quiet=False, **kwargs):
        """
        Start the Flask development server.
        
        Args:
            host: Host address to bind to (defaults to config.host)
            port: Port number to bind to (defaults to config.port)
            debug: Enable debug mode (defaults to False)
            quiet: If True, suppress the startup banner
            **kwargs: Additional arguments passed to Flask's run() method
        """
        if not quiet:
            print(
                r"""
  _____ __ __  _      _        ___  __ __
 / ___/|  |  || |    | |      /  _]|  |  |
(   \_ |  |  || |    | |     /  [_ |  |  |
 \__  ||  |  || |___ | |___ |    _]|  ~  |
 /  \ ||  :  ||     ||     ||   [_ |___, |
 \    ||     ||     ||     ||     ||     |
  \___| \__,_||_____||_____||_____||____/

            """
            )
            print(
                " * Send SMS to {} and test your application".format(
                    self._config.provider["phone"]
                )
            )
        
        # Use config values as defaults if not provided
        host = host or self._config.host
        port = port or self._config.port
        debug = debug if debug is not None else False
        
        self._app.run(host=host, port=port, debug=debug, **kwargs)
