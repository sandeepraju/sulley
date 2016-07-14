from setuptools import setup

setup(
    name='sulley',
    packages=['sulley'],
    version='0.0.1a0',
    description=('With Sulley, you can build SMS bots in just'
                 ' a few lines of code. Powered by Twilio & Plivo,'
                 ' Sulley requires very minimal configuration and '
                 'code to bring your bot to life!'),
    long_description=('For more information, visit:'
                      ' https://sandeepraju.github.io/sulley/'),
    author='Sandeep Raju Prabhakar',
    author_email='me@sandeepraju.in',
    url='https://github.com/sandeepraju/sulley',
    download_url='https://github.com/sandeepraju/sulley/archive/master.zip',
    install_requires=[
        'plivo==0.11.1',
        'twilio==5.4.0',
        'Flask==0.11.1'
    ],
    keywords=[
        'sms', 'message', 'twilio', 'plivo',
        'bot', 'text', 'communication'
    ],
    classifiers=[
        'Programming Language :: Python',
    ],
)
