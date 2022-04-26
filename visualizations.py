import pandas as pd
import os
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np

year = []
overall = []
pace = []
shooting = []
passing = []
defending = []
physic = []
dribbling = []
main_stats = [overall, pace, shooting, passing, defending, physic, dribbling]

national_teams = []
national_team_scores = []

for file in os.listdir("data/players"):
    if (file.split("_")[0] == 'female'):
        continue
    data = pd.read_csv("data/players/" + file)
    data.sort_values(by=['overall'])
    data = data.fillna(0)
    
    year.append("20" + file.split(".")[0][-2:])
    overall.append(mean(data['overall'][:20]))
    pace.append(round(mean([data_point for data_point in data['pace'][:20] if data_point != 0]), 2))
    shooting.append(round(mean([data_point for data_point in data['shooting'][:20] if data_point != 0]), 2))
    passing.append(round(mean([data_point for data_point in data['passing'][:20] if data_point != 0]), 2))
    defending.append(round(mean([data_point for data_point in data['defending'][:20] if data_point != 0]), 2))
    physic.append(round(mean([data_point for data_point in data['physic'][:20] if data_point != 0]), 2))
    dribbling.append(round(mean([data_point for data_point in data['dribbling'][:20] if data_point != 0]), 2))

    data['nation_team_id'].replace(0.0, np.nan, inplace=True)
    data.dropna(subset=['nation_team_id'], inplace=True)
    top_20_national_teams = data.groupby(by=["nationality_name"]).mean()['overall'].to_frame().reset_index().sort_values(by=['overall'], ascending=False)[:20]
    national_teams.append(top_20_national_teams['nationality_name'])
    national_team_scores.append(top_20_national_teams['overall'])
    

year.reverse()
stat_labels = ['Overall', 'Pace', 'Shooting', 'Passing', 'Defending', 'Physic', 'Dribbling']
for idx, stat in enumerate(main_stats):    
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'visualizations/')
    file_name = stat_labels[idx] + ' Averages for Top 20 Players 2k15-22'

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    stat.reverse()
    plt.figure()
    plt.plot(year, stat)
    plt.title(stat_labels[idx] + ' Average For Top 20 Players Vs Year')
    plt.xlabel('Year')
    plt.ylabel(stat_labels[idx])
    plt.savefig(results_dir + file_name)

national_teams.reverse()
national_team_scores.reverse()
for y, team, score in zip(year, national_teams, national_team_scores):
    script_dir = os.path.dirname(__file__)
    results_dir = os.path.join(script_dir, 'visualizations/')
    file_name = 'Top 20 National Teams for ' + y

    fig, ax = plt.subplots(figsize =(16, 9))
    ax.barh(team, score)

    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)

    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
                str(round((i.get_width()), 2)),
                fontsize = 10, fontweight ='bold',
                color ='grey')

    ax.set_title("Top 20 National Teams for " + y)
    plt.xlabel('Avg Player Score for Team')
    plt.ylabel('National Team')
    plt.savefig(results_dir + file_name)