"""
Pattern matching system for Sulley SMS bot.

This module provides the Matcher class that handles regex pattern matching
for incoming SMS messages and routes them to appropriate handlers.
"""

import re


class Matcher(object):
    """
    Handles regex pattern matching for SMS message routing.
    
    The Matcher class maintains a registry of regex patterns and their
    associated handler functions. When a message is received, it finds
    the first matching pattern and returns the corresponding handler.
    
    Attributes:
        _pairs (list): List of (pattern, handler) tuples
    """

    def __init__(self):
        """
        Initialize a new Matcher instance.
        """
        self._pairs = []

    def register(self, pattern, func):
        """
        Register a regex pattern with its handler function.
        
        Args:
            pattern: Regex pattern (string or compiled regex object)
            func: Function to call when pattern matches
            
        Example:
            >>> matcher = Matcher()
            >>> matcher.register(r'hello', lambda msg: print('Hi!'))
            >>> matcher.register(re.compile(r'weather', re.IGNORECASE), weather_handler)
        """
        if pattern.__class__.__name__ == "Pattern":
            # A compiled pattern object is passed directly
            self._pairs.append((pattern, func))
        else:
            # A pattern string is passed - compile it
            self._pairs.append((re.compile(str(pattern)), func))

    def deregister(self, pattern):
        """
        Remove all patterns matching the given pattern string.
        
        Args:
            pattern (str): Pattern string to remove (must match exactly)
            
        Note:
            This method removes ALL patterns with the same string representation.
            If you have multiple compiled patterns with the same string, they
            will all be removed.
        """
        try:
            # Remove all patterns that match the given pattern string
            # For compiled patterns, compare the pattern string
            # For string patterns, compare directly
            if isinstance(pattern, str):
                self._pairs = [(p, f) for p, f in self._pairs if p.pattern != pattern]
            else:
                # If pattern is a compiled regex, remove exact matches
                self._pairs = [(p, f) for p, f in self._pairs if p != pattern]
        except Exception:
            # Pattern not found - fail silently
            pass

    def match(self, text):
        """
        Find the first matching pattern for the given text.
        
        Args:
            text (str): The text to match against registered patterns
            
        Returns:
            function or None: The handler function for the first matching pattern,
                             or None if no patterns match
                             
        Example:
            >>> matcher = Matcher()
            >>> matcher.register(r'hello', hello_handler)
            >>> matcher.register(r'bye', bye_handler)
            >>> handler = matcher.match('hello world')  # Returns hello_handler
            >>> handler = matcher.match('goodbye')      # Returns bye_handler
            >>> handler = matcher.match('unknown')      # Returns None
        """
        for pair in self._pairs:
            match = pair[0].match(text)
            if match:
                # Store the matched text for later use
                self._last_matched_text = match.group(0)
                return pair[1]
        return None

    def get_matched_text(self, text):
        """
        Get the matched text for a given input text.
        
        Args:
            text (str): The text to match against registered patterns
            
        Returns:
            str or None: The matched text if a pattern matches, None otherwise
            
        Example:
            >>> matcher = Matcher()
            >>> matcher.register(r'hello (.+)', lambda msg: None)
            >>> matched = matcher.get_matched_text('hello world')  # Returns 'hello world'
        """
        for pair in self._pairs:
            match = pair[0].match(text)
            if match:
                return match.group(0)
        return None
