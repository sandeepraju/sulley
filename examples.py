"""
Sulley SMS Bot Examples

This file contains various examples demonstrating how to use the Sulley
SMS bot framework for different use cases.
"""

import re
from sulley import Sulley

# Example 1: Basic Greeting Bot
def basic_greeting_bot():
    """
    A simple bot that responds to basic greetings.
    """
    bot = Sulley()

    @bot.reply_to(r'hi|hello|hey')
    def greet(message):
        message.reply('Hello! How can I help you today?')

    @bot.reply_to(r'bye|goodbye|see you')
    def farewell(message):
        message.reply('Goodbye! Have a great day!')

    @bot.default
    def unknown(message):
        message.reply("I didn't understand that. Try saying 'hi' or 'bye'!")

    bot.run()


# Example 2: Weather Bot
def weather_bot():
    """
    A bot that handles weather-related queries.
    """
    bot = Sulley()

    @bot.reply_to(r'weather')
    def weather_general(message):
        message.reply('Please specify a city. Try: "weather in London"')

    @bot.reply_to(r'weather in (.+)')
    def weather_city(message):
        city = message.get_matched_text()
        # In a real app, you'd call a weather API here
        message.reply(f'Checking weather for {city}... (This is a demo)')

    @bot.reply_to(r'temperature')
    def temperature(message):
        message.reply('Please specify a city for temperature info.')

    @bot.default
    def unknown(message):
        message.reply('Try asking about the weather!')

    bot.run()


# Example 3: Calculator Bot
def calculator_bot():
    """
    A bot that performs basic calculations.
    """
    bot = Sulley()

    @bot.reply_to(r'calculate (.+)')
    def calculate(message):
        expression = message.get_matched_text()
        try:
            # Note: eval() is used for demo purposes only
            # In production, use a proper expression parser
            result = eval(expression)
            message.reply(f'{expression} = {result}')
        except:
            message.reply('Sorry, I couldn\'t calculate that.')

    @bot.reply_to(r'add (\d+) and (\d+)')
    def add(message):
        # Extract numbers from the message
        text = message.get_raw_text()
        import re
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
            result = int(numbers[0]) + int(numbers[1])
            message.reply(f'{numbers[0]} + {numbers[1]} = {result}')
        else:
            message.reply('Please provide two numbers to add.')

    @bot.default
    def unknown(message):
        message.reply('Try: "calculate 2 + 2" or "add 5 and 3"')

    bot.run()


# Example 4: Reminder Bot
def reminder_bot():
    """
    A bot that helps set reminders.
    """
    bot = Sulley()

    @bot.reply_to(r'remind me to (.+)')
    def set_reminder(message):
        task = message.get_matched_text()
        message.reply(f'Reminder set: {task}')

    @bot.reply_to(r'reminders')
    def list_reminders(message):
        message.reply('Your reminders: (This is a demo - no actual reminders stored)')

    @bot.reply_to(r'clear reminders')
    def clear_reminders(message):
        message.reply('All reminders cleared!')

    @bot.default
    def unknown(message):
        message.reply('Try: "remind me to call mom" or "reminders"')

    bot.run()


# Example 5: Advanced Pattern Matching
def advanced_patterns_bot():
    """
    A bot demonstrating advanced regex pattern matching.
    """
    bot = Sulley()

    # Case-insensitive matching
    @bot.reply_to(re.compile(r'help', re.IGNORECASE))
    def help_case_insensitive(message):
        message.reply('I can help you with various tasks!')

    # Multiple word matching
    @bot.reply_to(r'\b(what|how|when|where|why)\b')
    def question_words(message):
        word = message.get_matched_text()
        message.reply(f'You used the question word "{word}". How can I help?')

    # Number patterns
    @bot.reply_to(r'(\d+) times (\d+)')
    def multiply(message):
        text = message.get_raw_text()
        import re
        numbers = re.findall(r'\d+', text)
        if len(numbers) >= 2:
            result = int(numbers[0]) * int(numbers[1])
            message.reply(f'{numbers[0]} × {numbers[1]} = {result}')

    # Email validation
    @bot.reply_to(r'email (.+@.+\..+)')
    def email_validation(message):
        email = message.get_matched_text()
        message.reply(f'Valid email format: {email}')

    @bot.default
    def unknown(message):
        message.reply('Try asking for help, using question words, or math!')

    bot.run()


# Example 6: Multi-language Bot
def multilingual_bot():
    """
    A bot that responds in multiple languages.
    """
    bot = Sulley()

    # English
    @bot.reply_to(r'hello|hi')
    def english_greet(message):
        message.reply('Hello! Welcome to our multilingual bot!')

    # Spanish
    @bot.reply_to(r'hola|buenos dias')
    def spanish_greet(message):
        message.reply('¡Hola! ¡Bienvenido a nuestro bot multilingüe!')

    # French
    @bot.reply_to(r'bonjour|salut')
    def french_greet(message):
        message.reply('Bonjour! Bienvenue sur notre bot multilingue!')

    # German
    @bot.reply_to(r'hallo|guten tag')
    def german_greet(message):
        message.reply('Hallo! Willkommen bei unserem mehrsprachigen Bot!')

    @bot.default
    def unknown(message):
        message.reply('Try: hello, hola, bonjour, or hallo')

    bot.run()


