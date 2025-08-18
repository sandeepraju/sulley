# Sulley SMS Bot Tutorial: End-to-End Setup

This tutorial will guide you through creating a complete SMS bot using Sulley, from setup to deployment. We'll use Twilio as our SMS provider and ngrok for local development.

## Prerequisites

- Python 3.8 or higher
- A Twilio account (free trial available)
- ngrok (free tier available)
- Basic knowledge of Python and command line

## Step 1: Set Up Your Development Environment

### Install Poetry (if not already installed)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Clone and Set Up Sulley
```bash
git clone https://github.com/sandeepraju/sulley.git
cd sulley
poetry install
poetry shell
```

## Step 2: Create Your Twilio Account

1. Go to [Twilio's website](https://www.twilio.com/) and sign up for a free account
2. Verify your phone number during signup
3. Get your Account SID and Auth Token from the Twilio Console
4. Purchase a Twilio phone number (free trial includes $15 credit)

## Step 3: Create Your Bot

Create a new file called `my_bot.py`:

```python
from sulley import Sulley

# Create your bot instance
bot = Sulley()

# Handle greetings
@bot.reply_to(r'hi|hello|hey')
def greet(message):
    message.reply('Hello! Welcome to my SMS bot! 👋')

# Handle weather queries
@bot.reply_to(r'weather in (.+)')
def weather(message):
    city = message.get_matched_text()
    message.reply(f'Checking weather for {city}... ☀️ (This is a demo)')

# Handle math calculations
@bot.reply_to(r'calculate (.+)')
def calculate(message):
    expression = message.get_matched_text()
    try:
        result = eval(expression)
        message.reply(f'{expression} = {result}')
    except:
        message.reply('Sorry, I couldn\'t calculate that.')

# Handle unknown messages
@bot.default
def unknown(message):
    message.reply('I didn\'t understand that. Try: hi, weather in London, or calculate 2+2')

if __name__ == '__main__':
    bot.run(debug=True)
```

## Step 4: Configure Your Bot

Create a `config.json` file in the same directory:

```json
{
    "host": "127.0.0.1",
    "port": 5000,
    "provider": {
        "name": "twilio",
        "key": "YOUR_TWILIO_ACCOUNT_SID",
        "secret": "YOUR_TWILIO_AUTH_TOKEN",
        "phone": "+1234567890",
        "url": "/webhook",
        "methods": ["POST"]
    }
}
```

Replace the placeholder values:
- `YOUR_TWILIO_ACCOUNT_SID`: Your Twilio Account SID
- `YOUR_TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
- `+1234567890`: Your Twilio phone number

## Step 5: Set Up ngrok for Local Development

### Install ngrok
Download ngrok from [ngrok.com](https://ngrok.com/) and follow their installation instructions.

### Start Your Bot
```bash
python my_bot.py
```

You should see output like:
```
  _____ __ __  _      _        ___  __ __
 / ___/|  |  || |    | |      /  _]|  |  |
(   \_ |  |  || |    | |     /  [_ |  |  |
 \__  ||  |  || |___ | |___ |    _]|  ~  |
 /  \ ||  :  ||     ||     ||   [_ |___, |
 \    ||     ||     ||     ||     ||     |
  \___| \__,_||_____||_____||_____||____/

 * Send SMS to +1234567890 and test your application
 * Running on http://127.0.0.1:5000
```

### Expose Your Local Server
In a new terminal window, run:
```bash
ngrok http 5000
```

You'll see output like:
```
Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok.io -> http://localhost:5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`).

## Step 6: Configure Twilio Webhook

1. Go to your Twilio Console
2. Navigate to Phone Numbers → Manage → Active numbers
3. Click on your phone number
4. In the "Messaging" section, set the webhook URL to:
   ```
   https://abc123.ngrok.io/webhook
   ```
   (Replace with your actual ngrok URL)
5. Set the HTTP method to POST
6. Save the configuration

## Step 7: Test Your Bot

Send an SMS to your Twilio phone number with different messages:

- Send "hi" → Should reply with greeting
- Send "weather in London" → Should reply about weather
- Send "calculate 15 + 27" → Should reply with the result
- Send "random text" → Should reply with the default message

## Step 8: Monitor and Debug

### View ngrok Traffic
Visit `http://127.0.0.1:4040` to see all incoming webhook requests and responses.

### Check Flask Logs
Your bot's console will show incoming requests and any errors.

### Test Webhook Endpoint
You can test your webhook directly using curl:
```bash
curl -X POST https://abc123.ngrok.io/webhook \
  -d "From=%2B1234567890&Body=hi" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

## Step 9: Enhance Your Bot

### Add More Features
```python
# Handle reminders
@bot.reply_to(r'remind me to (.+)')
def set_reminder(message):
    task = message.get_matched_text()
    message.reply(f'Reminder set: {task}')

# Handle help requests
@bot.reply_to(r'help|commands')
def help(message):
    help_text = """Available commands:
- hi/hello/hey: Get a greeting
- weather in [city]: Check weather
- calculate [expression]: Do math
- remind me to [task]: Set a reminder
- help: Show this message"""
    message.reply(help_text)
```

### Add Error Handling
```python
@bot.reply_to(r'calculate (.+)')
def calculate(message):
    expression = message.get_matched_text()
    try:
        # Only allow safe operations
        if any(op in expression for op in ['import', 'eval', 'exec', 'open']):
            message.reply('Sorry, that operation is not allowed.')
            return
        
        result = eval(expression)
        message.reply(f'{expression} = {result}')
    except ZeroDivisionError:
        message.reply('Cannot divide by zero!')
    except:
        message.reply('Sorry, I couldn\'t calculate that.')
```

## Step 10: Deploy to Production

### Option 1: Heroku
1. Create a `requirements.txt` file:
```bash
poetry export -f requirements.txt --output requirements.txt
```

2. Create a `Procfile`:
```
web: python my_bot.py
```

3. Deploy to Heroku:
```bash
heroku create my-sms-bot
git add .
git commit -m "Deploy SMS bot"
git push heroku main
```

4. Update your Twilio webhook URL to your Heroku app URL.

### Option 2: AWS/GCP/Azure
Deploy your Flask app to any cloud platform and update your Twilio webhook URL accordingly.

## Troubleshooting

### Common Issues

**Bot not responding to messages:**
- Check that ngrok is running and the URL is correct
- Verify your Twilio webhook URL is set correctly
- Check your bot's console for error messages

**"Invalid provider" error:**
- Verify your config.json has the correct provider name ("twilio")
- Check that your Twilio credentials are correct

**Webhook not receiving requests:**
- Ensure your ngrok URL is HTTPS
- Check that your webhook URL ends with `/webhook`
- Verify the HTTP method is set to POST in Twilio

**Regex patterns not matching:**
- Remember that patterns match from the beginning by default
- Use `^` and `$` anchors for exact matches
- Test your regex patterns in a regex tester first

### Debug Tips

1. **Enable debug mode**: Run your bot with `debug=True`
2. **Check ngrok logs**: Visit the ngrok web interface
3. **Test webhook manually**: Use curl to test your endpoint
4. **Add logging**: Add print statements to your handlers

## Next Steps

- Add database integration for persistent storage
- Implement user authentication
- Add more sophisticated NLP capabilities
- Integrate with external APIs (weather, news, etc.)
- Add analytics and monitoring
- Implement conversation state management

## Resources

- [Sulley Documentation](https://github.com/sandeepraju/sulley)
- [Twilio SMS API Documentation](https://www.twilio.com/docs/sms)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Regular Expressions](https://docs.python.org/3/library/re.html)

Happy bot building! 🤖📱
