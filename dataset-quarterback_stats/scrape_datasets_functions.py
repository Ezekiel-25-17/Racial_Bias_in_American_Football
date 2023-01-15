import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup



def get_nfl_stats(year):

  ### PASSING STATS  
  # Make a request to the website
  response = requests.get(f'https://www.pro-football-reference.com/years/{year}/passing.htm')

  # Parse the HTML content
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find the table with the stats
  table = soup.find('table', {'id': 'passing'})

  # Create an empty list to store the data
  data = []

  # Iterate over the rows of the table and store the stats
  for row in table.find_all('tr'):
      cells = row.find_all('td')
      if len(cells) > 0:
          player = cells[0]
          team = cells[1]
          age = cells[2]
          position = cells[3]
          games = cells[4]
          games_started = cells[5]
          qb_record = cells[6]
          completions = cells[7]
          attempts = cells[8]
          completion_percentage = cells[9]
          yards = cells[10]
          passing_touchdowns = cells[11]
          touchdown_percentage = cells[12]
          interceptions = cells[13]
          interceptions_percentage = cells[14]
          first_downs_passing = cells[15]
          longest_completion = cells[16]
          yards_per_attempt = cells[17]
          adjusted_yards_per_attempt = cells[18]
          yards_per_completion = cells[19]
          yards_per_game = cells[20]
          rate = cells[21]
          qbr = cells[22]
          sacks = cells[23]
          yards_lost = cells[24]
          sack_percentage = cells[25]
          net_yards_attempt = cells[26]
          adjusted_net_yards_attempt = cells[27]
          fourth_q_comebacks = cells[28]
          game_winning_drives = cells[29] 

          data.append([player.text, team.text, age.text, position.text, games.text, games_started.text, qb_record.text, completions.text,
                attempts.text, completion_percentage.text, yards.text, passing_touchdowns.text, touchdown_percentage.text, 
                interceptions.text, interceptions_percentage.text, first_downs_passing.text, longest_completion.text, yards_per_attempt.text,
                adjusted_yards_per_attempt.text, yards_per_completion.text, yards_per_game.text, rate.text, qbr.text, sacks.text, yards_lost.text, 
                sack_percentage.text, net_yards_attempt.text, adjusted_net_yards_attempt.text, fourth_q_comebacks.text, game_winning_drives.text])

  # Create a pandas DataFrame from the data
  passing = pd.DataFrame(data, columns=['Player', 'Team', 'Age', 'Position', 'Games', 'Games Started', 'W/L Record', 'Completions', 'Attempts',
                            'Cmp %', 'Passing Yards', 'Passing TDs', 'TD %', 'Interceptions', 'Int %', 'Passing 1D', 'Longest Cmp',
                            'Yds/Att', 'Adj Yds/Att', 'Yds/Cmp', 'Yds/G', 'Rating', 'QBR', 'Sacks', 'Yds Lost', 'Sack %', 'Net Yds/Att',
                            'Adj Net Yds/Att', '4th Quarter Comeback', 'Game Winning Drives'])
  
  # Selecting QBs
  passing = passing[passing['Position'] == 'QB'].reset_index(drop=True)
  passing['Player'] = passing['Player'].str.replace('*', '').str.replace('+', '')
  
  ### RUSHING STATS  
  # Make a request to the website
  response = requests.get(f'https://www.pro-football-reference.com/years/{year}/rushing.htm')

  # Parse the HTML content
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find the table with the stats
  table = soup.find('table', {'id': 'rushing'})

  # Create an empty list to store the data
  data = []

  # Iterate over the rows of the table and store the stats
  for row in table.find_all('tr'):
      cells = row.find_all('td')
      if len(cells) > 0:
          player = cells[0]
          team = cells[1]
          age = cells[2]
          position = cells[3]
          games = cells[4]
          games_started = cells[5]
          rushing_attempts = cells[6]
          rushing_yards = cells[7]
          rushing_touchdowns = cells[8]
          first_downs_rushing = cells[9]
          longest_run = cells[10]
          rushing_yards_per_attempt = cells[11]
          rushing_yards_per_game = cells[12]
          fumbles = cells[13]

          data.append([player.text, team.text, age.text, position.text, games.text, games_started.text, rushing_attempts.text, rushing_yards.text,
                       rushing_touchdowns.text, first_downs_rushing.text, longest_run.text, rushing_yards_per_attempt.text, 
                       rushing_yards_per_game.text, fumbles.text])

  # Create a pandas DataFrame from the data
  rushing = pd.DataFrame(data, columns=['Player', 'Team', 'Age', 'Position', 'Games', 'Games Started', 'Rushing Attempts', 'Rushing Yards', 
                                        'Rushing TDs', 'Rushing 1D', 'Longest Run', 'Rush Yds/Att', 'Rush Yds/Game', 'Fumbles'])
  
  # Select QBs
  rushing = rushing[rushing['Position'] == 'QB'].reset_index(drop=True)
  rushing['Player'] = rushing['Player'].str.replace('*', '').str.replace('+', '')
  
  # Merge the final Dataset
  nfl = passing.merge(rushing, how='left', on=['Player', 'Team', 'Age', 'Position', 'Games', 'Games Started'])
  nfl.insert(1, 'Year', year) # Create year column

  nfl.insert(8, 'Wins', 0)
  nfl.insert(9, 'Losses', 0)
  nfl.insert(10, 'Draws', 0)

  nfl.fillna(0, inplace=True)
  nfl['W/L Record'] = nfl['W/L Record'].replace('', '0-0-0')

  for index, row in nfl.iterrows():
    tmp = str(row['W/L Record']).split('-')
    while len(tmp) != 3:
      tmp.append(0)
    nfl.iat[index, 8] = int(tmp[0])
    nfl.iat[index, 9] = int(tmp[1])
    nfl.iat[index, 10] = int(tmp[2])

  nfl.drop('W/L Record', axis=1, inplace=True)

  return nfl





