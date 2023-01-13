import pandas as pd
import shutil
import json
import os

# Select path where to save the converted datasets and transcripts
cwd = os.getcwd()
data_path = os.path.join('dataset_converted', 'mentions')
tr_path = 'dataset_converted'

# Create directories to store the converted transcripts
if os.path.exists(os.path.join(cwd, tr_path)):
    shutil.rmtree(os.path.join(cwd, tr_path))
    os.mkdir(os.path.join(cwd, tr_path))
    print('Directory Replaced')
else:
    os.mkdir(os.path.join(cwd, tr_path))
    print('Directory Created')

df = pd.read_json('dataset_original/raw_transcripts.json')
df = df.T.reset_index()
df.rename(columns={'index':'filename'})
df.to_csv(os.path.join(tr_path, 'raw_transcripts.csv'), index=False)

df = pd.read_json('dataset_original/tagged_transcripts.json')
df = df.T.reset_index()
df.rename(columns={'index':'filename'})
df.to_csv(os.path.join(tr_path, 'tagged_transcripts.csv'), index=False)

# Create directories to store the converted datasets
if os.path.exists(os.path.join(cwd, data_path)):
    shutil.rmtree(os.path.join(cwd, data_path))
    os.mkdir(os.path.join(cwd, data_path))
    print('Directory Replaced')
else:
    os.mkdir(os.path.join(cwd, data_path))
    print('Directory Created')

windows = [5, 6, 8, 10, 12, 15]

for window in windows:
    print(f'Window {window}: Started')
    with open(f'dataset_original/FOOTBALL/football_{window}.json') as f:
        data = json.load(f)
        
    df = pd.json_normalize(data, max_level=2)
    df2 = df.T.reset_index(drop=True).rename(columns={0:'column'})
    df3 = pd.DataFrame(columns=['Player', 'Position', 'Race', 'Reference', 'Teams', 'Year', 'Mention'])

    for i in range(0, len(df2), 7):
        d = {'Player': df2['column'][i], 'Position': df2['column'][i+1], 'Race': df2['column'][i+2], 
            'Reference': df2['column'][i+3], 'Teams': [df2['column'][i+4]], 
            'Year': df2['column'][i+5], 'Mention': [df2['column'][i+6]]}
        df3 = pd.concat([df3, pd.DataFrame(d)])

    df3.to_csv(os.path.join(data_path, f'mentions_by_player_{window}.csv'), index=False)
    print(f'Window {window}: Done')