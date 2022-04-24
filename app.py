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

@app.route("/api/v1/player/", methods=["GET"])
def get_player():
    name = request.args["name"]
    year = request.args["year"]
    player = mongo_api.get_player(player=name, year=year)
    return jsonify(player)

@app.route("/api/v1/players/", methods=["GET"])
def get_players():
    query_params = request.args
    players = mongo_api.get_players(query_params)
    return jsonify(players)


@app.route("/api/v1/team/", methods=["GET"])
def get_team():
    username = request.args["username"]
    team_name = request.args["team_name"]
    response = mongo_api.get_team(user=username, team_name=team_name)
    return jsonify(response)


@app.route("/api/v1/team/", methods=["POST"])
def create_team():
    if request.headers["content-type"] == "application/json":
        data = request.json
        data = jsonify(data).json
        username = data["user"]
        team_name = data["team_name"]
        players = data["players"]
        year = data["year"]
    resp = mongo_api.create_team(user=username, team_name=team_name, players=players, year=year)
    return jsonify(resp)


@app.route("/api/v1/team/edit/", methods=["PUT"])
def edit_team():
    if request.headers["content-type"] == "application/json":
        data = request.json
        data = jsonify(data).json
        username = data["user"]
        team_name = data["team_name"]
        year = data["year"]
        p1_name = data["original_player_name"]
        p2_name = data["replacing_player_name"]
    resp = mongo_api.edit_team(user=username, team_name=team_name, year=year, original_player_name=p1_name, replacing_player_name=p2_name)
    return jsonify(resp)


@app.route("/api/v1/team/replace/", methods=["GET"])
def get_player_recommendation():
    print(request.args)
    year = request.args["year"]
    position = request.args["position"]
    wage = request.args["wage"]
    stat = request.args["stat"]
    response = mongo_api.get_player_recommendation(year=year, position=position, wage=int(wage), stat_to_optimize=stat)
    return jsonify(response)

if __name__ == '__main__':
    app.run()