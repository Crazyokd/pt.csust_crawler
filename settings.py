import os
from dotenv import load_dotenv

load_dotenv()

DISPLAY_NAME = os.getenv('display_name')
SENDER_EMAIL = os.getenv('sender_email')
EMAIL_PASSWORD = os.getenv('email_password')
ACCOUNT = os.getenv('account')
PASSWORD = os.getenv('password')

try:
    assert DISPLAY_NAME
    assert SENDER_EMAIL
    assert EMAIL_PASSWORD
    assert ACCOUNT
    assert PASSWORD
except AssertionError:
    print('Please set up credentials. Read https://github.com/crazyokd/pt.csust_crawler#pt.csust_crawler')
else:
    print('Credentials loaded successfully')
