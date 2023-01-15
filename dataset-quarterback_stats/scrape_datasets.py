from scrape_datasets_functions import get_nfl_stats, get_cfb_stats, get_career_stats
import pandas as pd
import shutil
import os

### SCRAPE A DATASET FOR EACH SEASON

# Select path where to save the datasets
cwd = os.getcwd()
nfl_path = 'nfl_datasets'
cfb_path = 'cfb_datasets'

# Select Years
start = 2006
end = 2021
years = list(range(start, end+1))

# Create directories to store the datasets
if os.path.exists(os.path.join(cwd, nfl_path)):
    shutil.rmtree(os.path.join(cwd, nfl_path))
    os.mkdir(os.path.join(cwd, nfl_path))
    print('Directory Replaced')
else:
    os.mkdir(os.path.join(cwd, nfl_path))
    print('Directory Created')

if os.path.exists(os.path.join(cwd, cfb_path)):
    shutil.rmtree(os.path.join(cwd, cfb_path))
    os.mkdir(os.path.join(cwd, cfb_path))
    print('Directory Replaced')
else:
    os.mkdir(os.path.join(cwd, cfb_path))
    print('Directory Created')

# Scrape NFL datasets
for year in years:
    df = get_nfl_stats(year)
    df.to_csv(os.path.join(nfl_path, f'nfl_{year}.csv'), index=False)

# Scrape CLB datasets
for year in years:    
    df = get_cfb_stats(year)
    df.to_csv(os.path.join(cfb_path, f'cfb_{year}.csv'), index=False)


### CONVERT SEASONAL DATASETS TO CAREER STATS

df_nfl = get_career_stats(years, nfl_path, league='nfl') # NFL
df_cfb = get_career_stats(years, cfb_path, league='cfb') # CFB

# Add Race Variable
df = pd.read_csv('census.csv')
df_nfl = df_nfl.merge(df, how='left', on='Player')
df_nfl = df_nfl[['Player', 'Years', 'Position', 'Race', 'Games', 'Games Started',
       'Wins', 'Losses', 'Draws', 'Completions', 'Attempts', 'Cmp %', 
       'Passing Yards', 'Passing TDs', 'TD %', 'Interceptions', 'Int %', 
       'Passing 1D', 'Longest Cmp', 'Yds/Att', 'Adj Yds/Att', 'Yds/Cmp', 'Yds/G', 
       'Rating', 'Sacks', 'Yds Lost', 'Sack %', 'Net Yds/Att', 'Adj Net Yds/Att',
       '4th Quarter Comeback', 'Game Winning Drives', 'Rushing Attempts',
       'Rushing Yards', 'Rushing TDs', 'Rushing 1D', 'Longest Run',
       'Rush Yds/Att', 'Rush Yds/Game', 'Fumbles']]

df_nfl = df_nfl.sort_values('Player').reset_index(drop=True)
df_nfl.to_csv(f'nfl_{start}-{end}.csv', index=False)

df_cfb = df_cfb.sort_values('Player').reset_index(drop=True)
df_cfb.to_csv(f'cfb_{start}-{end}.csv', index=False)