# Example 7: Customer Service Bot
def customer_service_bot():
    """
    A customer service bot with common support scenarios.
    """
    bot = Sulley()

    @bot.reply_to(r'order|purchase|buy')
    def order_help(message):
        message.reply('For order help, please call 1-800-ORDER or visit our website.')

    @bot.reply_to(r'refund|return|money back')
    def refund_help(message):
        message.reply('For refunds, please email refunds@company.com with your order number.')

    @bot.reply_to(r'complaint|problem|issue')
    def complaint_help(message):
        message.reply('We\'re sorry to hear that. Please call 1-800-SUPPORT for immediate assistance.')

    @bot.reply_to(r'hours|open|closed')
    def hours_info(message):
        message.reply('We\'re open Monday-Friday 9AM-6PM EST. Closed weekends.')

    @bot.reply_to(r'contact|phone|email')
    def contact_info(message):
        message.reply('Contact us: Phone: 1-800-HELP, Email: support@company.com')

    @bot.default
    def unknown(message):
        message.reply('How can I help? Try: order, refund, complaint, hours, or contact')

    bot.run()


# Example 8: Quiz Bot
def quiz_bot():
    """
    A simple quiz bot with multiple choice questions.
    """
    bot = Sulley()

    @bot.reply_to(r'start quiz|begin quiz|quiz')
    def start_quiz(message):
        message.reply('Welcome to the quiz! Question 1: What is 2+2? Reply with A, B, C, or D')

    @bot.reply_to(r'[Aa]')
    def answer_a(message):
        message.reply('Correct! 2+2 = 4. Next question: What is the capital of France? A) London B) Paris C) Berlin D) Madrid')

    @bot.reply_to(r'[Bb]')
    def answer_b(message):
        message.reply('Correct! Paris is the capital of France. Quiz complete!')

    @bot.reply_to(r'[Cc]|[Dd]')
    def wrong_answer(message):
        message.reply('Incorrect! Try again.')

    @bot.default
    def unknown(message):
        message.reply('Type "start quiz" to begin, or answer with A, B, C, or D')

    bot.run()


# Example 9: Restaurant Bot
def restaurant_bot():
    """
    A restaurant bot for menu and reservation queries.
    """
    bot = Sulley()

    @bot.reply_to(r'menu|food|dishes')
    def show_menu(message):
        menu = """Today's Menu:
🍕 Pizza - $15
🍔 Burger - $12
🥗 Salad - $8
🍝 Pasta - $14
Call 555-0123 to order!"""
        message.reply(menu)

    @bot.reply_to(r'reservation|book|table')
    def reservation(message):
        message.reply('For reservations, call 555-0123 or visit our website. We accept bookings up to 2 weeks in advance.')

    @bot.reply_to(r'hours|open|closed')
    def hours(message):
        message.reply('Hours: Mon-Sat 11AM-10PM, Sunday 12PM-9PM')

    @bot.reply_to(r'location|address|where')
    def location(message):
        message.reply('We\'re located at 123 Main Street, Downtown. Free parking available!')

    @bot.reply_to(r'delivery|deliver|takeout')
    def delivery(message):
        message.reply('Delivery available within 5 miles. Call 555-0123 or order online!')

    @bot.default
    def unknown(message):
        message.reply('Try: menu, reservation, hours, location, or delivery')

    bot.run()


# Example 10: Fitness Tracker Bot
def fitness_bot():
    """
    A fitness tracking bot for logging workouts and goals.
    """
    bot = Sulley()

    @bot.reply_to(r'log workout|workout|exercise')
    def log_workout(message):
        message.reply('Great! What type of workout? Reply with: cardio, strength, yoga, or other')

    @bot.reply_to(r'cardio|running|cycling|swimming')
    def cardio_workout(message):
        message.reply('Cardio logged! How many minutes? Reply with the number.')

    @bot.reply_to(r'strength|weights|lifting')
    def strength_workout(message):
        message.reply('Strength training logged! How many minutes? Reply with the number.')

    @bot.reply_to(r'yoga|stretching|flexibility')
    def yoga_workout(message):
        message.reply('Yoga logged! How many minutes? Reply with the number.')

    @bot.reply_to(r'(\d+)')
    def log_duration(message):
        duration = message.get_matched_text()
        message.reply(f'Workout logged: {duration} minutes. Keep up the great work!')

    @bot.reply_to(r'progress|stats|summary')
    def show_progress(message):
        message.reply('This week: 3 workouts, 120 minutes total. You\'re doing great!')

    @bot.reply_to(r'goal|target')
    def set_goal(message):
        message.reply('What\'s your fitness goal? Reply with: lose weight, build muscle, or stay active')

    @bot.default
    def unknown(message):
        message.reply('Try: log workout, progress, or goal')

    bot.run()


if __name__ == '__main__':
    # Uncomment the example you want to run:
    
    # basic_greeting_bot()
    # weather_bot()
    # calculator_bot()
    # reminder_bot()
    # advanced_patterns_bot()
    # multilingual_bot()
    # customer_service_bot()
    # quiz_bot()
    # restaurant_bot()
    # fitness_bot()
    
    # For now, run the basic greeting bot
    basic_greeting_bot()
