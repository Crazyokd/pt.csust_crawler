import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT = os.getenv('account')
PASSWORD = os.getenv('password')

try:
    assert ACCOUNT
    assert PASSWORD
except AssertionError:
    print('Please confirm whether the account and password are set in the .env file respectively')
else:
    print('Personal information loaded successfully')