from fifa_app.data_service import MongoAPI

api = MongoAPI()

print(api.get_team("chris", "chris"))