import pymongo
from type_map import projections



categorical_fields = [
    "club_name",
    "league_name",
    "club_position",
    "player_positions",
    "nationality_name",
    "physic"
]

fields_to_use_less_than = [
    "age", 
    "wage_eur",
]

class MongoAPI():

    def MongoAPI(self):
        self.connection = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.connection["fifa"]
        self.players_collection = self.db["players"]

    def get_players(self, query_params_dict):
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
        if "year" not in fields:
            match["year"] = 2022
        if "gender" not in fields:
            match["gender"] = "Male"
        for field in fields:
            if field in categorical_fields:
                match[field] = query_params_dict[field]
            elif field in fields_to_use_less_than:
                match[field] = {"$lt": query_params_dict[field]}
            else:
                match[field] = {"$gt": query_params_dict[field]}

        if "projection" in fields:
            projection = projections[str.lower(query_params_dict["projection"])]
        else:
            projection = projections["basic"]
        return self.players_collection.find(filter=match, projection=projection, limit=50)
        


