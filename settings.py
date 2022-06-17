import os
from dotenv import load_dotenv

load_dotenv()

DISPLAY_NAME = os.getenv('display_name')
SENDER_EMAIL = os.getenv('sender_email')
EMAIL_PASSWORD = os.getenv('email_password')
ACCOUNT = os.getenv('account')
PASSWORD = os.getenv('password')
RUN_FREQUENCY_LEVEL = os.getenv('run_frequency_level')
NUMBER_OF_INVALID_RUN = os.getenv('number_of_invalid_run')

try:
    assert DISPLAY_NAME
    assert SENDER_EMAIL
    assert EMAIL_PASSWORD
    assert ACCOUNT
    assert PASSWORD
    assert RUN_FREQUENCY_LEVEL
    assert NUMBER_OF_INVALID_RUN
except AssertionError:
    print('Please set up credentials. Read https://github.com/crazyokd/pt.csust_crawler#pt.csust_crawler')
else:
    print('Credentials loaded successfully')
