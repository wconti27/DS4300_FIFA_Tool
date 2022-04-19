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
            if "female" in file:
                data["gender"] = "F"
            else:
                data["gender"] = "M"
            data_json = json.loads(data.to_json(orient='records'))
            
            for player in data_json:
                columns_to_format = ["ls", "st", "rs", "lw", "lf",	"cf", "rf", "rw", "lam", "cam",	"ram", "lm", "lcm",	"cm", "rcm", "rm", "lwb", "ldm", "cdm", "rdm", "rwb", "lb", "lcb", "cb", "rcb", "rb", "gk"]
                for column in columns_to_format:
                    if isinstance(player[column], str):
                        if "+" in player[column]:
                            split = player[column].split("+")
                            player[column] = int(split[0]) + int(split[1])
                        elif "-" in player[column]:
                            split = player[column].split("-")
                            player[column] = int(split[0]) - int(split[1])
                list_columns = ["player_positions", "player_tags", "player_traits"]
                for column in list_columns:
                    if player[column] is not None:
                        player[column] = [x.strip() for x in player[column].split(',')]
            players_collection.insert_many(data_json)
            print("Successfully loaded data for", file)

        # TODO: Add indexes to data collection for quicker queries

    else:
        print("Data has been previously loaded.")

if __name__ == "__main__":
    main()