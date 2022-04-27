import pandas as pd
import requests
import json
from fifa_app.type_map import projections

API_ENDPOINT = "http://127.0.0.1:5000/api/v1"
HEADERS = {'content-type': 'application/json'}

def main():
    display = pd.options.display

    display.max_columns = 999
    display.max_rows = 1000
    display.max_colwidth = 199
    display.width = 1000

    type_q = choose_query()
    if type_q == 'Basic Search':
        ret = basic_search()
        print(ret)
        main()
    elif type_q == 'Advanced Search':
        ret = advanced_search()
        print(ret)
        main()
    elif type_q == 'Quit':
        return 'Quit'
    else:
        ret = ultimate_team_handler()


def ultimate_team_handler():
    queries = {1: 'Input Team', 2: 'Replace player', 3: 'Replacement recommender'}
    prompting = True
    q = prompt_builder(queries)
    while prompting:
        user_input = int(input(q))
        if user_input in queries.keys():
            prompting = False
        else:
            print('INPUT NOT RECOGNIZED')

    if user_input == 1:
        input_team()
        main()
    elif user_input == 2:
        replace_player()
        main()
    elif user_input == 3:
        recommendation()
        main()



def input_team():
    players = []
    year = choose_year()
    username = input("\nEnter a username: \n")
    teamname = input("\nEnter a team name: \n")
    while len(players) < 11:
        player = input("\nInput a player that you would like to add to your team: First Last\n")
        names = get_names(player)
        rets = {'num_results': 0}
        c = 0
        while rets['num_results'] == 0 and c < len(names):
            body = {'year': year, 'short_name': names[c]}
            rets = requests.get(f"{API_ENDPOINT}/players/", params=body).json()
            c += 1
        if rets['num_results'] == 0:
            print('Player not found')
        else:
            rets = list(rets["players"])[0]
            players.append({rets['player_positions'][0]: rets['short_name']})
    print("Team Successfully Inputted")
    body = {
        "user": username,
        "team_name": teamname,
        "year": year,
        "players": players,
    }
    requests.post(f"{API_ENDPOINT}/team/", data=json.dumps(body), headers=HEADERS)
    body = {"username":username,"team_name":teamname}
    return print(pd.DataFrame(requests.get(f"{API_ENDPOINT}/team/", params=body).json()["players"]))

def replace_player():
    team = None
    while team == None:
        username = input("\nInput your username\n")
        teamname = input("\nInput your team name\n")
        body = {"username":username,"team_name":teamname}
        team = requests.get(f"{API_ENDPOINT}/team/", params=body).json()
        if team == None:
            print("Username Or Team Name not recognised\n")
    year = choose_year()

    player = input("\nInput the name of the player that you want to add to the team: First Last\n")
    player_to_replace = input("\nInput the name of the player that you want to replace: First Last\n")


    names = get_names(player)
    rets = {'num_results': 0}
    c = 0
    while rets['num_results'] == 0 and c < len(names):
        body = {'year': year, 'short_name': names[c]}
        rets = requests.get(f"{API_ENDPOINT}/players/", params=body).json()
        c += 1
    if rets['num_results'] == 0:
        print('Player not found')
    else:
        new_player = list(rets['players'])[0]["short_name"]

    previous_team = pd.DataFrame(team["players"])
    names_rep = get_names(player_to_replace)
    for i in names_rep:
        if i in list(previous_team['short_name']):
            print(i, "previous player")
            body = {
                "user": username, 
                "team_name": teamname, 
                "year": year, 
                "original_player_name": i, 
                "replacing_player_name": new_player,
            }
            requests.put(f"{API_ENDPOINT}/team/edit/", data=json.dumps(body), headers=HEADERS)
            print("Player successfully returned")
            break
        elif i == names_rep[-1]:
            print('Player to replace not on team')
    body = {"username": username, "team_name": teamname}
    team = requests.get("http://127.0.0.1:5000/api/v1/team/", params=body).json()
    print(pd.DataFrame(team["players"]))

def recommendation():
    year = choose_year()
    position = None
    stat = None
    print("\nInput a position from the following list\n")
    for x in POSITIONS:
        print(x)
    while position not in POSITIONS:
        if position != None:
            print("\nInvalid position, enter one from the list\n")
        position = input().upper()

    wage = int(input("\ninput a maximum salary\n"))
    print("\nselect a stat to maxamize\n")
    for x in STATSLIST:
        print(x)
    while stat not in STATSLIST:
        if stat != None:
            print("\nInvalid stat, enter one from the list\n")
        stat = input().lower()
    body = {
        "year": year,
        "wage": wage,
        "position": position,
        "stat_to_optimize": stat,
    }
    print(pd.DataFrame(requests.get(f"{API_ENDPOINT}/team/replace/", params=body).json()['players']))

