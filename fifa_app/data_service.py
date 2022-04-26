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
    "short_name"
]

fields_to_use_less_than = [
    "age", 
    "wage_eur",
]

stat_group_to_optimize = ["overall", "pace", "shooting", "passing", "attacking", "dribbling", "defending"]

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
                "year": "2015",
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
            result["num_results"] += 1
            result["players"].append(player)
        return result

    def get_player(self, player: str, year: str, stats_projection="basic", gender="M") -> dict:
        result = self.players_collection.find(filter={"short_name": player, "year": year, "gender": gender}, projection=projections[stats_projection], limit=1)
        returned_player = None
        for p in result:
            returned_player=p
            del p["_id"]
        return returned_player


    def get_team(self, user: str, team_name: str):
        team = self.user_team_collection.find(filter={"username": user, "team_name": team_name})
        returned_team = None
        for t in team:
            returned_team=t
            del t["_id"]
        return returned_team

        
    def create_team(self, user: str, team_name: str, year: str, players) -> str:
        """
        request_object = {
            "user": "wconti",
            "team_name": "wills_team",
            "year": "2016","players": [
                {"CF": "L. Messi"},
                {"ST": "L. Suárez"},
                {"LW": "Neymar"},
                {"CDM": "Sergio Busquets"},
                {"CB": "Piqué"},
                {"RB": "Dani Alves"},
                {"CM": "I. Rakitić"},
                {"LB": "Jordi Alba"},
                {"CB": "J. Mathieu"},
                {"GK": "M. ter Stegen"},
                {"LM": "A. Turan"}
            ],
        }
        """
        
        record = {
            "username": user,
            "team_name": team_name,
            "year": year,
            "team_stats": {},
            "players": [],
        }
        team_stats = {
            "overall": 0,
            "pace": 0,
            "shooting": 0,
            "passing": 0,
            "dribbling": 0,
            "defending": 0,
        }

        if len(players) != 11:
            return f"Could not create team, needs to have exactly 11 players, counted {len(players)} players."

        if self.get_team(user=user, team_name=team_name) is not None:
            return f"Team already exists, please edit team or use new team name!"
        
        players_field = []
        for p in players:
            position = list(p.keys())[0]
            player = p[position]
            player_with_stats = self.get_player(player, year=year)
            if position.lower() == "gk":
                team_stats["overall"] += int(player_with_stats["overall"] / 11)
                continue
            else:
                for stat in list(team_stats.keys()):
                    team_stats[stat] += int(player_with_stats[stat] / 11)
            player_with_stats["ultimate_team_position"] = position
            players_field.append(player_with_stats)
        record["team_stats"] = team_stats
        record["players"] = players_field
        self.user_team_collection.insert_one(record)
        return "Team created successfully!"
    
    def get_player_recommendation(self, year: str, position: str, wage: int, stat_to_optimize: str) -> dict:
        match = {
            "year": year,
            "player_positions": position,
            "wage_eur": {"$lt": wage},
        }
        projection = projections["basic"]

        if stat_to_optimize not in stat_group_to_optimize:
            raise Exception("Not a valid stat to optimize, please choose from the following:", stat_group_to_optimize)
        
        
        r = self.players_collection.find(filter=match, projection=projection, limit=10, sort=[(stat_to_optimize, pymongo.DESCENDING)])

        result = {
            "num_results": 0,
            "players": [],
        }
        for player in r:
            del player["_id"]
            result["num_results"] += 1 
            result["players"].append(player)
        
        return result

    def edit_team(self, user: str, team_name: str, year: str, original_player_name: str, replacing_player_name: str):
        original_player_stats = self.get_player(original_player_name, year=year)
        new_player_stats = self.get_player(replacing_player_name, year=year)

        if self.get_team(user=user, team_name=team_name) is None:
            raise Exception(f"Team: {team_name} not found for user {user}")
        
        match = {
            "username": user,
            "team_name": team_name,
            "year": year,
            "players.short_name": original_player_name,
        }
        team = self.user_team_collection.find_one(filter=match)
        if team is not None:
            team_stats = team["team_stats"]
            new_players = []
            for player in team["players"]:
                if player["short_name"] == original_player_name:
                    if player["ultimate_team_position"] == "gk":
                        team_stats["overall"] -= int(original_player_stats["overall"] / 11)
                        team_stats["overall"] += int(new_player_stats["overall"] / 11)
                    else:
                        for stat in team_stats:
                            team_stats[stat] -= int(original_player_stats[stat] / 11)
                            team_stats[stat] += int(new_player_stats[stat] / 11)
                            new_player_stats["ultimate_team_position"] = player["ultimate_team_position"]
                    new_players.append(new_player_stats)
                else:
                    new_players.append(player)
            update = { 
                "$set": {
                    "players": new_players,
                    "team_stats": team_stats,
                }
            }
            print(update)
            self.user_team_collection.update_one(filter=match, update=update, upsert=True)
            return f"Successfully switched player {original_player_name} with player {replacing_player_name}."
        else:
            raise Exception(f"Player: {original_player_name} not found on team!")







