import pandas as pd
import shutil
import spacy
import ast
import os
import re

# Convert our "strange" string format to a coherent text, removing special characters (tag, etc.)
def join_text(text):
    pattern = '^[^a-zA-Z0-9]'
    return ' '.join(token for token in ast.literal_eval(text) if not re.match(pattern, token))

# Cleaning function to preprocess our mentions
def clean(text):
    return ' '.join([token.lemma_          # Lemmization
           for token in nlp(text.lower())  # Split sentences into lowercase words
           if token.pos_ in content])      # Keep only "content" words

# Select path where to save the cleaned mentions
cwd = os.getcwd()
clean_path = os.path.join('dataset_converted', 'mentions_cleaned')

# Create directories to store the cleaned mentions
if os.path.exists(os.path.join(cwd, clean_path)):
    shutil.rmtree(os.path.join(cwd, clean_path))
    os.mkdir(os.path.join(cwd, clean_path))
    print('Directory Replaced')
else:
    os.mkdir(os.path.join(cwd, clean_path))
    print('Directory Created')

windows = [5, 6, 8, 10, 12, 15]

for window in windows:

    print(f'Window {window}: Starting...')

    # Import mentions
    path = 'dataset_converted/mentions'
    df = pd.read_csv(os.path.join(cwd, path, f'mentions_by_player_{window}.csv'))
    
    # Select only QBs from 2006 on
    df = df[df['Year'] >= 2006].reset_index(drop=True)
    df = df[df['Position'] == 'QB']

    # Uppercase first letters
    for index, row in df.iterrows():
        df.at[index, 'Player'] = row['Player'].title()

    # Import spacy
    nlp = spacy.load('en_core_web_sm')

    # Define content words
    content = {'NOUN', 'VERB', 'ADJ', 'ADV', 'X', 'PROPN'}

    # We create a new column for the preprocessed mentions and we apply our functions
    df['Mention_Cleaned'] = df['Mention'].apply(join_text).apply(clean)

    # Remove empty reports
    df = df[df['Mention'].notnull()]

    # Make sure everything is a string
    df['Mention'] = df['Mention'].apply(str)

    df.to_csv(os.path.join(cwd, clean_path, f'mentions_cleaned_{window}.csv'), index=False)

    print(f'Window {window}: Done!')