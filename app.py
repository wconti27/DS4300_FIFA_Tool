from flask import Flask, request
from app.data_service import MongoAPI

app = Flask(__name__)

mongo_api = MongoAPI()


@app.route("/")
def hello():
    return "hello world"

# TODO: Create additional routing for other pages on app

# TODO: Create api routing for get requests, make calls to DB for associated data

@app.route("/api/v1/players/", methods=["GET"])
def get_players():
    query_params = request.args
    players = mongo_api.get_players(query_params)
    return players



if __name__ == '__main__':
    app.run()