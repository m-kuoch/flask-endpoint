"""App with candles endpoint."""
import argparse
from datetime import timedelta
from flask import Flask
from flask import request
import json


from utils import (
    check_if_valid_iso,
    get_valid_currency_pairs,
    get_one_minute_candles_from_coinbase
)

INVALID_TIME_MSG = 'Please use ISO 8601 and specify up to the minute.'

def create_app():
    """Create the app."""
    app = Flask(__name__)
    valid_pairs = []
    load_pairs_success = False

    # Load the currency pairs from Coinbase API
    try:
        valid_pairs = get_valid_currency_pairs()
        load_pairs_success = True
    except:
        print("Error loading currency pairs")

    @app.route('/candles')
    def get_candles():
        """
        Get mintue candles between start time and end time for currency pair.
        This route takes parameters
            - currency_pair: the currency pair
            - start_time: the start time (will be rounded up to nearest minute)
            - end_time: the end time (inclusive)
        """
        # First clean inputs
        if '/' in request.args['currency_pair']:
            return "Invalid currency pair, forbidden character '/'.", 400
        # Check if currency pair is valid
        if load_pairs_success and request.args['currency_pair'] not in valid_pairs:
            return "Invalid currency pair.", 400

        # Check for valid start_time and end_time
        start_time = check_if_valid_iso(request.args['start_time'])
        end_time = check_if_valid_iso(request.args['end_time'])
        if start_time is None:
            return "Invalid start time. " + INVALID_TIME_MSG, 400
        if end_time is None:
            return "Invalid end time. "+ INVALID_TIME_MSG, 400
        if start_time > end_time:
            return "Start time is after end time.", 400

        # Check that time interval is less than 24 hours
        if end_time - start_time > timedelta(days=1):
            return "Time interval is too long (greater than 24 hours).", 400

        # Split time window into 5 hours intervals and get candles for each
        all_candles = []
        interval_start = start_time
        while interval_start < end_time:
            interval_end = min(interval_start + timedelta(hours=5), end_time)
            # Get candles for the interval
            response = get_one_minute_candles_from_coinbase(
                request.args['currency_pair'],
                interval_start,
                interval_end
            )
            interval_start = interval_end
            # Prepend next candles lists, avoiding duiplicates
            if (len(all_candles) > 0) and (response[-1][0] == all_candles[0][0]):
                response = response[:-1]
            all_candles = response + all_candles
        return json.dumps(all_candles), 200

    return app


def range_type(i, start, end):
    """Check if input is in range (inclusive)."""
    value = int(i)
    if start <= value <= end:
        return value
    else:
        raise argparse.ArgumentTypeError(f'value not in range [{start}-{end}]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the app.')
    parser.add_argument(
        '--port',
        type=lambda x: range_type(x, 1, 65535),
        default=5001,
        metavar='[1-65535]',
    )
    app = create_app()
    app.run(host='0.0.0.0', port=parser.parse_args().port)
