import pandas as pd
from fifa_app.data_service import MongoAPI

api = MongoAPI()
def main():
    pd.options.display.max_columns = 999
    api = MongoAPI()
    type_q = choose_query()
    if type_q == 'Basic Search':
        ret = basic_search(api)
        print(ret)
        main()
    elif type_q == 'Advanced Search':
        ret = advanced_search(api)
        print(ret)
        main()
    elif type_q == 'Quit':
        return 'Quit'
    else:
        ret = ultimate_team_handler(api)


def ultimate_team_handler(api):
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
        input_team(api)
        main()
    elif user_input == 2:
        replace_player(api)
        main()
    elif user_input == 3:
        recommendation(api)
        main()



def input_team(api):
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
            rets = api.get_players({'year': year, 'short_name': names[c]})
            c += 1
        if rets['num_results'] == 0:
            print('Player not found')
        else:
            rets = rets["players"][0]
            players.append({rets['player_positions'][0]: rets['short_name']})
    print("Team Successfully Inputted")
    api.create_team(username, teamname, year, players)
    return print(pd.DataFrame(api.get_team(username,teamname)["players"]))

def replace_player(api):
    team = None
    while team == None:
        username = input("Input your username\n")
        team_name = input("Input your team name\n")
        team = api.get_team(username, team_name)
        if team == None:
            print("Username Or Team Name not recognised\n")
    year = choose_year()

    player = input("Input the name of the player that you want to add to the team: First Last\n")
    player_to_replace = input("Input the name of the player that you want to replace: First Last\n")


    names = get_names(player)
    rets = {'num_results': 0}
    c = 0
    while rets['num_results'] == 0 and c < len(names):
        rets = api.get_players({'year': year, 'short_name': names[c]})
        c += 1
    if rets['num_results'] == 0:
        print('Player not found')
    else:
        new_player = rets['players'][0]["short_name"]

    previous_team = pd.DataFrame(team["players"])
    names_rep = get_names(player_to_replace)
    for i in names_rep:
        if i in list(previous_team['short_name']):
            print(i, "previous player")
            api.edit_team(username, team_name, year, i, new_player)
            print("Player successfully returned")
            break
        elif i == names_rep[-1]:
            print('Player to replace not on team')
    team = api.get_team(username, team_name)
    print(pd.DataFrame(team["players"]))

def recommendation(api):
    year = choose_year()
    position = None
    stat = None
    print("input a position from the following list")
    for x in POSITIONS:
        print(x)
    while position not in POSITIONS:
        if position != None:
            print("Invalid position, enter one from the list")
        position = input().upper()

    wage = int(input("input a maximum salary\n"))
    print("select a stat to maxamize")
    for x in STATSLIST:
        print(x)
    while stat not in STATSLIST:
        if stat != None:
            print("Invalid stat, enter one from the list")
        stat = input().lower()

    print(pd.DataFrame(api.get_player_recommendation(year,position, wage,stat)['players']))

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



def basic_search(api):
    year = choose_year()
    constraints = choose_constraints()
    constraints['year'] = year
    players = api.get_players(constraints)["players"]
    df = pd.DataFrame(players)
    return df

def get_names(name):
    names = name.split(" ")
    return [name, names[0][0]+". "+names[1], names[0], names[1]]

def advanced_search(api):
    year = choose_year()
    player = input("input a player name: First Last\n")
    names = get_names(player)
    rets = {'num_results': 0}
    c=0
    while rets['num_results'] == 0 and c < len(names):
        rets = api.get_players({'year':year, 'short_name': names[c]})
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
        players = api.get_players(rets)["players"]
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
