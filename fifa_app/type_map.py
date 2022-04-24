basic_projection = {
    "short_name": 1,
    "overall": 1,
    "potential": 1,
    "wage_eur": 1,
    "club_name": 1,
    "league_name": 1,
    "club_position": 1,
    "player_positions": 1,
    "nationality_name": 1,
    "pace": 1,
    "shooting": 1,
    "passing": 1,
    "dribbling": 1,
    "defending": 1,
}

attacking_projection = {
    "short_name": 1,
    "overall": 1,
    "shooting": 1,
    "passing": 1,
    "attacking_crossing": 1,
    "attacking_finishing": 1,
    "attacking_heading_accuracy": 1,
    "attacking_short_passing": 1,
    "attacking_volleys": 1,
}

defending_projection = {
    "short_name": 1,
    "overall": 1,
    "defending": 1,
    "defending_marking_awareness": 1,
    "defending_standing_tackle": 1,
    "defending_sliding_tackle": 1,
    "attacking_finishing": 1,
}

goalkeeping_projection = {
    "short_name": 1,
    "overall": 1,
    "goalkeeping_diving": 1,
    "goalkeeping_handling": 1,
    "goalkeeping_kicking": 1,
    "goalkeeping_positioning": 1,
    "goalkeeping_reflexes": 1,
    "goalkeeping_speed": 1,
}

physical_projection = {
    "short_name": 1,
    "overall": 1,
    "physic": 1,
    "height_cm": 1,
    "weight_kg": 1,
    "age": 1,
    "power_shot_power": 1,
    "power_jumping": 1,
    "power_stamina": 1,
    "power_strength": 1,
    "power_long_shots": 1,
}

mentality_projection = {
    "short_name": 1,
    "overall": 1,
    "mentality_aggression": 1,
    "mentality_interceptions": 1,
    "mentality_positioning": 1,
    "mentality_vision": 1,
    "mentality_penalties": 1,
    "mentality_composure": 1,
}

position_projection = {
    "short_name": 1,
    "overall": 1,
    "player_positions": 1,
    "ls": 1,
    "st": 1,
    "rs": 1,
    "lw": 1,
    "lf": 1,
    "cf": 1,
    "rf": 1,
    "rw": 1,
    "lam": 1,
    "cam": 1,
    "ram": 1,
    "lm": 1,
    "lcm": 1,
    "cm": 1,
    "rcm": 1,
    "rm": 1,
    "lwb": 1,
    "ldm": 1,
    "cdm": 1,
    "rdm": 1,
    "rwb": 1,
    "lb": 1,
    "lcb": 1,
    "cb": 1,
    "rcb": 1,
    "rb": 1,
    "gk": 1,
}

projections = {
    "basic": basic_projection,
    "attacking": attacking_projection,
    "defending": defending_projection,
    "goalkeeping": goalkeeping_projection,
    "physical": physical_projection,
    "mentality": mentality_projection,
    "position": position_projection
}