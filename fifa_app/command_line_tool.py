"""
Will need a few basic information for each search:
    FIFA year (2015-2022)
    What attributes to filter on
    What attribute to sort on

basic query example format:

{
    "year": 2015,
    "defense": 50 (would mean to search for defense above 50)
    "shooting": 60 Same as above
    "price": 2,000,000 # get players with cost below $2MM
    "projection": "Basic" # only return the basic fields
}

Also add a --help argument that can output all the possible fields to filter on such as below:
    Could also take arguments such as what stats / group of stats to return for the players. Groupings found below, ie return all basic stats for players filtered

Basic
--------
short_name
overall
potential
wage_eur
value_eur
club_name
league_name
club_position
player_positions
nationality_name
pace
shooting
passing
dribbling
defending

Attacking
---------
shooting
passing
attacking_crossing
attacking_finishing
attacking_heading_accuracy
attacking_short_passing
attacking_volleys

Defense
-------
defending_marking_awareness
defending_standing_tackle
defending_sliding_tackle

Goalkeeping
-----------
goalkeeping_diving
goalkeeping_handling
goalkeeping_kicking
goalkeeping_positioning
goalkeeping_reflexes
goalkeeping_speed

Physical
--------
physic
height_cm
weight_kg
age
power_shot_power
power_jumping
power_stamina
power_strength
power_long_shots

Mentality
----------
mentality_aggression
mentality_interceptions
mentality_positioning
mentality_vision
mentality_penalties
mentality_composure

Positions
---------
ls
st
rs
lw
lf
cf
rf
rw
lam
cam
ram
lm
lcm
cm
rcm
rm
lwb
ldm
cdm
rdm
rwb
lb
lcb
cb
rcb
rb
gk
"""
import requests

def call_get_player():
    body = {'year': '2016', 'name': 'L. Messi'}
    r = requests.get("http://127.0.0.1:5000/api/v1/player/", params=body)

def call_get_players():
    body = {"year":"2016","pace":90,"club_name":"FC Barcelona","projection":"attacking"}
    r = requests.get("http://127.0.0.1:5000/api/v1/players/", params=body)

def call_get_team():
    data = {"username":"wconti","team_name":"wills_team","year":"2016"}
    team = requests.get("http://127.0.0.1:5000/api/v1/team/", params=data)

def call_create_team():
    headers = {'content-type': 'application/json'}
    body = {
        "user": "wconti", 
        "team_name": "wills_team", 
        "year": "2016", 
        "players": [
            {"CF": "L. Messi"}, 
            {"ST": "L. Su\\u00e1rez"}, 
            {"LW": "Neymar"}, 
            {"CDM": "Sergio Busquets"}, 
            {"CB": "Piqu\\u00e9"}, 
            {"RB": "Dani Alves"}, 
            {"CM": "I. Rakiti\\u0107"}, 
            {"LB": "Jordi Alba"}, 
            {"CB": "J. Mathieu"}, 
            {"GK": "M. ter Stegen"}, 
            {"LM": "A. Turan"}
        ]
    }

    r = requests.post("http://127.0.0.1:5000/api/v1/team/", data=body, headers=headers)

def call_edit_team(): # Switches player
    headers = {'content-type': 'application/json'}
    request = {
        "user": "wconti", 
        "team_name": "wills_team", 
        "year": "2016", 
        "original_player_name": "J. Mathieu", 
        "replacing_player_name": "Thiago Silva"
    }

    r = requests.put("http://127.0.0.1:5000/api/v1/team/edit/", data=request, headers=headers)

def call_get_player_recommendations():
    recs = {"year":"2016","wage":10000000,"position":"CB","stat_to_optimize":"overall"}

    r = requests.get("http://127.0.0.1:5000/api/v1/team/replace/", params=recs)



    