import pymongo
import os
import pandas as pd
import json

def main():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    databases = client.list_database_names()

    if "fifa" not in databases:
        db = client["fifa"]

        players_collection = db["players"]

        for file in os.listdir("data/players"):
            data = pd.read_csv("data/players/" + file)
            data["year"] = "20" + file.split(".")[0][-2:]
            data_json = json.loads(data.to_json(orient='records'))
            players_collection.insert_many(data_json)
            print("Successfully loaded data for", file)
    else:
        print("Data has been previously loaded.")

if __name__ == "__main__":
    main()