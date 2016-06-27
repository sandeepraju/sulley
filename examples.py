from sulley import Sulley

bot = Sulley()

@bot.reply_to("hi")
@bot.reply_to("hello")
def say_hi(message):
    message.reply("hey!")

@bot.default
def say_default(message):
    message.reply("bow bow.")

if __name__ == '__main__':
    bot.run(debug=True)
