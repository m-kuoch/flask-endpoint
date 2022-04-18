from app import INVALID_TIME_MSG


def test_start_vs_end(client):
    response = client.get(
        "/candles?currency_pair=ETH-USD"
        "&start_time=2019-11-02T00:00:00"
        "&end_time=2019-11-01T00:00:00"
    )
    assert b"Start time is after end time." == response.data


def test_bad_start(client):
    response = client.get(
        "/candles?currency_pair=ETH-USD"
        "&start_time=2019-11-02T"
        "&end_time=2019-11-03T00:00:00"
    )
    assert bytes("Invalid start time. " + INVALID_TIME_MSG, 'utf-8') == response.data


def test_bad_end(client):
    response = client.get(
        "/candles?currency_pair=ETH-USD"
        "&start_time=2019-11-02T00:00:00"
        "&end_time=2019-11-03T"
    )
    assert bytes("Invalid end time. " + INVALID_TIME_MSG, 'utf-8') == response.data


def test_long_interval(client):
    response = client.get(
        "/candles?currency_pair=ETH-USD"
        "&start_time=2019-11-02T00:00:00"
        "&end_time=2019-11-03T00:01:00"
    )
    assert b"Time interval is too long (greater than 24 hours)." == response.data