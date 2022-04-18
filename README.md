# flask-endpoint

Start the server locally on port 5001 with ```python app.py```.  Alternatively, the port can be specified with ```--port``` argument.

Use the URL ```http://127.0.0.1:5001/candles?currency_pair=<currency-pair>&start_time=<start-time>&end_time=<end-time>``` to make requests to  the ```/candles``` endpoint, where ```<currency-pair>``` is a currency pair, and ```<start-time>``` and ```<end-time>``` are given in ISO 8601 format.
