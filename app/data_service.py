import pymongo

# TODO: Add get functionality for getting data ie: get player, get players

class MongoAPI():

    def MongoAPI(self):
        self.connection = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.connection["fifa"]
        self.players_collection = self.db["players"]

    def get_players(self, query_params_dict):

        """
         TODO: Implement necessary DB code. 
        """
        pass
