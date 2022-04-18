"""Utility functions for the project"""
from datetime import datetime
import requests


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