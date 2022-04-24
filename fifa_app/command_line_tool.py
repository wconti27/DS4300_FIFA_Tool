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