def get_cfb_stats(year):

  # Make a request to the website
  response = requests.get(f'https://www.sports-reference.com/cfb/years/{year}-passing.html')

  # Parse the HTML content
  soup = BeautifulSoup(response.content, 'html.parser')

  # Find the table with the stats
  table = soup.find('table', {'id': 'passing'})

  # Create an empty list to store the data
  data = []

  # Iterate over the rows of the table and store the stats
  for row in table.find_all('tr'):
      cells = row.find_all('td')
      if len(cells) > 0:
          player = cells[0]
          school = cells[1]
          conference = cells[2]
          games = cells[3]
          completions = cells[4]
          attempts = cells[5]
          completion_percentage = cells[6]
          yards = cells[7]
          yards_per_attempt = cells[8]
          adjusted_yards_per_attempt = cells[9]
          touchdowns = cells[10]
          interceptions = cells[11]
          rate = cells[12]
          rushing_attempts = cells[13]
          rushing_yards = cells[14]
          rushing_average = cells[15]
          rushing_touchdowns = cells[16]

          data.append([player.text, school.text, conference.text, games.text, completions.text, attempts.text, completion_percentage.text,
                       yards.text, yards_per_attempt.text, adjusted_yards_per_attempt.text, touchdowns.text, interceptions.text, rate.text,
                       rushing_attempts.text, rushing_yards.text, rushing_average.text, rushing_touchdowns.text])

  # Create a pandas DataFrame from the data
  cfb = pd.DataFrame(data, columns=['Player', 'School', 'Conference', 'Games', 'Completions', 'Attempts', 'Completion %', 'Passing Yards',
                                        'Yds/Att', 'Adj Yds/Att', 'Passing TDs', 'Interceptions', 'Rating', 'Rushing Attempts', 
                                        'Rushing Yards', 'Rush Yds/Att', 'Rushing TDs'])
  
  # Clean 'Player' column
  cfb['Player'] = cfb['Player'].str.replace('*', '')

  return cfb





