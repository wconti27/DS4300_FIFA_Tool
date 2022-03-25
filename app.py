from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "hello world"

# TODO: Create additional routing for other pages on app

# TODO: Create api routing for get requests, make calls to DB for associated data

if __name__ == '__main__':
    app.run()