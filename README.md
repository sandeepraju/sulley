Sulley (Beta)
=========================

![James P. Sullivan from Monsters, Inc.](http://i.imgur.com/KvSWLHo.png)

With Sulley, you can build SMS bots in just a few lines of code. Powered by Twilio & Plivo, it requires very minimal configuration and code to bring your SMS bot to life!

This project is inspired from Shuai Lin's [slackbot](https://github.com/lins05/slackbot).

## Installation

### From PyPI

Sulley can be installed from PyPI by running the following command:

```bash
pip install sulley
```

### From source code

* Get the source code by cloning the repository

```bash
git clone https://github.com/sandeepraju/sulley.git
```

* In the project directory, run the `setup.py`

```bash
cd sulley/
python setup.py install
```

## Getting started

Let us create a simple SMS bot using Sulley that greets it's users.

* Create a file called `app.py`.
* Add the following to your `app.py` file.

```python
from sulley import Sulley

bot = Sulley()

bot.reply_to(r'hi')
def say_hello(message):
    message.reply('hello!')

if __name__ == '__main__':
    bot.run()
```

* Grab a copy of `config.json` from [here](./config.json) and place it in the same directory as `app.py`.
* Configure Sulley to use Twilio or Plivo by modifying `key`, `secret` and `phone` in the config.
* Now, run the app using the following command:

```bash
python app.py
```

## More Examples

### Binding functions that reply to simple commands

```python
bot.reply_to(r'hi')
def say_hello(message):
    message.reply('hello!')
```

### Bind multiple commands to a single function

```python
bot.reply_to(r'hi')
bot.reply_to(r'hey')
def say_hello(message):
  message.reply('hello')
```

## More complex command matching rules using regex

```python
bot.reply_to(r'[0-9]abc')
def say_hello(message):
  message.reply('hello')
```

## Configuration details

Sulley can be configured by creating a `config.json` file. By setting the `SULLEY_CONFIG` environment variable, Sulley reads this file on startup. If this environment variable is not set, it looks for the config.json file in the current working directory.

The `SULLEY_CONFIG` environment variable can be set like this:

```
export SULLEY_CONFIG=/path/to/config.json
```

To quickly get started, grab a copy of the config file from [here](./config.json).

### Configuration options

The configuration options for Sulley are detailed below.

#### host

__Default__: `"127.0.0.1"`
__Description__: `host` specifies the binding IP address which Sulley will listen on for requests from [_Twilio_](https://www.twilio.com) or [_Plivo_](https://www.plivo.com) for incoming SMS.

A simple example of how the `host` configuration looks:

```json
{
    "host": "127.0.0.1"
}
```

#### port

__Default__: `5000`
__Description__: `port` specifies the port on which Sulley listens to for requests from [_Twilio_](https://www.twilio.com) or [_Plivo_](https://www.plivo.com) for incoming SMS.

A simple example of how the `port` configuration looks:

```json
{
    "port": 5000
}
```

#### provider

__Default__: No default value
__Description__: `provider` defines the SMS provider to use. Currently, two popular SMS service providers - [Twilio](https://www.twilio.com) & [Plivo](https://www.plivo.com) are supported. The value for this config is a JSON object with the following sub options:

* __name__: Name of the provider in lowercase. Supports `"twilio"` or `"plivo"` currently.
* __key__: For twilio, this is the _Account Sid_ and for plivo this is _Auth ID_ found on their respective dashboards.
* __secret__: For both twilio and plivo, this is the _Auth Token_ found on their respective dashboards.
* __phone__: The phone number (in [E164 format](https://en.wikipedia.org/wiki/E.164). ex: `+10000000000`) where Sulley lives. This number will be used by Sulley's users to talk it. See how to do this on [Twilio here](https://www.twilio.com/help/faq/sms/how-do-i-assign-my-twilio-number-to-my-sms-application) and for [Plivo here](https://www.plivo.com/docs/getting-started/receive-an-sms/#create-an-application).
* __url__: The url where Sulley receives HTTP(s) requests from [_Twilio_](https://www.twilio.com) or [_Plivo_](https://www.plivo.com) for incoming SMS. Refer the [Twilio](https://www.twilio.com/help/faq/sms/how-do-i-assign-my-twilio-number-to-my-sms-application) & [Plivo](https://www.plivo.com/docs/getting-started/receive-an-sms/#create-an-application) docs for more information.

A simple example of how the `provider` configuration looks:

```json
{
    "provider": {
        "name": "twilio",
        "key": "add-key-here",
        "secret": "add-secret-here",
        "phone": "+10000000000",
        "url": "/sulley/"
    }
}
```

The above configuration specifies Sulley to use `twilio` to send and receive SMS. The phone number to which users send SMS to talk to Sulley is `+10000000000`.

## Author

[Sandeep Raju Prabhakar](https://twitter.com/sandeeprajup)  
me[AT]sandeepraju[DOT]in

## License

```
BSD 3-Clause License

Copyright (c) 2016, Sandeep Raju Prabhakar
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

```
