"""App with candles endpoint."""
from datetime import timedelta
from flask import Flask
from flask import request
import json

from coinbase_api import get_one_minute_candles_from_coinbase
from utils import check_if_valid_iso, get_valid_currency_pairs

INVALID_TIME_MSG = 'Invalid time format. ' \
                   'Please use ISO 8601 and specify up to the minute.'

app = Flask(__name__)
valid_pairs = []
load_pairs_success = False


@app.route('/')
def testing():
    """Testing the Flask app."""
    return 'Hello :)'


@app.route('/testing2')
def testing2():
    """Testing another route."""
    print(request.args)
    return 'Hello again!'


if __name__ == '__main__':
    try:
        valid_pairs = get_valid_currency_pairs()
        load_pairs_success = True
    except:
        print("Error loading currency pairs")

    app.run(host='0.0.0.0', port=5001)
