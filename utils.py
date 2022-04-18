"""Utility functions for the project"""
from datetime import datetime
import json
import requests
from typing import List, Union


def check_if_valid_iso(date_string):
    """
    Return datetime object if date_string is a valid ISO date string specifying at least
    up-to-the-minute, None otherwise.
    """
    for fmt in ['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f']:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            pass
    return None


def get_valid_currency_pairs():
    """
    Get a list of valid currency pairs from the Coinbase API.
    """
    currency_resp = requests.get('https://api.exchange.coinbase.com/products')
    if currency_resp.status_code == 200:
        valid_pairs = set()
        for product in currency_resp.json():
            valid_pairs.add(product['id'])
        return valid_pairs
    else:
        raise Exception('Error retrieving currency pairs from Coinbase API')

def get_one_minute_candles_from_coinbase(
    currency_pair: str,
    start_utc_datetime: str,
    end_utc_datetime: str
) -> List[List[Union[str, float]]]:
    """Return one minute candles for the currency pair from Coinbase.
    start/end_utc_datetime should be ISO 8601 formatted datetime strings,
    for example 2014-11-06T10:34:47.123456.
    This endpoint is document at
    https://docs.cloud.coinbase.com/exchange/reference/exchangerestapi_getproductcandles .
    Notes
        - start timestamps are rounded up to the next minute. 12:00:50 will
          have the candle from 12:01 to 12:02 as the first candle
        - end timestamps are inclusive. If the end is 12:00:00, the candle for
          12:00 to 12:01 will be included. To avoid this, use 11:59:59
          as the end timestamp.
    """
    candles_resp = requests.get(
        f'https://api.exchange.coinbase.com/products/{currency_pair}/candles',
        params={
            'start': start_utc_datetime,
            'end': end_utc_datetime
        }
    )
    return json.loads(candles_resp.content)