import pandas as pd
import numpy as np
import os
import requests
from io import StringIO
import matplotlib

filenames = ["Amanda.csv", "BabyGotBack.csv", "Ben.csv", "Bump,Bump,Bump.csv",  "DukeOfEarl.csv", "ComeOnEileen.csv","GetBusy.csv", "HelpMe,Rhonda.csv","LetMeLoveYou.csv", "MyLove.csv","OnlyGirlInTheWorld.csv", "PennyLane.csv", "ShakeItOff.csv", "SlowJamz.csv", "TheStreak.csv"]

#git = "https://github.com/GEMcordelli/Personal-Projects/tree/main/Artists/Songs"

combined = []

for file in filenames:
    read = pd.read_csv(file)
    combined.append(read)
    
    
combined
    
combined = pd.concat(combined)

combined = pd.DataFrame(combined)

# save as csv in Songs Folder

combined.to_csv("AllSongs.csv", index=False)

# Clean Out Lyric Annotations

cleaning = combined

cleaning["chunk_str"] = cleaning.Content.str.replace(r"[\[\]\,\/\\\"]", ' ', regex=True)  # Remove brackets, comma, slash, backslash, quotes
cleaning["chunk_str"] = cleaning["chunk_str"].str.replace(r"^\s+|\s+$", "", regex=True)  # Strip leading and trailing whitespaces
cleaning = cleaning.drop(columns = ["Content"])

# save as a text file then import using open and split
cleaning.to_csv("AllSongs_Cleaned.csv", sep = "\t", index = False)

# tokenize for word frequency (we dont want this to be our only table; removes important stylistic information, i.e. parentheses, ..., etc.)
# add a line_id as index name so we can have a layered index of line_num and token_num later on
K = cleaning.index.name("line_id")
K = cleaning.chunk_str.str.split(expand=True).stack().to_frame('token_str')
K.index.names = ['line_num','token_num']
# looks like tokenizing might have actually kept in some of the key lyrical annotations! This can serve useful for other analysis
K.iloc[800:820]

K.to_csv("TOKENS_AllSongs.csv", index = False)


# Vocabulary Table
V = K.token_str.value_counts().to_frame('n')
V
V.index.name = 'term_str'

# probability of every token in the corpus over total token num; I might have to end up making a versiion of TOKENS with no 
# annotation marks because it will group their probability and frequency differently than the same words without annotations 
# #and may end up being a grouping of just one specific song
V['p'] = V.n/V.n.sum()
V["char_len"] = V.index.str.len()

V.to_csv("VOCAB_AllSongs.csv", index = True)

# Vocab Visuals

V.p.plot(figsize=(10,5), fontsize=14, rot=45, legend=False)

V.p.head(20).sort_values().plot.barh(figsize=(10,10))
V.index.name

