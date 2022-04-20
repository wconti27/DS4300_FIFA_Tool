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

class MongoAPI():

    def __init__(self):
        self.connection = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.connection["fifa"]
        self.players_collection = self.db["players"]

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

        


