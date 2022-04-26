import pandas as pd
import requests
import json

def main():
    type_q = choose_query()
    if type_q == 'Basic Search':
        ret = basic_search()
        print(ret)
    elif type_q == 'Advanced Search':
        ret = advanced_search()
        print(ret)
    else:
        ret = ultimate_team_handler()


def ultimate_team_handler():
    queries = {1: 'Input Team', 2: 'Replace player', 3: 'Replacement recommender'}
    prompting = True
    q = prompt_builder(queries)
    user_input = None
    while prompting:
        user_input = int(input(q))
        if user_input in queries.keys():
            prompting = False
        else:
            print('INPUT NOT RECOGNIZED')

    if user_input == 1:
        input_team()
    #elif user_input == 2:
        #replace_playeer()


def input_team():
    players = []
    year = choose_year()
    username = input("Enter a username")
    teamname = input("Enter a team name")
    while len(players) < 11:
        player = input("Input a player that you would like to add to your team: First Last\n")
        names = get_names(player)
        rets = {'num_results': 0}
        c = 0
        while rets['num_results'] == 0 and c < len(names):
            body = {'year': year, 'short_name': names[c]}
            rets = requests.get("http://127.0.0.1:5000/api/v1/player/", params=body).json()
            print(names[c])
            c += 1
        if rets['num_results'] == 0:
            print('Player not found')
        else:
            rets = rets["players"][0]
            print(rets)
            players.append({rets['player_positions'][0]: rets['short_name']})
    headers = {'content-type': 'application/json'}
    body = {
        "user": username,
        "team_name": teamname,
        "year": year,
        "players": players,
    }
    return requests.post("http://127.0.0.1:5000/api/v1/team/", data=json.dumps(body), headers=headers).json()

def choose_query():
    print("Fifa Search engine V1\n")
    queries = {1: 'Basic Search', 2: 'Advanced Search', 3: 'Ultimate Team Recommender'}
    prompting = True
    q = prompt_builder(queries)
    while prompting:
        user_input = int(input(q))
        if user_input in queries.keys():
            prompting = False
        else:
            print('INPUT NOT RECOGNIZED')
    return queries[user_input]


def prompt_builder(queries):
    prompt = 'Type: \n'
    for num in queries.keys():
        prompt = prompt + '%s for %s\n' % (num, queries[num])
    return prompt



def basic_search():
    year = choose_year()
    constraints = choose_constraints()
    constraints['year'] = year
    players = requests.get("http://127.0.0.1:5000/api/v1/players/", params=constraints).json()["players"]
    df = pd.DataFrame(players)
    return df

def get_names(name):
    names = name.split(" ")
    return [name, names[0][0]+". "+names[1], names[0], names[1]]

def advanced_search():
    year = choose_year()
    player = input("input a player name: First Last\n")
    names = get_names(player)
    rets = {'num_results': 0}
    c=0
    while rets['num_results'] == 0 and c < len(names):
        body = {'year':year, 'short_name': names[c]}
        rets = requests.get("http://127.0.0.1:5000/api/v1/players/", params=body).json()
        print(names[c])
        c+=1
    if len(rets) == 0:
        print('Player not found')
    else:
        constraints = choose_constraints(counter=1)
        rets = pd.DataFrame(rets['players'])
        rets = (rets[['club_position', 'overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending']].iloc[0]).to_dict()
        for key in constraints.keys():
            rets[key] = constraints[key]

        rets['year'] = year
        players = requests.get("http://127.0.0.1:5000/api/v1/players/", params=rets).json()["players"]
        df = pd.DataFrame(players)
        return df


def choose_constraints(counter=0):
    print("For a list of fields to search on, type --help")
    stop = False
    constraints = {}
    while not stop:
        if len(constraints) != 0:
            counter +=1
        if counter == 0:
            temp = input('Enter field and value separated by a comma. Value must be 1-99 for attributes.\n')
        else:
            temp = input('Type \'search\' to search on inputted constraints or add another constraint: Enter field and value separated by a comma. Value must be 1-99 for attributes\n')
        if temp.lower() == 'search':
            stop = True
            break

        if temp == '--help':
            for x in HELP:
                print(x)
        elif ',' in temp:
            field, value = temp.split(',')
            field, value = field.strip(), value.strip()

            if field in NUMERICS:
                if value.isnumeric():
                    value = int(value)
                    constraints[field] = value
                else:
                    print("constraint for this field must be numeric")

            elif field not in HELP:
                print('Field not recognized')
            else:
                constraints[field] = value
        else:
            print("constraints need to be comma separated")
    return constraints

def choose_year():
    years = list(range(2015, 2023))
    year = 0
    while int(year) not in years:
        year = input("Input a year to search 2015-2022\n")
    return year


HELP = ['Basic Statistics',
        '--------',
        'short_name',
        'overall',
        'potential',
        'wage_eur',
        'value_eur',
        'club_name',
        'league_name',
        'club_position',
        'player_positions (ls, st, rs, lw, lf, cf, rf, rw, lam, cam, ram, lm, lcm, cm, rcm, rm, lwb, ldm, cdm, rdm, rwb, lb, lcb, cb, rcb, rb)',
        'nationality_name',
        'pace',
        'shooting',
        'passing',
        'dribbling',
        'defending',
        'Attacking Statistics',
        '---------',
        'shooting',
        'passing',
        'attacking_crossing',
        'attacking_finishing',
        'attacking_heading_accuracy',
        'attacking_short_passing',
        'attacking_volleys',
        'Defense Statistics',
        '-------',
        'defending_marking_awareness',
        'defending_standing_tackle',
        'defending_sliding_tackle',
        'Goalkeeping',
        '-----------',
        'goalkeeping_diving',
        'goalkeeping_handling',
        'goalkeeping_kicking',
        'goalkeeping_positioning',
        'goalkeeping_reflexes',
        'goalkeeping_speed',
        'Physical Statistics',
        '--------',
        'physic',
        'height_cm',
        'weight_kg',
        'age',
        'power_shot_power',
        'power_jumping',
        'power_stamina',
        'power_strength',
        'power_long_shots',
        'Mentality Statistics',
        '----------',
        'mentality_aggression',
        'mentality_interceptions',
        'mentality_positioning',
        'mentality_vision',
        'mentality_penalties',
        'mentality_composure',
        ]

NUMERICS = ['overall',
     'potential',
     'wage_eur',
     'value_eur',
     'pace',
     'shooting',
     'passing',
     'dribbling',
     'defending',
     'shooting',
     'passing',
     'attacking_crossing',
     'attacking_finishing',
     'attacking_heading_accuracy',
     'attacking_short_passing',
     'attacking_volleys',
     'defending_marking_awareness',
     'defending_standing_tackle',
     'defending_sliding_tackle',
     'goalkeeping_diving',
     'goalkeeping_handling',
     'goalkeeping_kicking',
     'goalkeeping_positioning',
     'goalkeeping_reflexes',
     'goalkeeping_speed',
     'physic',
     'height_cm',
     'weight_kg',
     'age',
     'power_shot_power',
     'power_jumping',
     'power_stamina',
     'power_strength',
     'power_long_shots',
     'mentality_aggression',
     'mentality_interceptions',
     'mentality_positioning',
     'mentality_vision',
     'mentality_penalties',
     'mentality_composure',
     ]


if __name__ == "__main__":
    main()