def choose_query():
    print("Fifa Search engine V1\n")
    queries = {1: 'Basic Search', 2: 'Advanced Search', 3: 'Ultimate Team Recommender', 4: 'Quit'}
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
    projection = choose_projection()
    constraints = choose_constraints()
    constraints['year'] = year
    constraints['projection'] = projection
    players = requests.get(f"{API_ENDPOINT}/players/", params=constraints).json()["players"]
    df = pd.DataFrame(players)
    print('\n')
    return df
    
def sort_dataframe(df):
    first_column = df.pop('short_name')
    second_column = df.pop('overall')
    df.insert(0, 'short_name', first_column)
    df.insert(1, 'overall', second_column)
    return df

def choose_projection():
    projection = None
    print('\nAvailable stat projections are: "basic", "defending", "attacking", "goalkeeping", "mentality", and "physical"')
    while projection is None:
        temp = input('Please enter a projection type (stat-group) to return. Options are above: \n')
        if temp in list(projections.keys()):
            break
        else:
            print('\nPlease input a projection type from the list above!')
    return temp

def get_names(name):
    names = name.split(" ")
    try:
        potential_names = [name, names[0][0]+". "+names[1], names[0], names[1]]
    except:
        potential_names = names
    return potential_names

def advanced_search():
    year = choose_year()
    player = input("\nInput a player name: First Last\n")
    names = get_names(player)
    rets = {'num_results': 0}
    c=0
    while rets['num_results'] == 0 and c < len(names):
        body = {'year':year, 'short_name': names[c]}
        rets = requests.get(f"{API_ENDPOINT}/players/", params=body).json()
        c+=1
    if len(rets) == 0:
        print('Player not found')
    else:
        projection = choose_projection()
        constraints = choose_constraints(counter=1)
        rets = pd.DataFrame(rets['players'])
        rets = (rets[['club_position', 'overall', 'pace', 'shooting', 'passing', 'dribbling', 'defending']].iloc[0]).to_dict()
        for key in constraints.keys():
            rets[key] = constraints[key]

        rets['year'] = year
        rets['projection'] = projection
        players = requests.get(f"{API_ENDPOINT}/players/", params=rets).json()["players"]
        df = pd.DataFrame(players)
        df = sort_dataframe(df)
        return df

def choose_constraints(counter=0):
    print("\nFor a list of fields to search on, type --help")
    stop = False
    constraints = {}
    while not stop:
        if len(constraints) != 0:
            counter +=1
        if counter == 0:
            temp = input('Enter field and value separated by a comma. Value must be 1-99 for attributes.\n')
        else:
            temp = input('\nType \'search\' to search on inputted constraints or add another: Enter field and value separated by comma. Value must be 1-99 for attributes\n')
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
        year = input("\nInput a year to search 2015-2022\n")
    return year


HELP = ['Basic Statistics',
        '----------------',
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
        "\n",
        'Attacking Statistics',
        '--------------------',
        'shooting',
        'passing',
        'attacking_crossing',
        'attacking_finishing',
        'attacking_heading_accuracy',
        'attacking_short_passing',
        'attacking_volleys',
        "\n",
        'Defense Statistics',
        '------------------',
        'defending_marking_awareness',
        'defending_standing_tackle',
        'defending_sliding_tackle',
        "\n",
        'Goalkeeping',
        '-----------',
        'goalkeeping_diving',
        'goalkeeping_handling',
        'goalkeeping_kicking',
        'goalkeeping_positioning',
        'goalkeeping_reflexes',
        'goalkeeping_speed',
        "\n",
        'Physical Statistics',
        '-------------------',
        'physic',
        'height_cm',
        'weight_kg',
        'age',
        'power_shot_power',
        'power_jumping',
        'power_stamina',
        'power_strength',
        'power_long_shots',
        "\n",
        'Mentality Statistics',
        '--------------------',
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


STATSLIST= ['overall', 'pace', 'shooting', 'passing', 'attacking', 'dribbling', 'defending']

POSITIONS = ['LS',
 'ST',
 'RS',
 'LW',
 'LF',
 'CF',
 'RF',
 'RW',
 'LAM',
 'CAM',
 'RAM',
 'LM',
 'LCM',
 'CM',
 'RCM',
 'RM',
 'LWB',
 'LDM',
 'CDM',
 'RDM',
 'RWB',
 'LB',
 'LCB',
 'CB',
 'RCB',
 'RB']


main()

