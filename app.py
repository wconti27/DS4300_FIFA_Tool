from flask import Flask, request
from fifa_app.data_service import MongoAPI
from flask import jsonify

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
    return jsonify(players)


@app.route("/api/v1/team/", methods=["CREATE"])
def create_team():
    username = request.args["username"]
    team_name = request.args["team_name"]
    players = request.args["players"]
    year = request.args["year"]
    response = mongo_api.create_team(user=username, team_name=team_name, players=players, year=int(year))
    return jsonify(response)


@app.route("/api/v1/team/replace", methods=["GET"])
def get_player_recommendation():
    year = request.args["year"]
    position = request.args["position"]
    wage = request.args["wage"]
    stat = request.args["stat"]
    response = mongo_api.get_player_recommendation(year=int(year), position=position, wage=int(wage), stat_to_optimize=stat)
    return jsonify(response)

if __name__ == '__main__':
    app.run()