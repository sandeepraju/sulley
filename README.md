Sulley (Work in Progress)
=========================

![Sulley from Monsters, Inc.](http://i.imgur.com/KvSWLHo.png)

With Sulley, you can build SMS bots in just a few lines of code. Powered by Twilio & Plivo, Sulley requires very minimal configuration and code to bring your SMS bot to life!

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
* Grab a copy of `config.json` from here and place in the same directory as `app.py`.
* Configure Sulley to use Twilio or Plivo by setting `key`, `secret` and `phone` in the config.
* Add the following to your `app.py` file.

```python
from sulley import Sulley

bot = Sulley()

bot.reply_to(r'hi'):
def say_hi(message):
    message.reply('hello!')

if __name__ == '__main__':
    bot.run()
```
* Now, run the app using the following command:

```bash
python app.py
```

### Advanced command configuration

### Default reply handler

### Restricting users

### Delayed responses


## Configuration

Sulley can be configured by creating a `config.json` file. By setting the `SULLEY_CONFIG` environment variable, Sulley readds this file on startup. If this environment variable is not set, it looks for the config.json file in the current working directory.

The `SULLEY_CONFIG` environment variable can be set as follows:

```
export SULLEY_CONFIG=/path/to/config.json
```
To quickly get started, grab a copy of the config file from [here]().

### Configuration options

The configuration options for Sulley has been discussed in detail in the following set of sections.

#### host

__Default__: `"127.0.0.1"`
__Description__: `host` specifies the binding IP address which Sulley will listen on for requests from [_Twilio_](https://www.twilio.com) & [_Plivo_](https://www.plivo.com) for incoming SMSes.

A simple example of how the `host` configuration looks:

```json
{
    "host": "127.0.0.1"
}
```

#### port

__Default__: `5000`
__Description__: `port` specifies the port on which Sulley listens for requests from [_Twilio_](https://www.twilio.com) & [_Plivo_](https://www.plivo.com) for incoming SMSes.

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
* __key__: For twilio, this is the _<whatever>_ and for plivo this is _Auth ID_. Refer Configuration guides for [Twilio]() and [Plivo]() below for more details on how to configure this option.
* __secret__: For twilio, this is the _<whatever>_ and for plivo this is _Auth Token_. Refer Configuration guides for [Twilio]() and [Plivo]() below for more details on how to configure this option.
* __phone__: The phone number (in [E164 format](https://en.wikipedia.org/wiki/E.164). ex: `+10000000000`) where Sulley lives. This number will be used by Sulley's users to talk it. Refer Configuration guides for [Twilio]() and [Plivo]() below for more details on how to configure this option.
* __url__: The url where Sulley receives HTTP from [_Twilio_](https://www.twilio.com) & [_Plivo_](https://www.plivo.com) for incoming SMSes. Refer Configuration guides for [Twilio]() and [Plivo]() below for more details on how to configure this option.

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

The above configuration specifies Sulley to use Twilio to send and receive SMSes.

#### users

__Default__: `[]`
__Description__: `users` is used to make Sulley accessible to only the users configured here. By default, any user can talk to Sulley. Each item in this list is a JSON object with the following sub options:

* __name__: Name of the user. Example: `"John Doe"`.
* __phone__: Phone number (in [E164 format](https://en.wikipedia.org/wiki/E.164). ex: `+10000000000`) from which the user will talk to Sulley.
* __role__: Defines whether the user is an admin or normal user. Allowed values are `"admin"` or `"user"` (default). Admin users can access specific commands marked for admins. More on this can be found in the [reply decorator documentation]().

A simple example of how the `users` configuration looks:

```json
{
    "users": [
        {
            "name": "John Doe",
            "phone": "+10000000000",
            "role": "admin"
        },
        {
            "name": "James P. Sullivan",
            "phone": "+10000000001",
            "role": "user"
        },
    ]
}
```

The above configuration specifies Sulley to only respond to only John Doe and James P. Sullivan.

### Configuration with Twilio

#### Getting <whatever> for 'key'

#### Getting <whatever> for 'secret'

#### Getting Phone number for 'phone'

#### Configuring <> for 'url'

### Configuration with Plivo

#### Getting Auth ID for 'key'

#### Getting Auth Token for 'secret'

#### Getting Phone number for 'phone'

#### Configuring Message URL for 'url'

## Examples

## FAQ

## Author

[Sandeep Raju Prabhakar](https://twitter.com/sandeeprajup) <me AT sandeepraju DOT in>

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
