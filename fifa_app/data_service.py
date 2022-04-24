from argparse import ArgumentError
import pymongo
from fifa_app.type_map import projections


categorical_fields = [
    "club_name",
    "league_name",
    "club_position",
    "player_positions",
    "nationality_name",
    "physic",
    "year",
]

fields_to_use_less_than = [
    "age", 
    "wage_eur",
]

stat_group_to_optimize = ["overall", "pace", "shooting", "passing", "attacking", "dribbling", "defending", "goalkeeping"]

class MongoAPI():

    def __init__(self):
        self.connection = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.connection["fifa"]
        self.players_collection = self.db["players"]
        self.user_team_collection = self.db["ultimate_teams"]

    def get_players(self, query_params_dict: dict):
        """
        query_params_dict:

            example: {
                "year": 2015,
                "pace": 90,
                "projection": "attacking"
            }
                Will return players from 2015 (men) with pace above 90 and attacking stats for all matches
        
        """
        match = {}
        fields = list(query_params_dict.keys())
        mutable_dict = dict(query_params_dict)
        if "year" not in fields:
            match["year"] = 2022
        if "gender" not in fields:
            match["gender"] = "M"
        if "projection" in fields:
            projection = projections[str.lower(query_params_dict["projection"])]
            del mutable_dict["projection"]
        else:
            projection = projections["basic"]
        for field in list(mutable_dict.keys()):
            if field in categorical_fields:
                match[field] = query_params_dict[field]
            elif field in fields_to_use_less_than:
                match[field] = {"$lt": int(query_params_dict[field])}
            else:
                match[field] = {"$gt": int(query_params_dict[field])}
        r = self.players_collection.find(filter=match, projection=projection, limit=50)

        result = {
            "num_results": 0,
            "players": [],
        }
        for player in r:
            del player["_id"]
            result["players"].append(player)
        print(result)
        return result

    def get_player(self, player: str, year: int, stats_projection="basic", gender="M") -> dict:
        result = self.players_collection.find(filter={"long_name": player, "year": year, "gender": gender}, projection=projections[stats_projection], limit=1)
        return_player = {}
        for p in result:
            return_player = p
        del return_player["_id"]
        return return_player

        
    def create_team(self, user: str, team_name: str, year: int, players) -> None:
        
        record = {
            "username": user,
            "team_name": team_name,
            "year": year,
        }
        team_stats = {
            "overall": 0,
            "pace": 0,
            "shooting": 0,
            "attacking": 0,
            "passing": 0,
            "dribbling": 0,
            "defending": 0,
            "goalkeeping": 0,
        }

        if len(list(players.keys())) < 11:
            raise Exception("Inputted team cannot have less than 11 players!")
        players_field = []
        for position in list(players.keys()):
            player = players[position]
            player_with_stats = self.get_player(player["name"], year=year)
            
            for stat in list(team_stats.keys()):
                if position.lower() == "gk" and stat == "goalkeeping":
                    team_stats[stat] = player_with_stats["goalkeeping"]
                    team_stats["overall"] += int(player_with_stats["overall"] / 11)
                elif position.lower() != "gk" and stat != "goalkeeping":
                    team_stats[stat] += int(player_with_stats[stat] / 11)
            players_field.append({"name": player_with_stats["long_name"], "position": position})
        record["team_stats"] = team_stats
        record["players"] = players_field
        self.user_team_collection.insert_one(record)

    
    def get_player_recommendation(self, year: int, position: str, wage: int, stat_to_optimize: str) -> dict:
        match = {
            "year": year,
            "player_positions": position,
            "wage_eur": {"$lt": wage},
        }
        projection = projections["overall"]

        if stat_to_optimize not in stat_group_to_optimize:
            raise Exception("Not a valid stat to optimize, please choose from the following:", stat_group_to_optimize)
        
        
        r = self.players_collection.find(filter=match, projection=projection, limit=10, sort=stat_to_optimize)

        result = {
            "num_results": 0,
            "players": [],
        }
        for player in r:
            del player["_id"]
            result["players"].append(player)
        
        return result
        







