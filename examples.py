from sulley import Sulley

bot = Sulley()


# bind handlers to keyword / pattern based queries
@bot.reply_to('ping')
def ping(message):
    message.reply('pong')


# access the query text using the message parameter
@bot.reply_to('echo')
def echo(message):
    # TODO: implement raw_text & text
    message.reply(message.text)


# bind multiple keywords / queries to a single handler
@bot.reply_to('hi')  # matches hi, his, him, hide, etc.
@bot.reply_to('hello')
def say_hi(message):
    message.reply('hey!')

@bot.reply_to('^ola$') # matches only 'ola' not 'hola' or 'olas'.
def ola(message):
    message.reply('hello')


# catch all unexpected keywords / queries with a default handler
@bot.default
def say_default(message):
    message.reply('woof woof.')

if __name__ == '__main__':
    bot.run(debug=True)
