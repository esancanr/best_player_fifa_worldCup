import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

#--------------------------------------------------------
# DATA EXTRACTION
#--------------------------------------------------------
df = pd.read_csv('data/players_22.csv', low_memory=False)
df = df[['short_name', 'age', 'nationality_name','overall', 'potential',
         'club_name', 'value_eur', 'wage_eur', 'player_positions']]

df['player_positions'] = df['player_positions'].str.split(',', expand=True)[0]
df.dropna(inplace=True)

players_missing_games = ['K. Benzema', 'N. Kanté', 'P. Pogba', 'C. Nkunku', 'M. Maignan', 'A. Martial', 'S. Mané', 
                         'M. Reus', 'D. Jota', 'P. Neto', 'B. Chilwell', 'R. James', 'K. Walker', 'G. Wijnaldum', 'G. Jesus',
                         'A. Telles', 'R. Araújo', 'J. Corona', 'M. Robinson']

delete_index = df[df['short_name'].isin(players_missing_games)].index
df.drop(delete_index, axis=0, inplace=True)


teams_worldcup = ['Qatar', 'Ecuador', 'Senegal', 'Netherlands', 'England', 'Iran', 'USA', 'Wales', 'Argentina', 'Saudi Arabia', 'Mexico',
    'Poland', 'France', 'Australia', 'Denmark', 'Tunisia','Spain', 'Costa Rica', 'Germany', 'Japan', 'Belgium', 'Canada', 'Morocco',
    'Croatia', 'Brazil', 'Serbia', 'Switzerland','Cameroon', 'Portugal', 'Ghana', 'Uruguay','South Korea']
df = df[df['nationality_name'].isin(teams_worldcup)]
df.sort_values(by=['overall', 'potential', 'value_eur'], ascending=False, inplace=True)

#--------------------------------------------------------
# BEST PLAYER SCORE
#--------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 5), tight_layout=True)

sns.histplot(df, x='overall', binwidth=1)
bins = np.arange(df['overall'].min(), df['overall'].max(), 1)
plt.xticks(bins)
plt.show()

#--------------------------------------------------------
# DREAM TEAM FIFA WORLD CUP 2022
#--------------------------------------------------------
df.drop_duplicates('player_positions')

#--------------------------------------------------------
# THE BEST PLAYER FROM EACH WORLD CUP COUNTRY
#--------------------------------------------------------
df_best_player = df.copy()
df_best_player = df_best_player.drop_duplicates('nationality_name').reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)

sns.barplot(data=df_best_player, x='overall', y='short_name')
plt.show()

#--------------------------------------------------------
# THE BEST TEAM FROM EACH COUNTRY
#--------------------------------------------------------
def get_best_team(country):
    df_team = df.copy()
    df_team = df_team.groupby(['nationality_name', 'player_positions']).head(2)
    df_team = df_team[df_team['nationality_name'] == country].sort_values(by=['player_positions', 'overall', 'potential'], ascending=False)
    return df_team

average_score = [get_best_team(team)['overall'].mean() for team in teams_worldcup]

df_average_score = pd.DataFrame({'Teams': teams_worldcup, 'Average_score': average_score})
df_average_score = df_average_score.dropna()
df_average_score = df_average_score.sort_values(by='Average_score', ascending=False)

fig, ax = plt.subplots(figsize=(10, 6), tight_layout=True)
sns.barplot(df_average_score[:10], x='Teams', y='Average_score')
plt.show()

#--------------------------------------------------------
# BEST LINEUP 
#--------------------------------------------------------
dict_positions = {
    '4-3-3': ['GK', 'RB', 'CB', 'CB', 'LB', 'CDM', 'CM', 'CAM', 'RW', 'ST', 'LV'],
    '4-4-2': ['GK', 'RB', 'CB', 'CB', 'LB', 'RM', 'CM', 'CM', 'LM', 'ST', 'ST'],
    '4-2-3-1': ['GK', 'RB', 'CB', 'CB', 'LB', 'CDM', 'CDM', 'CAM', 'CAM', 'CAM', 'ST'],
}

def get_best_lineup(nationality, lineup):
    lineup_count = [lineup.count(i) for i in lineup]
    df_lienup = pd.DataFrame({'position': lineup, 'count': lineup_count})
    position_norepeats = df_lienup[df_lienup['count'] <= 1]['position'].values
    position_repeats = df_lienup[df_lienup['count'] > 1]['position'].values

    df_team = get_best_team(nationality)

    df_lineup = pd.concat([
        df_team[df_team['player_positions'].isin(position_norepeats)].drop_duplicates('player_positions', keep='first'),
        df_team[df_team['player_positions'].isin(position_repeats)]
    ])
    return df_lineup[['short_name', 'overall', 'club_name', 'player_positions']]

print(get_best_lineup('Brazil', dict_positions['4-4-2']))