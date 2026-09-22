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


teams = ['Qatar', 'Ecuador', 'Senegal', 'Netherlands', 'England', 'Iran', 'USA', 'Wales', 'Argentina', 'Saudi Arabia', 'Mexico',
    'Poland', 'France', 'Australia', 'Denmark', 'Tunisia','Spain', 'Costa Rica', 'Germany', 'Japan', 'Belgium', 'Canada', 'Morocco',
    'Croatia', 'Brazil', 'Serbia', 'Switzerland','Cameroon', 'Portugal', 'Ghana', 'Uruguay','South Korea']
df = df[df['nationality_name'].isin(teams)]
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
