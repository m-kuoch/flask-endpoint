def test_valid_pair(client):
    response = client.get(
        "/candles?currency_pair=ETH-USD"
        "&start_time=2019-11-02T00:00:00"
        "&end_time=2019-11-02T00:05:00"
    )
    assert 200 == response.status_code

def test_forbidden_character(client):
    response = client.get(
        "/candles?currency_pair=ETH/USD"
        "&start_time=2019-11-02T00:00:00"
        "&end_time=2019-11-02T00:05:00"
    )
    assert b"Invalid currency pair, forbidden character '/'." == response.data


def test_invalid_pair(client):
    response = client.get(
        "/candles?currency_pair=qwe-rty"
        "&start_time=2019-11-02T00:00:00"
        "&end_time=2019-11-02T00:05:00"
    )
    assert b"Invalid currency pair." == response.data