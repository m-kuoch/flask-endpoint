from flask import Flask

app = Flask(__name__)


@app.route('/')
def testing():
    """Testing the Flask app."""
    return 'Hello :)'


@app.route('/testing2')
def testing2():
    """Testing another route."""
    return 'Hello again!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