def get_career_stats(years, path, league):

  if league == 'nfl':
    
    dfs = [pd.read_csv(os.path.join(path, league + '_' + str(year) +'.csv')) for year in years]
    df = pd.concat(dfs).reset_index(drop=True)
    df.fillna(0, inplace=True)
    players = list(set(df['Player']))
    career = pd.DataFrame(columns=['Player', 'Years', 'Position', 'Games', 'Games Started', 'Wins', 'Losses', 'Draws', 'Completions',
          'Attempts', 'Cmp %', 'Passing Yards', 'Passing TDs', 'TD %', 'Interceptions', 'Int %', 'Passing 1D', 'Longest Cmp',
          'Yds/Att', 'Adj Yds/Att', 'Yds/Cmp', 'Yds/G', 'Rating', 'Sacks', 'Yds Lost', 'Sack %', 'Net Yds/Att', 'Adj Net Yds/Att',
          '4th Quarter Comeback', 'Game Winning Drives', 'Rushing Attempts', 'Rushing Yards', 'Rushing TDs', 'Rushing 1D', 
          'Longest Run', 'Rush Yds/Att', 'Rush Yds/Game', 'Fumbles'])

    for player in players:
      tmp = df[df['Player']==player].reset_index(drop=True)

      warnings.simplefilter(action='ignore', category=RuntimeWarning)

      # Components for "Rating"
      a = ((tmp['Completions'].sum() / tmp['Attempts'].sum()) - 0.3) * 5
      b = ((tmp['Passing Yards'].sum() / tmp['Attempts'].sum()) - 3) * 0.25
      c = (tmp['Passing TDs'].sum() / tmp['Attempts'].sum()) * 20
      d = 2.375 - ((tmp['Interceptions'].sum() / tmp['Attempts'].sum()) * 25)

      p = {'Player': player,
          'Years' : len(tmp),
          'Position' : tmp['Position'][0],
          'Games' : tmp['Games'].sum(),
          'Games Started' : tmp['Games Started'].sum(),
          'Wins' : tmp['Wins'].sum(),
          'Losses' : tmp['Losses'].sum(),
          'Draws' : tmp['Draws'].sum(),
          'Completions' : tmp['Completions'].sum(),
          'Attempts' : tmp['Attempts'].sum(),
          'Cmp %' : 100 * tmp['Completions'].sum() / tmp['Attempts'].sum(),
          'Passing Yards' : tmp['Passing Yards'].sum(),
          'Passing TDs' : tmp['Passing TDs'].sum(),
          'TD %' : 100 * tmp['Passing TDs'].sum() / tmp['Attempts'].sum(),
          'Interceptions' : tmp['Interceptions'].sum(),
          'Int %' : 100 * tmp['Interceptions'].sum() / tmp['Attempts'].sum(),
          'Passing 1D' : tmp['Passing 1D'].sum(),
          'Longest Cmp' : tmp['Longest Cmp'].max(),
          'Yds/Att' : tmp['Passing Yards'].sum() / tmp['Attempts'].sum(),
          'Adj Yds/Att' : (tmp['Passing Yards'].sum() + 20*tmp['Passing TDs'].sum() - 45*tmp['Interceptions'].sum()) / tmp['Attempts'].sum(),
          'Yds/Cmp' : tmp['Passing Yards'].sum() / tmp['Completions'].sum(),
          'Yds/G' : tmp['Passing Yards'].sum() / tmp['Games'].sum(),
          'Rating' : ((a + b + c + d) / 6) * 100,
          'Sacks' : tmp['Sacks'].sum(),
          'Yds Lost' : tmp['Yds Lost'].sum(),
          'Sack %' : 100 * tmp['Sacks'].sum() / (tmp['Sacks'].sum() + tmp['Attempts'].sum()),
          'Net Yds/Att' : (tmp['Passing Yards'].sum() - tmp['Yds Lost'].sum()) / (tmp['Sacks'].sum() + tmp['Attempts'].sum()),
          'Adj Net Yds/Att' : (tmp['Passing Yards'].sum() - tmp['Yds Lost'].sum() + 20*tmp['Passing TDs'].sum() - 45*tmp['Interceptions'].sum()) / (tmp['Sacks'].sum() + tmp['Attempts'].sum()),
          '4th Quarter Comeback' : tmp['4th Quarter Comeback'].sum(),
          'Game Winning Drives' : tmp['Game Winning Drives'].sum(),
          'Rushing Attempts' : tmp['Rushing Attempts'].sum(),
          'Rushing Yards' : tmp['Rushing Yards'].sum(),
          'Rushing TDs' : tmp['Rushing TDs'].sum(),
          'Rushing 1D' : tmp['Rushing 1D'].sum(),
          'Longest Run' : tmp['Longest Run'].max(),
          'Rush Yds/Att' : tmp['Rushing Yards'].sum() / tmp['Rushing Attempts'].sum(),
          'Rush Yds/Game' : tmp['Rushing Yards'].sum() / tmp['Games'].sum(),
          'Fumbles' : tmp['Fumbles'].sum()}

      career = pd.concat([career, pd.DataFrame(p, index=[0])]).reset_index(drop=True).round(2)
      career.fillna(0, inplace=True)


  elif league == 'cfb':

    dfs = [pd.read_csv(os.path.join(path, league + '_' + str(year) +'.csv')) for year in years]
    df = pd.concat(dfs).reset_index(drop=True)
    df.fillna(0, inplace=True)
    players = list(set(df['Player']))
    career = pd.DataFrame(columns=['Player', 'Years', 'Completions', 'Attempts', 
          'Completion %', 'Passing Yards', 'Yds/Att', 'Adj Yds/Att', 
          'Passing TDs', 'Interceptions', 'Rating', 'Rushing Attempts', 
          'Rushing Yards', 'Rush Yds/Att', 'Rushing TDs'])
    
    for player in players:
      tmp = df[df['Player']==player].reset_index(drop=True)

      warnings.simplefilter(action='ignore', category=RuntimeWarning)

      # Components for "Rating"
      a = tmp['Passing Yards'].sum() * 8.4
      b = tmp['Passing TDs'].sum() * 330
      c = tmp['Completions'].sum() * 100
      d = tmp['Interceptions'].sum() * 200

      p = {'Player': player,
          'Years' : len(tmp),
          'Completions' : tmp['Completions'].sum(),
          'Attempts' : tmp['Attempts'].sum(),
          'Completion %' : tmp['Completions'].sum() / tmp['Attempts'].sum(),
          'Passing Yards' : tmp['Passing Yards'].sum(),
          'Yds/Att' : tmp['Passing Yards'].sum() / tmp['Attempts'].sum(),
          'Adj Yds/Att' : (tmp['Passing Yards'].sum() + 20*tmp['Passing TDs'].sum() - 45*tmp['Interceptions'].sum()) / tmp['Attempts'].sum(),
          'Passing TDs' : tmp['Passing TDs'].sum(),
          'Interceptions' : tmp['Interceptions'].sum(),
          'Rating' : (a + b + c - d) / tmp['Attempts'].sum(),
          'Rushing Attempts' : tmp['Rushing Attempts'].sum(),
          'Rushing Yards' : tmp['Rushing Yards'].sum(),
          'Rushing TDs' : tmp['Rushing TDs'].sum(),
          'Rushing TDs' : tmp['Rushing TDs'].sum()}
      
      career = pd.concat([career, pd.DataFrame(p, index=[0])]).reset_index(drop=True).round(2)
      career.fillna(0, inplace=True)
  
  return career 

