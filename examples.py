import re

from sulley import Sulley

bot = Sulley()

# bind handlers to keyword / pattern based queries
@bot.reply_to('ping')
def ping(message):
    message.reply('pong')


# access the query text using the message parameter
@bot.reply_to('echo')
def echo(message):
    message.reply(message.text)


# bind multiple keywords / queries to a single handler
@bot.reply_to('hi')  # matches hi, his, him, hide, etc.
@bot.reply_to('hello')
def say_hi(message):
    message.reply('hey!')


# matches only 'ola' not 'hola' or 'olas'.
@bot.reply_to('^ola$')
def ola(message):
    message.reply('hello')

# even better, pass a python compiled regex
# matches 'List', 'list', 'LIST', 'LiSt', etc.
@bot.reply_to(re.compile('^list', re.IGNORECASE))
def launch(message):
    message.reply('listing items')

# catch all unexpected keywords / queries with a default handler
@bot.default
def say_default(message):
    message.reply('booo.')

if __name__ == '__main__':
    bot.run(debug=True)
